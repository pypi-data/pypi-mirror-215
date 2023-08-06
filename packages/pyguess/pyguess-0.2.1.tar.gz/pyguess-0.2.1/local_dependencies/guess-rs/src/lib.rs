//! This crate is aimed to be a simple and fast solution for text-matching from the file with
//! more than 2 millions of lines, especially for streets in Switzerland.
//!
//! It serves as my first Rust project used for work and published out to the people
pub mod addr;
pub mod candidate;
pub mod config;
pub mod guessr;
pub mod metrics;

pub use addr::Location;
pub use candidate::Candidate;
pub use config::{Config, UBound};
pub use guessr::{guess_address, Address};
pub use metrics::StringMetric;

pub mod error {
    use std::{error::Error as StdError, fmt, io};

    #[derive(Debug)]
    pub enum Error {
        Io(io::Error),
        InvalidCandidate(String),
        NotFound(String),
    }

    impl fmt::Display for Error {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            match self {
                Self::NotFound(candidate) => write!(f, "Candidates not found for {}", candidate),
                Self::InvalidCandidate(err) => f.write_str(err),
                Self::Io(err) => f.write_str(&err.to_string()),
            }
        }
    }

    impl StdError for Error {
        fn description(&self) -> &str {
            match *self {
                Error::Io(_) => "I/O Error",
                Error::InvalidCandidate(_) => "Invalid Candidate",
                Error::NotFound(_) => "Candidates Not Found",
            }
        }
    }

    impl From<io::Error> for Error {
        fn from(err: io::Error) -> Self {
            Self::Io(err)
        }
    }
}

pub type GResult<T> = Result<T, error::Error>;
