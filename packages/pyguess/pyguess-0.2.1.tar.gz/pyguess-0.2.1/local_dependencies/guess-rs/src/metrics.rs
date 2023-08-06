//! This module creates API and algorithm of matching candidates from file input.
//! Candidates in file should be separated by newline

use std::fmt;

pub(crate) type StringMetricFn = fn(&str, &str) -> f64;

#[derive(Clone, Copy, Debug)]
pub enum StringMetric {
    Levenshtein,
    DamerauLevenshtein,
    /// The same as Jaro, but gives additional boost to texts with the same prefix
    JaroWinkler,
    Jaro,
    SorensenDice,
    Osa,
}

impl Default for StringMetric {
    fn default() -> Self {
        Self::Levenshtein
    }
}

impl fmt::Display for StringMetric {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}",
            match self {
                StringMetric::Levenshtein => "levenshtein",
                StringMetric::Jaro => "jaro",
                StringMetric::JaroWinkler => "jaro-winkler",
                StringMetric::SorensenDice => "sorensen-dice",
                StringMetric::DamerauLevenshtein => "damerau-levenshtein",
                StringMetric::Osa => "osa",
            }
        )
    }
}

impl From<String> for StringMetric {
    fn from(metric: String) -> Self {
        match metric.as_str() {
            "levenshtein" => StringMetric::Levenshtein,
            "jaro" => StringMetric::Jaro,
            "jaro-winkler" => StringMetric::JaroWinkler,
            "sorensen-dice" => StringMetric::SorensenDice,
            "damerau-levenshtein" => StringMetric::DamerauLevenshtein,
            "osa" => StringMetric::Osa,
            _ => panic!("Unknown string metric: {}", metric),
        }
    }
}

impl From<StringMetric> for StringMetricFn {
    fn from(metric: StringMetric) -> Self {
        match metric {
            StringMetric::Levenshtein => strsim::normalized_levenshtein,
            StringMetric::Jaro => strsim::jaro,
            StringMetric::JaroWinkler => strsim::jaro_winkler,
            StringMetric::SorensenDice => strsim::sorensen_dice,
            StringMetric::DamerauLevenshtein => strsim::normalized_damerau_levenshtein,
            StringMetric::Osa => |a, b| {
                1.0 - (strsim::osa_distance(a, b) as f64)
                    / (a.chars().count().max(b.chars().count()) as f64)
            },
        }
    }
}
