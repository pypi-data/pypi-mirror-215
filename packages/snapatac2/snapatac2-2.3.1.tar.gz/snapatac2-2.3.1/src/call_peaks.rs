use crate::utils::AnnDataLike;
use snapatac2_core::{export::Exporter, utils::merge_peaks};

use std::ops::Deref;
use anndata::Backend;
use anndata_hdf5::H5;
use pyanndata::data::PyDataFrame;
use pyo3::prelude::*;
use bed_utils::bed::{BEDLike, GenomicRange, io::Reader, tree::BedTree};
use flate2::read::MultiGzDecoder;
use tempfile::Builder;
use log::info;
use std::fs::File;
use polars::{prelude::{DataFrame, NamedFrom}, series::Series};
use std::collections::HashSet;
use anyhow::Result;

#[pyfunction]
pub fn call_peaks(
    anndata: AnnDataLike,
    group_by: Vec<&str>,
    selections: Option<HashSet<&str>>,
    q_value: f64,
    out_dir: Option<&str>,
) -> Result<PyDataFrame> {
    let dir = Builder::new().tempdir_in("./").unwrap();
    let temp_dir = out_dir.unwrap_or(dir.path().to_str().unwrap());

    macro_rules! run {
        ($data:expr) => {
            $data.call_peaks(
                q_value, &group_by, selections, temp_dir, "", ".NarrowPeak.gz",
            )?
        }
    }
    let peak_files = crate::with_anndata!(&anndata, run);
    let peak_iter = peak_files.values().flat_map(|fl|
        Reader::new(MultiGzDecoder::new(File::open(fl).unwrap()), None)
        .into_records().map(Result::unwrap)
    );

    info!("Merging peaks...");
    let peaks: Vec<_> = merge_peaks(peak_iter, 250).flatten().collect();
    let n = peaks.len();

    let peaks_str = Series::new("Peaks",
        peaks.iter().map(|x| x.to_genomic_range().pretty_show()).collect::<Vec<_>>());
    let peaks_index: BedTree<usize> = peaks.into_iter().enumerate().map(|(i, x)| (x, i)).collect();
    let iter = peak_files.into_iter().map(|(key, fl)| {
        let mut values = vec![false; n];
        Reader::new(MultiGzDecoder::new(File::open(fl).unwrap()), None)
        .into_records().for_each(|x| {
            let bed: GenomicRange = x.unwrap();
            peaks_index.find(&bed).for_each(|(_, i)| values[*i] = true);
        });
        Series::new(key.as_str(), values)
    });

    let df = DataFrame::new(std::iter::once(peaks_str).chain(iter).collect())?;
    dir.close()?;
    Ok(df.into())
}