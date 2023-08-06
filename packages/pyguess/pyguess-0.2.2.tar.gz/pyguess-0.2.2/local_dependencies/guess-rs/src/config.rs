use crate::addr::{PLACE_UBOUND, STREETS_DATA_PATH};
use crate::metrics::{StringMetric, StringMetricFn};
use clap::Parser;
use std::path::PathBuf;
use std::thread;

pub const DEFAULT_UBOUND: f64 = 0.6;

#[derive(Clone, Copy)]
pub struct UBound(pub f64);

impl UBound {
    pub fn new(value: f64) -> Self {
        if 1.0 - value < 0.0 {
            panic!(
                "ERROR: Upper bound should be lower or equal than 1.0, but the value was {}",
                value
            );
        }
        if value - 1e-10 < 0.0 {
            panic!(
                "ERROR: Upper bound should be larger or equal than 0.0, but the value was {}",
                value
            );
        }
        Self(value)
    }
}

impl Default for UBound {
    fn default() -> Self {
        Self(DEFAULT_UBOUND)
    }
}

#[derive(Clone)]
pub struct Config {
    pub ubound: UBound,
    pub place_ubound: UBound,
    pub max_candidates: usize,
    pub metric_fn: StringMetricFn,
    pub max_threads: usize,
    pub path_to_streets: PathBuf,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            ubound: UBound::default(),
            place_ubound: UBound::new(PLACE_UBOUND),
            max_candidates: 1,
            metric_fn: StringMetric::default().into(),
            max_threads: thread::available_parallelism().unwrap().get(),
            path_to_streets: PathBuf::from(STREETS_DATA_PATH),
        }
    }
}

impl Config {
    /// `ubound` - an upper threshold of the `similarity` between
    ///            candidate and target that still should be kept
    ///
    /// `max_candidates` - a number of candidates to keep after the matching process
    ///
    /// `metric` - a string metric to use for text matching
    ///
    /// `max_threads` - a number of threads to use during the file matching
    ///
    /// `path_to_streets` - a path to "streets_data/" folder
    ///
    /// # Panics
    /// Panics if the sensitivity value is lower than 0.0 or larger than 1.0
    pub fn new(
        ubound: f64,
        place_ubound: f64,
        max_candidates: usize,
        metric: StringMetric,
        max_threads: Option<usize>,
        path_to_streets: Option<String>,
    ) -> Self {
        Self {
            ubound: UBound::new(ubound),
            place_ubound: UBound::new(place_ubound),
            max_candidates,
            metric_fn: metric.into(),
            max_threads: max_threads
                .unwrap_or_else(|| thread::available_parallelism().unwrap().get()),
            path_to_streets: PathBuf::from(
                path_to_streets.unwrap_or_else(|| String::from(STREETS_DATA_PATH)),
            ),
        }
    }

    pub fn from_args(args: &Args) -> Self {
        Self::new(
            args.sens,
            args.place_sens,
            args.results,
            args.metric,
            args.threads,
            args.streets.clone(),
        )
    }
}

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
pub struct Args {
    /// Street to match
    #[arg(short, long)]
    pub street: String,

    /// The string metric to use. Available options: levenshtein,
    /// damerau-levenshtein, jaro, jaro-winkler, sorensed-dice, osa
    #[arg(short, long, default_value_t=StringMetric::default())]
    pub(crate) metric: StringMetric,

    /// Path to streets_data folder (see misc/data as an example)
    #[arg(long)]
    pub(crate) streets: Option<String>,

    /// The place where to search street
    #[arg(short, long)]
    pub(crate) place: Option<String>,

    /// The postal code where to search street
    #[arg(short, long)]
    pub(crate) zip: Option<usize>,

    /// Sensitivity of search: from 0.0 (None of candidates are accepted) to 1.0 (All candidates are accepted)
    #[arg(long, default_value_t=DEFAULT_UBOUND)]
    pub(crate) sens: f64,

    /// Sensitivity of place search: from 0.0 (None of candidates are accepted) to 1.0 (All candidates are accepted)
    #[arg(long, default_value_t=PLACE_UBOUND)]
    pub(crate) place_sens: f64,

    /// Number of results to keep
    #[arg(short, long, default_value_t = 1)]
    pub(crate) results: usize,

    /// Number of threads to use for string matching
    #[arg(short, long)]
    pub(crate) threads: Option<usize>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "should be larger or equal than")]
    fn sensitivity_lower_than_zero() {
        UBound::new(-1.0);
    }

    #[test]
    #[should_panic(expected = "should be lower or equal than")]
    fn sensitivity_larger_than_one() {
        UBound::new(1.1);
    }
}
