//! This crate is aimed to be a simple and fast solution for text-matching from the file with
//! more than 2 millions of lines, especially for streets in Switzerland.
//!
//! Also, it serves as my first Rust project used for work and published out to the people
use guess_rs::{self as guessr, Address, Config, GResult, Location, StringMetric, UBound};
use pyo3::basic::CompareOp;
use pyo3::prelude::*;
use std::{fmt, path::PathBuf};

#[derive(FromPyObject, Clone, PartialEq, Eq)]
enum PyLocation {
    #[pyo3(transparent)]
    Place(String),
    #[pyo3(transparent)]
    Zip(usize),
}

impl fmt::Display for PyLocation {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Self::Place(place) => place.clone(),
                Self::Zip(zip) => zip.to_string(),
            }
        )
    }
}

impl IntoPy<Py<PyAny>> for PyLocation {
    fn into_py(self, py: Python) -> Py<PyAny> {
        match self {
            PyLocation::Place(value) => value.into_py(py),
            PyLocation::Zip(value) => value.into_py(py),
        }
    }
}

impl From<PyLocation> for Location {
    fn from(source: PyLocation) -> Self {
        match source {
            PyLocation::Place(place) => Location::Place(place),
            PyLocation::Zip(zip) => Location::Zip(zip),
        }
    }
}

/// A config for guess
#[derive(Clone)]
#[pyclass(get_all, set_all, name = "Config")]
struct PyConfig {
    ubound: Option<f64>,
    place_ubound: Option<f64>,
    max_candidates: Option<usize>,
    metric: Option<String>,
    max_threads: Option<usize>,
    path_to_streets: Option<String>,
}

#[pymethods]
impl PyConfig {
    /// Create a new PyConfig instance
    #[new]
    fn new(
        ubound: Option<f64>,
        place_ubound: Option<f64>,
        max_candidates: Option<usize>,
        metric: Option<String>,
        max_threads: Option<usize>,
        path_to_streets: Option<String>,
    ) -> Self {
        Self {
            ubound,
            place_ubound,
            max_candidates,
            metric,
            max_threads,
            path_to_streets,
        }
    }
}

impl From<PyConfig> for Config {
    fn from(pyconfig: PyConfig) -> Self {
        let default_config = Self::default();
        Self {
            ubound: pyconfig.ubound.map_or(default_config.ubound, UBound::new),
            place_ubound: pyconfig
                .place_ubound
                .map_or(default_config.place_ubound, UBound::new),
            max_candidates: pyconfig
                .max_candidates
                .unwrap_or(default_config.max_candidates),
            metric_fn: pyconfig.metric.map_or(default_config.metric_fn, |x| {
                Into::<StringMetric>::into(x).into()
            }),
            max_threads: pyconfig.max_threads.unwrap_or(default_config.max_threads),
            path_to_streets: pyconfig
                .path_to_streets
                .map_or(default_config.path_to_streets, PathBuf::from),
        }
    }
}

/// A guess candidate
#[derive(Clone)]
#[pyclass(get_all, set_all, name = "Candidate")]
struct PyCandidate {
    street: String,
    location: Option<PyLocation>,
}

#[pymethods]
impl PyCandidate {
    #[new]
    fn new(street: String, location: Option<PyLocation>) -> Self {
        Self { street, location }
    }

    fn __eq__(&self, other: &PyAny) -> PyResult<bool> {
        let other_candidate = other.extract::<Self>()?;
        Ok(self.street == other_candidate.street && self.location == other_candidate.location)
    }

    fn __ne__(&self, other: &PyAny) -> PyResult<bool> {
        self.__eq__(other).map(|x| !x)
    }

    fn __str__(&self) -> PyResult<String> {
        let location = self
            .location
            .as_ref()
            .map(|x| x.to_string())
            .unwrap_or("".to_string());
        Ok(format!("{}, {}", &self.street, location))
    }

    fn __richcmp__(&self, other: &PyAny, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => self.__eq__(other),
            CompareOp::Ne => self.__ne__(other),
            _ => Ok(false),
        }
    }
}

impl PyCandidate {
    fn from_match(address: GResult<Address>) -> Option<Self> {
        let address = address.ok()?;
        Some(PyCandidate {
            street: address.0.sequence,
            location: match address.1 {
                Location::Empty => None,
                Location::Place(place) => Some(PyLocation::Place(place)),
                Location::Zip(zip) => Some(PyLocation::Zip(zip)),
            },
        })
    }
}

#[pyfunction]
fn guess_address(
    street: &str,
    location: Option<PyLocation>,
    config: Option<PyConfig>,
) -> Option<PyCandidate> {
    let config = config.map_or(Config::default(), |x| x.into());
    let location = location.map_or(Location::Empty, |x| x.into());
    let mat = guessr::guess_address(street, location, config);
    PyCandidate::from_match(mat)
}

#[pymodule]
fn pyguess(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(guess_address, m)?)?;
    m.add_class::<PyCandidate>()?;
    m.add_class::<PyConfig>()?;
    Ok(())
}
