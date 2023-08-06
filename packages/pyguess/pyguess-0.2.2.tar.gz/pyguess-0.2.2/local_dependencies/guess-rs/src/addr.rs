use crate::{
    config::{Args, Config, UBound},
    guessr, StringMetric,
};
use regex::Regex;
use std::{fs, io};
use toml::Value;

pub(crate) const PLACE_UBOUND: f64 = 0.8;
const STRING_METRIC_PLACE: StringMetric = StringMetric::JaroWinkler;
const FILE_EXTENSION: &str = "toml";
const FORWARD_SLASH_REPL: &str = "%2C";
pub(crate) const STREETS_DATA_PATH: &str = "../misc/data/streets_data";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Location {
    Place(String),
    Zip(usize),
    Empty,
}

impl Location {
    pub fn guess(&self, config: &Config, candidates: Vec<String>) -> Self {
        match self {
            Self::Place(place) => {
                let config = Config {
                    ubound: UBound::new(PLACE_UBOUND),
                    max_candidates: 1,
                    metric_fn: STRING_METRIC_PLACE.into(),
                    ..config.clone()
                };
                let guessed_location =
                    guessr::search_in_candidates_list(place, &candidates, &config);
                guessed_location.ok().map_or(Self::Empty, |location| {
                    Self::Place(location[0].sequence.to_string())
                })
            }
            _ => self.clone(),
        }
    }

    pub fn from_args(args: &Args) -> Self {
        if let Some(place) = args.place.clone() {
            Location::Place(place)
        } else if let Some(zip) = args.zip {
            Location::Zip(zip)
        } else {
            Location::Empty
        }
    }
}

impl ToString for Location {
    fn to_string(&self) -> String {
        match self {
            Self::Place(place) => place.to_string(),
            Self::Zip(zip) => zip.to_string(),
            Self::Empty => panic!("Trying to convert Location::Empty to String"),
        }
    }
}

#[inline]
pub(crate) fn contains_numbers(street: &str) -> bool {
    street.chars().filter(|ch| ch.is_numeric()).count() > 0
}

fn find_street_name<'a>(
    street: &'a str,
    number1: Option<&'a str>,
    number2: Option<String>,
) -> Option<&'a str> {
    let mut idxs = Vec::new();

    if let Some(number) = number1 {
        idxs.push(street.find(number).unwrap());
    }
    if let Some(number) = number2 {
        idxs.push(street.find(&number).unwrap());
    }
    idxs.iter().min().map(|min_idx| street[..*min_idx].trim())
}

fn parse_many_streets(street: &str) -> Vec<String> {
    if !contains_numbers(street) {
        return Vec::new();
    }
    let re = Regex::new(r"(\d+([a-zA-Z]-[a-zA-Z]|[a-zA-Z])?)[,/]").unwrap();
    let mut numbers = re
        .captures_iter(street)
        .map(|captures| captures.get(1).unwrap().as_str())
        .collect::<Vec<&str>>();

    // Capture last number in the list
    if !numbers.is_empty() {
        let idx = street.find(numbers.last().unwrap()).unwrap() + numbers.last().unwrap().len();
        let re = Regex::new(r"^\d+([a-zA-Z]-[a-zA-Z]|[a-zA-Z])?\b").unwrap();
        let chars_to_trim: &[char] = &[',', '/', ' '];
        if let Some(mat) = re.find(street[idx..].trim_matches(chars_to_trim)) {
            let matches = mat.as_str().split('-').collect::<Vec<&str>>();
            if matches.len() == 1 || (matches.len() == 2 && matches[1].parse::<u32>().is_err()) {
                numbers.push(mat.as_str());
            }
        }
    }

    let re = Regex::new(r"(\d+)-(\d+)").unwrap();
    let numbers_ranges = re
        .captures_iter(street)
        .flat_map(|captures| {
            let start_num_range = captures.get(1).unwrap().as_str().parse::<usize>().unwrap();
            let end_num_range = captures.get(2).unwrap().as_str().parse::<usize>().unwrap();
            start_num_range..=end_num_range
        })
        .map(|x| x.to_string())
        .collect::<Vec<String>>();

    numbers.extend(
        &numbers_ranges
            .iter()
            .map(|x| x.as_str())
            .collect::<Vec<&str>>(),
    );

    let street_name = if let Some(street_name) = find_street_name(
        street,
        numbers.first().copied(),
        numbers_ranges.first().cloned(),
    ) {
        street_name
    } else {
        return vec![street.trim().to_string()];
    };

    numbers.sort();
    numbers.dedup();

    let re_numbers_range = Regex::new(r"([a-zA-Z])-([a-zA-Z])").unwrap();
    let re_number = Regex::new(r"^(\d+)[a-zA-Z]").unwrap();
    numbers
        .iter()
        .flat_map(|x| match re_numbers_range.captures(x) {
            Some(captures) => {
                let number = re_number.captures(x).unwrap().get(1).unwrap().as_str();
                let start_char = captures.get(1).unwrap().as_str().chars().next().unwrap();
                let end_char = captures.get(2).unwrap().as_str().chars().next().unwrap();
                (start_char..=end_char)
                    .map(|ch| format!("{} {}{}", street_name, number, ch))
                    .collect::<Vec<String>>()
            }
            None => vec![format!("{} {}", street_name, x)],
        })
        .collect()
}

fn split_streets(street: &str) -> Vec<String> {
    let re = Regex::new(r"(.*?)/([^0-9]|(3-|1[.]|4[b ]))").unwrap();
    let mut streets: Vec<String> = Vec::new();
    let mut prefix: Option<&str> = None;
    for captures in re.captures_iter(street) {
        streets.push(prefix.unwrap_or_default().to_string() + captures.get(1).unwrap().as_str());
        if let Some(mat) = captures.get(2) {
            prefix = Some(mat.as_str());
        }
    }
    if let Some(last_street) = streets.last() {
        let idx = street.find(last_street).unwrap() + last_street.len();
        if idx < street.len() {
            let chars_to_trim: &[char] = &['/', ' '];
            streets.push(street[idx..].trim_matches(chars_to_trim).to_string());
        }
    }
    if streets.is_empty() {
        return vec![street.to_string()];
    }
    streets
}

pub(crate) fn detect_streets(street: &str) -> Vec<String> {
    if street.contains('/') {
        split_streets(street)
    } else {
        vec![street.to_string()]
    }
    .iter()
    .flat_map(|street| parse_many_streets(street))
    .collect()
}

#[inline]
pub(crate) fn starts_with_number(street: &str) -> bool {
    Regex::new(r"^\d+,?\s.+").unwrap().is_match(street)
        || Regex::new(r"^\w\d+,?\s").unwrap().is_match(street)
}

pub fn replace_prefixes(mut street: String) -> String {
    street = street.replace("str.", "strasse");
    let replacements = [
        (r"\bst-", "saint-"),
        (r"\brt ", "route "),
        (r"\bst\.", "saint"),
        (r"\bav\.", "avenue"),
    ];
    for (pattern, replacement) in replacements.iter() {
        let re = Regex::new(pattern).unwrap();
        street = re.replace_all(&street, *replacement).to_string();
    }
    street
}

pub(crate) fn remove_building_number(street: &str) -> String {
    let re = Regex::new(r"\b\d+[a-zA-Z]?$").unwrap();
    re.replace_all(street, "").to_string().trim().to_string()
}

pub fn clean_street(street: &str) -> String {
    let mut street = replace_prefixes(street.trim().to_lowercase());
    // Matches: '76 chemin des clos', 'a4 résidence du golf', etc.
    if starts_with_number(&street) {
        let (num, street_name) = street.split_once(' ').expect("matched by regexp");
        street = format!("{} {}", street_name, num);
    }
    // Regex to match streets in different format like:
    // eisfeldstrasse 21/23, milchstrasse 2-10a, milchstrasse 2,10a, bernstrasse 7 8, etc.
    let re = Regex::new(r"(.*?\s\d*?\s?[a-zA-Z]?)[\./,\-\+\s–\\]").unwrap();
    let street = match re.find(&street) {
        Some(mat) => {
            // Regex to replace spaces between street number and its letter,
            // e.g. bernstrasse 4 a
            let re = Regex::new(r"\s(\d+)\s+([a-zA-Z])").unwrap();
            let chars_to_trim: &[char] = &[',', '.', '-', '_', '/', ' ', ':', ';'];
            let mat = re.replace_all(mat.as_str().trim_matches(chars_to_trim), " $1$2");
            mat.to_string()
        }
        _ => street,
    };
    street
}

pub fn open_street_file(street: &str, config: &Config) -> io::Result<Value> {
    // let mut path_to_street_file = config.path_to_streets.clone();
    let path_to_street_file = config.path_to_streets.join(format!(
        "{}.{}",
        street.replace('/', FORWARD_SLASH_REPL),
        FILE_EXTENSION
    ));
    Ok(
        toml::from_str::<Value>(&fs::read_to_string(path_to_street_file)?).unwrap_or_else(|_| {
            unimplemented!("Should use new error and implement From<toml::Error> and From<io::Error> [since toml 0.7.3]")
        }),
    )
}

#[inline]
fn iter_from_toml_value(value: &Value) -> impl Iterator<Item = String> + '_ {
    value
        .as_array()
        .unwrap()
        .iter()
        .map(|x| x.to_string().replace('\"', ""))
}

fn get_all_streets(value: &Value) -> Vec<String> {
    let mut values = value
        .as_table()
        .expect("correct table structure")
        .iter()
        .flat_map(|(_, v)| iter_from_toml_value(v))
        .collect::<Vec<String>>();
    values.sort();
    values.dedup();
    values
}

fn get_locations(value: &Value) -> Vec<String> {
    value
        .as_table()
        .unwrap()
        .iter()
        .map(|(k, _)| k.to_string())
        .collect()
}

#[inline]
fn get_all_streets_empty_loc(value: &Value) -> (Vec<String>, Location) {
    (get_all_streets(value), Location::Empty)
}

pub(crate) fn streets_from_location(
    value: &Value,
    location: &Location,
    config: &Config,
) -> (Vec<String>, Location) {
    let locations = get_locations(value);
    match location.guess(config, locations) {
        Location::Empty => get_all_streets_empty_loc(value),
        guessed_location => value.get(&guessed_location.to_string()).map_or_else(
            || get_all_streets_empty_loc(value),
            |x| (iter_from_toml_value(x).collect(), guessed_location),
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_remove_building_number() {
        let actual = remove_building_number("industriestrasse 2a");
        let expected = "industriestrasse".to_string();
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_split_streets() {
        let expected = vec!["Haupstrasse 5"];
        let actual = split_streets("Haupstrasse 5");
        assert_eq!(actual, expected);
    }

    fn assert_detect_streets(expected: &[&str], street_to_detect: &str) {
        let mut actual = detect_streets(street_to_detect);
        let mut expected = expected
            .iter()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        actual.sort();
        expected.sort();
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_detect_streets() {
        let expected = &[
            (
                vec![
                    "Weinsteig 206",
                    "Weinsteig 208",
                    "Weinsteig 210",
                    "Weinsteig 212",
                    "Weinsteig 214",
                    "Weinsteig 216",
                    "Haupstrasse 26",
                    "Haupstrasse 26a",
                    "Haupstrasse 26b",
                    "Haupstrasse 26c",
                ],
                "Weinsteig 206/208/210/212/214/216/Haupstrasse 26/26a-c",
            ),
            (
                vec!["1. Gangstrasse 10", "3-Eidgenossen 30"],
                "1. Gangstrasse 10/3-Eidgenossen 30",
            ),
            (
                vec![
                    "Haupstrasse 30",
                    "Haupstrasse 31",
                    "Haupstrasse 32",
                    "Haupstrasse 34",
                    "Haupstrasse 35",
                    "Haupstrasse 36",
                ],
                "Haupstrasse 30, 31, 32, 34-36",
            ),
            (
                vec![
                    "Haupstrasse 30",
                    "Haupstrasse 31",
                    "Haupstrasse 32",
                    "Haupstrasse 33",
                    "Haupstrasse 35",
                    "Haupstrasse 36",
                    "Haupstrasse 37",
                    "Haupstrasse 38",
                    "Haupstrasse 39",
                    "Haupstrasse 40",
                ],
                "Haupstrasse 30-33, 35-40",
            ),
            (vec!["Haupstrasse 10"], "Haupstrasse 10"),
            (vec!["Wanistrassse 1"], "Wanistrassse 1, «Logistikzentrum»"),
            (
                vec![
                    "Im Sihlhof 20",
                    "Im Sihlhof 23",
                    "Im Sihlhof 4",
                    "Im Sihlhof 2",
                    "Im Sihlhof 28",
                    "Im Sihlhof 27",
                    "Im Sihlhof 24",
                    "Im Sihlhof 21",
                    "Im Sihlhof 1",
                    "Im Sihlhof 25",
                    "Im Sihlhof 22",
                    "Im Sihlhof 29",
                    "Im Sihlhof 26",
                ],
                "Im Sihlhof 1, 2, 4, 20-29, «The Jay» ",
            ),
            (
                vec!["Via Santa Caterina 1", "Largo Zorzi 1"],
                "Largo Zorzi 1 / Via Santa Caterina 1",
            ),
            (
                vec!["Route des Paquays 105"],
                "Chemin de la Confrerie / Route des Paquays 105",
            ),
            (
                vec![
                    "Schlossackerstrasse 11",
                    "Schlossackerstrasse 7",
                    "Schlossackerstrasse 9",
                    "Schlossackerstrasse 13",
                    "Hegifeldstrasse 85",
                    "Hegifeldstrasse 89",
                    "Hegifeldstrasse 87",
                    "Schlossackerstrasse 5",
                ],
                "Schlossackerstrasse 5, 7, 9, 11, 13 / Hegifeldstrasse 85, 87, 89",
            ),
            (vec!["Fadenstrasse 26"], "Fadenstrasse 26, 4Viertel"),
            (
                vec![
                    "Zentrum 2",
                    "Zentrum 3a",
                    "Zentrum 2a",
                    "Zentrum 2b",
                    "Zentrum 3",
                    "Zentrum 3b",
                ],
                "Zentrum 2, 2a, 2b, 3, 3a, 3b, «Zentrumsüberbauung»",
            ),
            (
                vec![
                    "Rheinstrasse 3",
                    "Bahnhofstrasse 3",
                    "Schützenstrasse 6",
                    "Schützenstrasse 10",
                    "Schützenstrasse 8",
                    "Schützenstrasse 4",
                    "Rheinstrasse 5",
                    "Schützenstrasse 12",
                ],
                "Bahnhofstrasse 3 / Rheinstrasse 3, 5/ Schützenstrasse 4, 6, 8, 10, 12",
            ),
            (
                vec![
                    "Neuchlenstrasse 7",
                    "Neuchlenstrasse 7a",
                    "Neuchlenstrasse 11",
                ],
                "Neuchlenstrasse 7/7a/11",
            ),
        ];
        for (expected, street) in expected.iter() {
            assert_detect_streets(expected, street);
        }
    }
}
