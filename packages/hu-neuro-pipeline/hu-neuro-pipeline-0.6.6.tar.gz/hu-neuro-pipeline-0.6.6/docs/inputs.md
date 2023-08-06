# Pipeline inputs

This page lists all input options for the `group_pipeline()` function as well as example arguments, both in Python and R syntax.

---

* [1. Input file options](#1-input-file-options)

* [2. Output directory options](#2-output-directory-options)

* [3. Preprocessing options](#3-preprocessing-options)

* [4. Epoching options](#4-epoching-options)

* [5. Averaging options](#5-averaging-options)

* [6. Options for time-frequency analysis](#6-options-for-time-frequency-analysis)

* [7. Options for cluster-based permutation tests](#7-options-for-cluster-based-permutation-tests)

* [8. Performance options](#8-performance-options)

---

## 1. Input file options

### **`vhdr_files` (required)**

Input BrainVision EEG header files.
Either a list of `.vhdr` file paths or a single path pointing to their parent directory.
You can also specify a nested list in case that some or all participants have multiple EEG data sets that need to be concatenated.

| Python examples                                                                                      |
| ---------------------------------------------------------------------------------------------------- |
| `'Results/EEG/raw'`                                                                                  |
| `['Results/EEG/raw/Vp01.vhdr', 'Results/EEG/raw/Vp02.vhdr', ...]`                                    |
| `['Results/EEG/raw/Vp01.vhdr', ['Results/EEG/raw/Vp02_a.vhdr', 'Results/EEG/raw/Vp02_b.vhdr'], ...]` |

| R examples                                                                                                |
| --------------------------------------------------------------------------------------------------------- |
| `"Results/EEG/raw"`                                                                                       |
| `c("Results/EEG/raw/Vp01.vhdr", "Results/EEG/raw/Vp02.vhdr"...)`                                          |
| `list("Results/EEG/raw/Vp01.vhdr", c("Results/EEG/raw/Vp02_a.vhdr", "Results/EEG/raw/Vp02_b.vhdr"), ...)` |

### **`log_files` (required)**

Either a list of `.csv`, `.tsv`, or `.txt` (tab-separated) file paths or a single path pointing to their parent directory.
Can also be a list of data frames, which is useful when the log files need some cleaning before they can be matched to the EEG data (but see also `skip_log_rows` and `skip_log_conditions` below).
Either way, each log file must have the same number of rows (trials) as there are epochs in the corresponding EEG file (defined via `triggers` below).

| Python examples                | R examples                      |
| ------------------------------ | ------------------------------- |
| `['Results/RT/Vp01.txt', ...]` | `c("Results/RT/Vp01.txt", ...)` |
| `'Results/RT'`                 | `"Results/RT"`                  |
| `[pd.DataFrame({...}), ...]`   | `list(data.frame(...), ...)`    |

## 2. Output directory options

### **`output_dir` (required)**

Main output directory.
All group level outputs are saved there, including, e.g., the single trial data frame (`all_trials.csv`) and the by-participant condition averages (`all_ave.csv`/`.fif`).

| Python examples        | R examples             |
| ---------------------- | ---------------------- |
| `'Results/EEG/export'` | `"Results/EEG/export"` |

### **`clean_dir` (optional, default `None`)**

Cleaned data directory.
Each participant's continuous EEG data is saved there after downsampling, bad channel interpolation, re-referencing, ocular correction, and frequency domain filtering.
It is usually not necessary to save these intermediary files.

| Python examples       | R examples            |
| --------------------- | --------------------- |
| `None`                | `NULL`                |
| `'Results/EEG/clean'` | `"Results/EEG/clean"` |

### **`epochs_dir` (optional, default `None`)**

Epoched data directory.
Each participant's ERP epochs (defined via `triggers`) are saved there.
It is usually not necessary to save these intermediary files.
One use case for them would be to fit a linear mixed model with `time` as a groupping factor (see [here](https://mne.tools/mne-r/articles/plot_evoked_multilevel_model.html) for an example).
Note that these files contain all samples and channels for all epochs, which makes them very large (especially with `to_df=True`, see below).

| Python examples        | R examples             |
| ---------------------- | ---------------------- |
| `None`                 | `NULL`                 |
| `'Results/EEG/epochs'` | `"Results/EEG/epochs"` |

### **`report_dir` (optional, default `None`)**

HTML report directory.
If not `None`, the pipeline automatically creates one HTML report per participant, visualizing their data at various stages of processing (raw, ICA, cleaned, events, epochs, evokeds).
Note that this is experimental and will increase the runtime of the pipeline by a minute or so per participant.

| Python examples         | R examples              |
| ----------------------- | ----------------------- |
| `None`                  | `NULL`                  |
| `'Results/EEG/reports'` | `"Results/EEG/reports"` |

### **`to_df` (optional, default `True`)**

How to save MNE-Python objects (i.e., epochs and evokeds).
If `True`, save all objects as data frames in `.csv` format.
These can then easily be imported into other software like R or Excel.
If `False`, save them as `.fif` files, which take up less disk space but can only be opened by MNE-Python and other specialized M/EEG software.
You can also save them in `'both'` formats.

| Python examples               | R examples                    |
| ----------------------------- | ----------------------------- |
| `True` or `False` or `'both'` | `TRUE` or `FALSE` or `"both"` |

## 3. Preprocessing options

### **`downsample_sfreq` (optional, default `None`)**

The sampling rate (in Hz) to downsample the EEG data to before doing any preprocessing.
If `None`, retain the original sampling rate.
Moderate downsampling (e.g., to 250 Hz) will significantly speed up the processing and reduce the size of the output files.

| Python examples | R examples |
| --------------- | ---------- |
| `None`          | `NULL`     |
| `250.0`         | `250.0`    |

### **`veog_channels` (optional, default `'auto'`)**

Two EEG or EOG channel labels from which to create a new vertical electrooculography (VEOG) channel.
This virtual channel will then be used during Independent Component Analysis (ICA; see below).
Can also be `'auto'`, in which case the pipeline will check if it can find two channel labels typically used for VEOG (`['Fp1', 'FP1', 'Auge_u', 'IO1']`).
If `None`, don't construct a new VEOG channel (which is okay if using BESA and/or if a channel named `VEOG` is already present in the raw data).

| Python examples  | R examples        |
| ---------------- | ----------------- |
| `'auto'`         | `"auto"`          |
| `['Fp1', 'IO1']` | `c("Fp1", "IO1")` |
| `None`           | `NULL`            |

### **`heog_channels` (optional, default `'auto'`)**

Two EEG or EOG channel labels from which to create a new horizontal electrooculography (HEOG) channel.
This virtual channel will then be used during Independent Component Analysis (ICA; see below).
Can also be `'auto'`, in which case the pipeline will check if it can find two channel labels typically used for HEOG (`['F9', 'F10', 'Afp9', 'Afp10']`).
If `None`, don't construct a new HEOG channel (which is okay if using BESA and/or if a channel named `HEOG` is already present in the raw data).

| Python examples | R examples       |
| --------------- | ---------------- |
| `'auto'`        | `"auto"`         |
| `['F9', 'F10']` | `c("F9", "F10")` |
| `None`          | `NULL`           |

### **`montage` (optional, default `'easycap-M1'`)**

The standard or custom montage for reading channel locations.
Can be the name of one of the [standard montages](https://mne.tools/stable/generated/mne.channels.make_standard_montage.html) shipped with MNE-Python (such as `'easycap-M1'` for the standard montage used at the Neuro lab).
Can also be a file path pointing to a file with custom channel locations (see [here](https://mne.tools/stable/generated/mne.channels.read_custom_montage.html) for possible file types).

| Python examples                   | R examples                        |
| --------------------------------- | --------------------------------- |
| `'easycap-M1'`                    | `"easycap-M1"`                    |
| `'Results/EEG/chanlocs_besa.txt'` | `"Results/EEG/chanlocs_besa.txt"` |

### **`bad_channels` (optional, default: `None`)**

Bad EEG channels to repair via interpolation.
If `None`, assume that all channels of all participants are good and do not interpolate anything.
Can be a list of lists, each containing the bad channel labels for one participants.
Can also be a dict where the keys are (a selection of) participant labels and the values are lists of their corresponding bad channel labels.
Finally, there is an (experimental) `'auto'` option that automatically interpolates channels if their standard error (across epochs) exceeds a certain threshold (namely being more than three standard deviations away from the average standard error of all channels).

| Python examples                     | R examples                                 |
| ----------------------------------- | ------------------------------------------ |
| `None`                              | `NULL`                                     |
| `[['Fp1', 'TP9'], [], ['Oz'], ...]` | `list(c("Fp1", "TP9"), c(), c("Oz"), ...)` |
| `{'Vp05': ['Cz', 'F10'], ...}`      | `list("Vp05" = c("Cz", "F10"), ...)`       |
| `'auto'`                            | `"auto"`                                   |

### **`besa_files` (optional, default: `None`)**

Output files from the BESA software for ocular correction using Multiple Source Eye Correction (MSEC).
Either a list of `.matrix` file paths or a single path pointing to their parent directory.
If `None`, no ocular correction using MSEC will be performed.

| Python examples                         | R examples                               |
| --------------------------------------- | ---------------------------------------- |
| `None`                                  | `NULL`                                   |
| `['Results/EEG/cali/Vp01.matrix', ...]` | `c("Results/EEG/cali/Vp01.matrix", ...)` |
| `'Results/EEG/cali'`                    | `"Results/EEG/cali"`                     |

### **`ica_method` (optional, default: `None`)**

Method for Indepedent Component Analysis (ICA) to correct for eye movement artifacts.
For valid methods, see [`mne.preprocessing.ICA`](https://mne.tools/stable/generated/mne.preprocessing.ICA.html).
If set, an ICA decomposition will be performed on a high-pass filtered copy of the data (cutoff = 1.0 Hz) and any ICA components that correlate substantially with VEOG and/or HEOG will be removed in a fully automatic fashion.
If `None`, no ocular correction using ICA will be performed.

| Python examples | R examples  |
| --------------- | ----------- |
| `None`          | `NULL`      |
| `'fastica'`     | `"fastica"` |
| `'infomax'`     | `"infomax"` |
| `'picard'`      | `"picard"`  |

### **`ica_n_components` (optional, default: `0.99`)**

Number of principal components (from the pre-whitening PCA step) that are passed to the ICA algorithm during fitting.
Can either be an integer (greater than `1`) that specifies the number of components, or a floating point number (between `0.0` and `1.0`, exclusive) that specifies the desired amount of variance explained (potentially leading to a different number of extracted components for each participant).
This option is only used if `ica_method` is not `None`.

| Python examples | R examples |
| --------------- | ---------- |
| `0.99`          | `0.99`     |
| `15`            | `15`       |

### **`highpass_freq` (optional, default: `0.1`)**

The lower passband edge of the frequency domain filter (in Hz).
Can also be `None` to disable highpass filtering.

| Python examples | R examples |
| --------------- | ---------- |
| `0.1`           | `0.1`      |
| `None`          | `NULL`     |

### **`lowpass_freq` (optional, default: `40.0`)**

The upper passband edge of the frequency domain filter (in Hz).
Can also be `None` to disable lowpass filtering.

| Python examples | R examples |
| --------------- | ---------- |
| `40.0`          | `40.0`     |
| `None`          | `NULL`     |

## 4. Epoching options

### **`triggers` (recommended, default: `None`)**

The EEG triggers for creating epochs, usually denoting the onset of stimuli (or responses) of interest.
Should be a list of numerical trigger values.
The meaning of these triggers will be inferred later on based on the log file (see `average_by` below).
Can also be `None`, in which case *all* the triggers present in the experiment are used (so don't expect this to work).

| Python examples | R examples    |
| --------------- | ------------- |
| `[201, 202]`    | `c(201, 202)` |
| `None`          | `NULL`        |

### **`triggers_column` (optional, default: `None`)**

A column to automatically match the log file rows to the EEG epochs.
This is useful to detect and exclude any trials that are present in the log file but not in the EEG data, e.g., because the recording was paused accidently.
The column must contain the same numeric values as the relevant `triggers` in the EEG.
If you don't already have such a column in your log files, you can add it (e.g., in R) based on your conditions, and pass the resulting data frames via `log_files` (see above) into the pipeline.

| Python examples | R examples  |
| --------------- | ----------- |
| `None`          | `NULL`      |
| `'trigger'`     | `"trigger"` |

### **`epochs_tmin` (optional, default: `-0.5`)**

Start of the epoch relative to stimulus onset (in s).

| Python examples | R examples |
| --------------- | ---------- |
| `-0.5`          | `-0.5`     |

### **`epochs_tmax` (optional, default: `1.5`)**

End of the epoch relative to stimulus onset (in s).

| Python examples | R examples |
| --------------- | ---------- |
| `1.5`           | `1.5`      |

### **`baseline` (optional, default: `(-0.2, 0.0)`)**

Time period (in s relative to stimulus onset) for baseline correction.
For each epoch and channel, the average voltage during this interval is subtracted from all time points in the epoch, so as to correct for shifts in voltage level that had occured before stimulus onset.
Setting the first or the second value to `None` will use the start or the end of the epoch, respectively.
Choosing `None` instead of a tuple will skip baseline correction.

| Python examples | R examples     |
| --------------- | -------------- |
| `(-0.2, 0.0)`   | `c(-0.2, 0.0)` |
| `(None, 0.0)`   | `c(NULL, 0.0)` |
| `None`          | `NULL`         |

### **`skip_log_rows` (optional, default: `None`)**

Row indices to skip from the log file.
In case of `None`, all rows from the log file are used (but see also `skip_log_conditions` below).
Can be a list of row indices for excluding the same rows for all subjects (e.g., always skip the first three rows).
Alternatively, it can be a list (or dict) of lists for skipping different indices for each subject (e.g., because the EEG was accidently paused during some trials).
All indices are in Python style, i.e., starting from `0` (not from `1` as in R).

| Python examples                   | R examples                                |
| --------------------------------- | ----------------------------------------- |
| `None`                            | `NULL`                                    |
| `[0, 1, 2]`                       | `c(0, 1, 2)`                              |
| `[113, 114, 115], [], [12], ...]` | `list(c(113, 114, 115), c(), c(12), ...)` |
| `{'Vp12': [55, 239], ...}`        | `list("Vp12" = c(55, 239), ...)`          |

### **`skip_log_conditions` (optional, default: `None`)**

An alternative to `skip_log_rows` for excluding an entire condition (or multiple conditions) from the log file (rather than individual trials).
If `None`, all rows from the file are used (but see also `skip_log_rows` above).
Can be a dict where keys are column names from the log file and values are (lists of) condition labels as they occur in these columns.
This is useful, e.g., to exclude "filler" stimuli that don't have corresponding EEG triggers.

| Python examples                            | R examples                                       |
| ------------------------------------------ | ------------------------------------------------ |
| `None`                                     | `NULL`                                           |
| `{'emotion': 'filler'}`                    | `list("emotion" = "filler")`                     |
| `{'emotion': ['filler', 'positive'], ...}` | `list("emotion" = c("filler", "positive"), ...)` |

### **`reject_peak_to_peak` (optional, default: `200.`)**

Rejection threshold (in microvolts) for excluding epochs as "bad."
If the peak-to-peak amplitude of any channel in the time window (defined by `epochs_tmin` and `epochs_tmax`) exceeds this value, the corresponding epoch (a) will be set to `NaN` for all ERP components in the single trial data frame and (b) will not enter into the by-participant condition averages that are used for plotting and permutation testing.

| Python examples | R examples |
| --------------- | ---------- |
| `200.0`         | `200.0`    |
| `None`          | `NULL`     |

### **`components` (recommended, default: don't compute any components)**

Time window and region of interest (ROI) for the ERP component(s) of interest.
Must be a dict with the following entries:

* `'name'`: The name of each component, which will become the column name in the single trial data frame.

* `'tmin'`: The starting time point of each component (relativ to stimulus onset in s).

* `'tmax'`: The ending time point of each component (relativ to stimulus onset in s).
  
* `'roi'`: The channel labels in the ROI for each component.

| Python example                                                                                            |
| --------------------------------------------------------------------------------------------------------- |
| `{'name': ['P1', 'N170'], 'tmin': [0.08, 0.15], 'tmax': [0.13, 0.2], 'roi': [['PO3', ...], ['P7', ...]]}` |

| R example                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------- |
| `list("name" = list("P1", "N170"), "tmin" = list(0.08, 0.15), "tmax" = list(0.13, 0.2), "roi" = list(c("PO3", ...), c("P7", ...)))` |

## 5. Averaging options

### **`average_by` (recommended, default: `None`)**

(Combinations of) conditions to create per-participant averages for.
These per-participant condition averages (a.k.a. ["evokeds"](https://mne.tools/stable/auto_tutorials/evoked/10_evoked_overview.html)) are useful for plotting and for running permutation tests (see the `perm_*` arguments below).
Must be a dict where each key is a custom condition label of your choice and each value is a string expression that will be used to select the relevant trials for this condition based on columns in the log file (see examples below and the [pandas documentation on querying](https://pandas.pydata.org/docs/user_guide/indexing.html#indexing-query)).
If `None`, the pipeline will not create any custom averages but will instead create averages for each value in `triggers`.

| Python examples                                                                      | R examples                                                                              |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `None`                                                                               | `NULL`                                                                                  |
| `{'related': 'semantics == "related"', 'unrelated': 'semantics == "unrelated"}`      | `list(related = "semantics == 'related'", unrelated = "semantics == 'unrelated'")`      |
| `{'neg_unrel': 'context == "negative" & semantics == "unrelated" & rt < 3000', ...}` | `list(neg_unrel = "context == 'negative' & semantics == 'unrelated' & rt < 3000", ...)` |

## 6. Options for time-frequency analysis

### **`perform_tfr` (optional, default: `False`)**

Whether or not to perform time-frequency analysis in addition to ERPs.

| Python examples | R examples |
| --------------- | ---------- |
| `False`         | `FALSE`    |
| `True`          | `TRUE`     |

### **`tfr_subtract_evoked` (optional, default: `False`)**

Whether or not to subtract evoked activity from epochs before computing the time-frequency representation.
If `False`, the resulting spectral power will not just reflect induced activity but also evoked activity from the ERP.
If `True`, the average ERP is removed before computing spectral power.
The average ERP is computed separately for each condition in `average_by`.
If `average_by` is `None`, the average ERP is computed across all epochs.

| Python examples | R examples |
| --------------- | ---------- |
| `False`         | `FALSE`    |
| `True`          | `TRUE`     |

### **`tfr_freqs` (optional, default: `np.linspace(4.0, 40.0, num=37)`)**

The frequencies for the family of [Morlet wavelets](https://neuroimage.usc.edu/brainstorm/Tutorials/TimeFrequency#Morlet_wavelets).
A larger number of frequencies will create smoother plots at the expense of taking longer to compute and needing more disk space.
Note that the time-frequency representation is computed on the *unfiltered* epochs so that frequencies larger than `lowpass_freq` are possible.

| Python examples                                         | R examples                                               |
| ------------------------------------------------------- | -------------------------------------------------------- |
| `np.linspace(4.0, 40.0, num=37)`                        | `seq(4.0, 40.0, length.out = 37)`                        |
| `np.arange(4.0, 41.0, step=1.)`                         | `seq(4.0, 40.0, by = 1)`                                 |
| `[8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0]` | `c(8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0)` |

### **`tfr_cycles` (optional, default: `np.linspace(2.0, 20.0, num=37)`)**

The number of cycles for the family of [Morlet wavelets](https://neuroimage.usc.edu/brainstorm/Tutorials/TimeFrequency#Morlet_wavelets).
These values will control the time-frequency tradeoff: More cycles offer better spectral resolution at the cost of worse temporal resolution.
Choosing cycles that increase in a linear fashion with `tfr_freqs` is recommended to keep the temporal resolution constant across frequencies.
Must have the same length as `tfr_freqs`.

| Python examples                                      | R examples                                           |
| ---------------------------------------------------- | ---------------------------------------------------- |
| `np.linspace(2.0, 20.0, num=37)`                     | `seq(2.0, 20.0, length.out = 37)`                    |
| `np.arange(2.0, 20.5, step=0.5)`                     | `seq(2.0, 20.0, by = 0.5)`                           |
| `[4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.]` | `c(4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20)` |

### **`tfr_mode` (optional, default: `'percent'`)**

The "baseline" correction method to adjust the time-frequency data for the $1/f$ scaling of the human EEG.
See the [MNE documentation](https://mne.tools/stable/generated/mne.time_frequency.EpochsTFR.html#mne.time_frequency.EpochsTFR.apply_baseline) for information about the possible methods.
Note that this method will be applied using the entire epoch as the "baseline" window.
This is because it was shown that using the pre-stimulus interval for single trial divisive baseline correction leads to positively biased post-stimulus power ([Grandchamp & Delorme, 2011](https://doi.org/10.3389/fpsyg.2011.00236)).
After applying this method, a second, *subtractive* baseline will be applied using the pre-stimulus interval only (defined via `tfr_baseline` below).
If `None`, no divisive "baseline" correction will be applied.

| Python examples | R examples    |
| --------------- | ------------- |
| `'percent'`     | `"percent"`   |
| `'ratio'`       | `"ratio"`     |
| `'logratio'`    | `"logratio"`  |
| `'zscore'`      | `"zscore"`    |
| `'zlogratio'`   | `"zlogratio"` |
| `None`          | `NULL`        |

### **`tfr_baseline` (optional, default: `(-0.45, -0.05)`)**

Time period (in s relative to stimulus onset) for baseline correction of the time-frequency data.
For each epoch and channel, the average power during this interval is subtracted from all time points in the epoch, so as to correct for shifts in power that had occured before stimulus onset.
It is a good idea to have the baseline period end *before* stimulus onset so that post-stimulus power at low frequencies doesn't get contaminated by pre-stimulus fluctuations.

| Python examples  | R examples        |
| ---------------- | ----------------- |
| `(-0.45, -0.05)` | `c(-0.45, -0.05)` |
| `(None, 0.0)`    | `c(NULL, 0.0)`    |
| `None`           | `NULL`            |

### **`tfr_components` (optional, default: no TFR components)**

Similar to `components` for ERPs, i.e., the time windows, frequency bands, and channels for the time-frequency bands of interest.
The structure is the same as for `components`, but adding new dict entries for the lower (`'fmin'`) and upper (`'fmax'`) bounds for the frequencies of interest (e.g., 8–13 Hz for alpha band activity).
Note that the term "component" is specific to ERPs and is used here solely to highlight the correspondence between the two options.

| Python example                                                                                              |
| ----------------------------------------------------------------------------------------------------------- |
| `{'name': ['alpha'], 'tmin': [0.05], 'tmax': [0.25], 'fmin': [8.0], 'fmax': [13.0], 'roi': [['PO9', ...]]}` |

| R example                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `list("name" = list("alpha"), "tmin" = list(0.05), "tmax" = list(0.25), "fmin" = list(8.0), "fmax" = list(13.0), "roi" = list(c("PO9", ...)))` |

## 7. Options for cluster-based permutation tests

### **`perm_contrasts` (optional, default: `None`)**

Contrasts between conditions to test using cluster-based permutation tests (CBPTs).
Must be one or multiple tuples, each containing exactly two condition labels.
Each condition label must correspond to one of the dictionary keys specified in `average_by` or, if `average_by=None`, to one of the EEG triggers specified in `triggers`.

| Python examples                | R examples                           |
| ------------------------------ | ------------------------------------ |
| `[('related', 'unrelated')]`   | `list(c("related", "unrelated"))`    |
| `[('neg_unrel'), ('neg_rel')]` | `list(c("neg_unrel"), c("neg_rel"))` |

### **`perm_tmin` (optional, default: `0.`)**

The starting time point (in s relative to stimulus onset) of the time window to consider for permutation testing.
If `None`, all time points from the beginning of the epoch (including the prestimulus intervall) are used.
Cropping the time window (based on *a priori* knowledge about plausible effects) can increase the sensitivity of the test.

| Python examples | R examples |
| --------------- | ---------- |
| `0.0`           | `0.0`      |
| `None`          | `NULL`     |

### **`perm_tmax` (optional, default: `1.`)**

The ending time point (in s relative to stimulus onset) of the time window to consider for permutation testing.
If `None`, all time points until the end of the epoch are used.
Cropping the time window (based on *a priori* knowledge about plausible effects) can increase the sensitivity of the test.

| Python examples | R examples |
| --------------- | ---------- |
| `1.0`           | `1.0`      |
| `None`          | `NULL`     |

### **`perm_channels` (optional, default: `None`)**

The channel labels to consider for permutation testing.
If `None`, all EEG channels are used.
Reducing the channels to a region of interest (based on *a priori* knowledge about plausible effects) can increase the sensitivity of the test.

| Python examples           | R examples                 |
| ------------------------- | -------------------------- |
| `None`                    | `NULL`                     |
| `['C1', 'Cz', 'C2', ...]` | `c("C1", "Cz", "C2", ...)` |

### **`perm_fmin` (optional, default: `None`)**

The lowest frequency (in Hz) of the time-frequency representation to consider for permutation testing.
Only relevent if `perform_tfr` is `True`.
If `None`, the lowest frequency in the data is used.
Cropping the frequency range (based on *a priori* knowledge about plausible effects) can increase the sensitivity of the test.

| Python examples | R examples |
| --------------- | ---------- |
| `None`          | `NULL`     |
| `8.0`           | `8.0`      |

### **`perm_fmax` (optional, default: `None`)**

The highest frequency (in Hz) of the time-frequency representation to consider for permutation testing.
Only relevent if `perform_tfr` is `True`.
If `None`, the highest frequency in the data is used.
Cropping the frequency range (based on *a priori* knowledge about plausible effects) can increase the sensitivity of the test.

| Python examples | R examples |
| --------------- | ---------- |
| `None`          | `NULL`     |
| `30.0`          | `30.0`     |

## 8. Performance options

### **`n_jobs` (optional, default: `1`)**

Number of jobs to run in parallel.
If `1`, participants will be processed sequentially.
If greater than `1`, multiple participants will be processed in parallel, thus reducing the overall runtime of the pipeline.
Negative values can be used to use all available cores (`-1`) or all but a certain number of available cores (e.g., `-2` = all but one core).
**This option is experimental and values other than `1` are currently not supported on Windows operating systems!**

| Python examples | R examples |
| --------------- | ---------- |
| `1`             | `1`        |
| `4`             | `4`        |
| `-2`            | `-2`       |
