//! This module creates an object that represents the candidate text to the target text
use std::cmp::{Ordering, PartialEq};

#[derive(Debug, Clone, Default)]
pub struct Candidate {
    pub sequence: String,
    pub distance: f64,
}

impl Candidate {
    pub fn from(sequence: &str) -> Self {
        Self {
            sequence: sequence.to_owned(),
            distance: 0.0,
        }
    }
}

impl PartialEq for Candidate {
    fn eq(&self, other: &Self) -> bool {
        self.sequence == other.sequence
    }
}

impl PartialOrd for Candidate {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        self.distance.partial_cmp(&other.distance)
    }
}
