//! This module provides matching on official Switzerland streets
use crate::{
    addr::{self, Location},
    error::Error as GError,
    Candidate, Config, GResult, StringMetric,
};
use std::{
    cmp,
    fs::File,
    io::{prelude::*, BufReader},
    path::Path,
    sync::{Arc, Mutex},
};
use threadpool::ThreadPool;

pub type Address = (Candidate, Location);

pub(crate) const PUNCTUATIONS: &[char] =
    &['_', '\\', '(', ')', ',', '\"', ';', ':', '\'', '/', '+'];
const STRING_METRIC_STREET: StringMetric = StringMetric::Jaro;
const MAX_STREET_CANDIDATES: usize = 500;
pub const STREET_NAMES_FILE: &str = "street_names.txt";

#[inline]
fn search_nearest_streets(street: &str, config: &Config) -> Vec<String> {
    let street_names_path = config.path_to_streets.clone().join(STREET_NAMES_FILE);
    search_in_candidates_file(street, &street_names_path, config)
        .unwrap_or_else(|err| match err {
            GError::Io(_) => panic!(
                "Unable to open a file: {}",
                street_names_path.to_str().unwrap()
            ),
            _ => Vec::new(),
        })
        .into_iter()
        .map(|x| x.sequence)
        .collect()
}

fn search_similar_streets(street: &str, config: &Config) -> GResult<Vec<Candidate>> {
    // Filter distant streets using simpler Jaro metric to reduce search time
    let nearest_streets = search_nearest_streets(
        street,
        &Config {
            max_candidates: cmp::max(MAX_STREET_CANDIDATES, config.max_candidates),
            metric_fn: STRING_METRIC_STREET.into(),
            ..config.clone()
        },
    );
    search_in_candidates_list(street, &nearest_streets, config)
}

fn sort_and_keep_max_cands(
    mut candidates: Vec<Candidate>,
    max_candidates: usize,
) -> Vec<Candidate> {
    candidates.sort_by(|l, r| r.partial_cmp(l).unwrap());
    candidates[..cmp::min(max_candidates, candidates.len())].to_vec()
}

#[inline]
fn clean_sequence(sequence: &str) -> String {
    sequence.to_lowercase().replace(PUNCTUATIONS, "")
}

pub fn search_in_candidates_list(
    target_sequence: &str,
    candidates: &[String],
    config: &Config,
) -> GResult<Vec<Candidate>> {
    let target_sequence = clean_sequence(target_sequence);
    let candidates = candidates
        .iter()
        .flat_map(|x| {
            let candidate_sequence = clean_sequence(x);
            let distance = (config.metric_fn)(&target_sequence, &candidate_sequence);
            if distance - config.ubound.0 > 0.0 {
                Some(Candidate {
                    sequence: x.to_string(),
                    distance,
                })
            } else {
                None
            }
        })
        .collect::<Vec<Candidate>>();

    if !candidates.is_empty() {
        Ok(sort_and_keep_max_cands(candidates, config.max_candidates))
    } else {
        Err(GError::NotFound(target_sequence))
    }
}

pub fn search_in_candidates_file(
    sequence: &str,
    file: &Path,
    config: &Config,
) -> GResult<Vec<Candidate>> {
    let lines = BufReader::new(File::open(file)?)
        .lines()
        .flatten()
        .collect::<Vec<String>>();
    let pool = ThreadPool::new(config.max_threads);
    let matches = Arc::new(Mutex::new(Vec::with_capacity(
        config.max_threads * config.max_candidates,
    )));

    for chunk in lines.chunks(lines.len() / config.max_threads + 1) {
        let candidates = matches.clone();
        let chunk = chunk.to_vec();
        let sequence = sequence.to_string();
        let config = config.clone();
        pool.execute(move || {
            for candidate in
                search_in_candidates_list(&sequence, &chunk, &config).unwrap_or_default()
            {
                candidates.lock().unwrap().push(candidate);
            }
        });
    }
    pool.join();

    let matches = matches.lock().unwrap().to_vec();

    if !matches.is_empty() {
        Ok(sort_and_keep_max_cands(matches, config.max_candidates))
    } else {
        Err(GError::NotFound(sequence.to_string()))
    }
}

/// Search for a candidate street(s) to a target street within a Postal Code (`zip`).
/// All official street candidates here grouped into files named by a street name.
/// `zip` must be a valid Switzerland Postal Code represented officially by government.
/// Otherwise, if `zip` did not match any of existings Postal Codes in the street name file,
/// the search on all streets in the file is provided.
/// Also, if a candidate was not found within a given `zip`, the same logic (search on all streets) is applied.
///
/// Search for a candidate street(s) to a target street within a Swiss peace of territory, assigned to the Postal Code (called `place`).
/// All official street candidates here grouped into files named by street names.
/// `place` could be an invalid name. In this case, the matcher will try to search for `place` candidate inside a guessed street name file.
/// If `place` did not match any of existings Postal Codes in the file,
/// the search on all streets in the file is provided.
///
/// # Examples
///
/// ```rust
/// # use guess_rs::{Location, self as guessr, Config};
/// #
/// # fn main() {
/// #     let street = "qu du seujet 36";
/// #     let mat = guessr::guess_address(street, Location::Zip(1201), Config::default()).unwrap();
/// #     assert_eq!(mat.0.sequence, String::from("quai du seujet 36"));
/// # }
/// ```
///
/// ```rust
/// # use guess_rs::{Location, self as guessr, Config};
/// #
/// # fn main() {
/// #     let street = "aarstrasse 76";
/// #     let place = String::from("Bern");
/// #     let mat = guessr::guess_address(street, Location::Place(place), Config::default()).unwrap();
/// #     assert_eq!(mat.0.sequence, String::from("aarstrasse 76"));
/// # }
/// ```
///
/// # Panics
///
/// Panics if `street` does not contain a number (as each valid street MUST contain any number)
pub fn guess_address(raw_street: &str, raw_location: Location, config: Config) -> GResult<Address> {
    let streets = addr::detect_streets(raw_street);
    if streets.is_empty() {
        return Err(GError::InvalidCandidate(format!(
            "Invalid street: {}",
            raw_street
        )));
    }
    let mut resulted_addresses: Vec<Address> = Vec::new();
    for street in streets.iter() {
        let raw_street = addr::clean_street(street).replace("henri guisan", "guisan");
        if !addr::contains_numbers(&raw_street) {
            continue;
        }
        if let Ok(similar_streets) =
            search_similar_streets(&addr::remove_building_number(&raw_street), &config)
        {
            let street_name = similar_streets[0].clone().sequence;
            let value = addr::open_street_file(&street_name, &config).unwrap_or_else(|err| {
                panic!("Unable to read street file for {}: {}", &street_name, err)
            });
            let (streets, location) = addr::streets_from_location(&value, &raw_location, &config);
            if let Ok(best_candidates) = search_in_candidates_list(&raw_street, &streets, &config) {
                let num_candidates = best_candidates.len();
                resulted_addresses.extend(
                    best_candidates
                        .into_iter()
                        .zip(vec![location; num_candidates]),
                );
            }
        }
    }
    if !resulted_addresses.is_empty() {
        resulted_addresses.sort_by(|l, r| r.0.partial_cmp(&l.0).unwrap());
        Ok(resulted_addresses[0].clone())
    } else {
        Err(GError::NotFound("Street was not found".to_string()))
    }
}

#[cfg(test)]
mod tests {
    use super::addr::Location;
    use super::*;
    use std::path::PathBuf;

    const DATA_FILE: &str = "../misc/data/streets_data/street_names.txt";
    const STREET_WITHOUT_NUMBERS: &str = "Bernstrasse";
    const STREET_WITH_NUMBER: &str = "Bernstrasse 7";

    #[test]
    fn street_contains_numbers() {
        assert!(addr::contains_numbers(STREET_WITH_NUMBER))
    }

    #[test]
    fn street_does_not_contain_numbers() {
        assert!(!addr::contains_numbers(STREET_WITHOUT_NUMBERS))
    }

    fn assert_clean_street(expected: &str, to_clean: &str) {
        assert_eq!(
            expected.to_string(),
            addr::clean_street(to_clean),
            "Testing: {} --- {}",
            expected,
            to_clean
        );
    }

    #[test]
    fn test_clean_street() {
        let candidates = &[
            ("bernstrasse 7", "   Bernstrasse 7   "),
            ("bernstrasse a4", "   a4 Bernstrasse   "),
            ("bernstrasse 4", "   4 Bernstrasse   "),
            ("bernstrasse 4a", "   Bernstrasse 4a, 5, 6   "),
            ("bernstrasse 4a", "   Bernstrasse 4a 5 6   "),
            ("bernstrasse 4a", "   Bernstrasse 4a-5-6   "),
            ("bernstrasse 4a", "   Bernstrasse 4a/5/6   "),
            ("bernstrasse 4a", "   Bernstrasse 4a. 5 6   "),
            ("bernstrasse 4a", "  Bernstrasse 4 A fasdfs"),
            ("bernstrasse 4a", "bernstr. 4a"),
            ("la roche saint-jean", "la roche st-jean"),
            ("saint-jean", "st-jean"),
            ("marco-angst-weg", "marco-angst-weg"),
            ("müsli ost-grossrüti", "müsli ost-grossrüti"),
            ("niderwis-strasse", "niderwis-str."),
            ("avenue giovanni rossi", "av. giovanni rossi"),
            ("piazza cav. giovanni rossi", "piazza cav. giovanni rossi"),
            ("route antonio", "rt antonio"),
            ("cort da muneda", "cort da muneda"),
            ("saint giovanni rossi", "st. giovanni rossi"),
        ];
        for (expected, to_clean) in candidates.iter() {
            assert_clean_street(expected, to_clean);
        }
    }

    #[test]
    fn match_with_place() {
        let location = Location::Place("bercher".to_string());
        let actual =
            guess_address("ch de saint-cierges 3", location.clone(), Config::default()).unwrap();
        let expected = (Candidate::from("chemin de saint-cierges 3"), location);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_without_place() {
        let actual =
            guess_address("ch de saint-cierges 3", Location::Empty, Config::default()).unwrap();
        let expected = (
            Candidate::from("chemin de saint-cierges 3"),
            Location::Empty,
        );
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_with_zip() {
        let location = Location::Zip(1201);
        let actual = guess_address("qu du seujet 36", location.clone(), Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), location);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_without_zip() {
        let actual = guess_address("qu du seujet 36", Location::Empty, Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), Location::Empty);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_with_wrong_zip() {
        let location = Location::Zip(1231231);
        let actual = guess_address("qu du seujet 36", location, Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), Location::Empty);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_with_wrong_first_word() {
        let location = Location::Zip(1201);
        let actual =
            guess_address("uai du seujet 36", location.clone(), Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), location);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_with_wrong_first_word_no_zip() {
        let actual = guess_address("uai du seujet 36", Location::Empty, Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), Location::Empty);
        assert_eq!(actual, expected);
    }

    #[test]
    fn match_with_wrong_first_word_wrong_zip() {
        let location = Location::Zip(2132131);
        let actual = guess_address("uai du seujet 36", location, Config::default()).unwrap();
        let expected = (Candidate::from("quai du seujet 36"), Location::Empty);
        assert_eq!(actual, expected);
    }

    #[test]
    fn guess_examples() {
        let init_data = &[
            ("Rigistrasse 10", "Pfäffikon", "pfäffikon zh"),
            ("Schlossstrasse 9", "Berg", "berg tg"),
            ("Oberfeld 7", "Root", "root"),
        ];
        for (street, place, place_expected) in init_data {
            let location = Location::Place(place.to_string());
            let actual = guess_address(street, location, Config::default()).unwrap();
            let expected = (
                Candidate::from(&street.to_lowercase()),
                Location::Place(place_expected.to_string()),
            );
            assert_eq!(actual, expected);
        }
    }

    #[test]
    fn guess_wil_place() {
        let location = Location::Place("Wil".to_string());
        let actual = guess_address("Zürcherstrasse 3", location, Config::default()).unwrap();
        let expected = (
            Candidate::from("zürcherstrasse 3"),
            Location::Place("wil sg".to_string()),
        );
        assert_eq!(actual, expected);
    }

    #[test]
    fn candidates_from_file() {
        let cfg = Config::new(
            0.5,
            addr::PLACE_UBOUND,
            1,
            StringMetric::default(),
            None,
            None,
        );
        let matches =
            search_in_candidates_file("qu du seujet 36", &PathBuf::from(DATA_FILE), &cfg).unwrap();
        assert_eq!(Candidate::from("quai du seujet"), matches[0]);
    }

    #[test]
    #[ignore]
    fn test_many_streets() {
        let streets = &[
            (
                "Neuchlenstrasse 7/7a/11",
                "neuchlenstrasse 11",
                "Gossau",
                Location::Place("gossau sg".to_string()),
            ),
            (
                "Bahnhofstrasse 3 / Rheinstrasse 3, 5/ Schützenstrasse 4, 6, 8, 10, 12",
                "bahnhofstrasse 3",
                "Aefligen",
                Location::Place("aefligen".to_string()),
            ),
            (
                "An unknows street 10/Bahnhofstrasse 3",
                "bahnhofstrasse 3",
                "Peist",
                Location::Place("peist".to_string()),
            ),
            (
                "Hauptstrasse 21",
                "hauptstrasse 21",
                "Solothurn",
                Location::Empty,
            ),
            (
                "Chemin du Cabinet 5, 7, 9, 11",
                "chemin du cabinet 11",
                "Villeneuve",
                Location::Place("villeneuve vd".to_string()),
            ),
            (
                "Rue du Grand Pont 16, 18",
                "rue du grand pont 18",
                "Lausanne",
                Location::Empty,
            ),
            (
                "Industriestrasse 2",
                "industriestrasse 2a",
                "Hochdorf",
                Location::Place("hochdorf".to_string()),
            ),
            (
                "Bohl 17",
                "bohl 17",
                "St. Gallen",
                Location::Place("st. gallen".to_string()),
            ),
            (
                "Alte Landstrasse 21, 23",
                "alte landstrasse 21",
                "Altstätten",
                Location::Place("altstätten sg".to_string()),
            ),
            (
                "Buch 16, «Seerose»",
                "buch 16",
                "Egnach",
                Location::Place("egnach".to_string()),
            ),
            (
                "Industriestrasse 40",
                "industriestrasse 40",
                "Oberentfelden",
                Location::Place("oberentfelden".to_string()),
            ),
            (
                "Via Generale Henri Guisan 13, 15 / Via Ciusarella 5",
                "via generale guisan 13",
                "Lugano-Massagno",
                Location::Empty,
            ),
            (
                "Via Generale Henri Guisan 13, 15",
                "via generale guisan 13",
                "Lugano-Massagno",
                Location::Empty,
            ),
            (
                "Bernstrasse 120, 120a, 120b, 120c",
                "bernstrasse 120a",
                "Rothrist",
                Location::Place("rothrist".to_string()),
            ),
        ];
        let config = Config {
            max_candidates: 20,
            ..Config::default()
        };
        for (to_guess, expected, place, expected_location) in streets {
            let location = Location::Place(place.to_string());
            let (actual_candidate, actual_location) =
                guess_address(to_guess, location, config.clone()).unwrap();
            assert_eq!(
                &actual_location, expected_location,
                "Comparing locations for street: {}",
                to_guess
            );
            assert_eq!(
                &actual_candidate.sequence, expected,
                "Comparing candidates for street: {}",
                to_guess
            );
        }
    }

    #[test]
    fn candidates_from_list() {
        let cfg = Config::new(
            0.5,
            addr::PLACE_UBOUND,
            1,
            StringMetric::JaroWinkler,
            None,
            None,
        );
        let matches = search_in_candidates_list(
            "foo",
            &["foobar", "foa", "2foo", "abcd"]
                .into_iter()
                .map(|x| x.to_string())
                .collect::<Vec<String>>(),
            &cfg,
        )
        .unwrap();
        assert_eq!(Candidate::from("2foo"), matches[0]);
    }
}
