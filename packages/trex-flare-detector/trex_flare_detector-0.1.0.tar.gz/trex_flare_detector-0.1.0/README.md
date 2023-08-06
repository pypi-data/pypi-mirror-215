# T-Rex Flare Detector

The `trex_flare_detector` Python package is a tool for detecting flares within light curves. It utilizes the Poisson Matched Filtering (PMF) algorithm to match a flaring template with a given light curve.

## Credits

This development is based on the T-Rex algorithm by Maayane Soumagnac, which is described in detail in [Soumagnac & al. in preparation](https://www.overleaf.com/read/tmvqvzvzgtrc).

The T-Rex source detection tool is provided here: https://github.com/maayane/T-Rex/tree/main.

The underlying Poisson Matched Filter (PMF) algorithm is based on the work of [Ofek & Zackay 2018](https://ui.adsabs.harvard.edu/abs/2018AJ....155..169O/abstract).

## Requirements

To run the flare detector, the following dependencies need to be installed:

* numpy
* scipy
* pandas
* matplotlib

# How to Run the Flare Detector?

The T-Rex Flare Detector provides a Python tool that locates a template (representing a flare in the time domain) within a given light curve.

To run a simple flare detection example, follow these steps:

1. Load an input light curve from a file:
    ```python
    light_curve = np.load(params.INPUT_LIGHT_CURVE_FILE)  # Load the input light curve.
    ```
    The input file `f"DATA/light_curve_example.npy"` was pre-generated using the `generate_example_input_file.py` script, located under the `examples` directory.
2. Generate a template of a flare of type FRSD (fast-rise-slow-decay):
    ```python
    flare_template = simulate_frsd_template(bin_count=params.TEMPLATE_LENGTH)  # Generate a "fast rise slow decay" template.
    ```
    Both the light curve and the templates are represented as 1D numpy arrays.
3. Estimate the background noise for the PMF detection algorithm:
    ```python
    background_noise = estimate_background_noise(light_curve,
                                                 chunks_number=params.NOISE_ESTIMATION_CHUNKS_NUMBER,
                                                 output=params.OUTPUT_DIRECTORY,
                                                 bins_number=params.NOISE_ESTIMATION_BINS_NUMBER)
    ```
   * The `chunks_number` parameter determines the number of chunks used in the background estimation process.
   * If the `output` parameter is provided (not `None`), a visualization plot of the background estimation process will be created, and the `output` parameter will set the subdirectory of the plotted image.
   * The `bins_number` parameter sets the number of bins in the output image histogram.
   In this example, the file `background-noise-estimation.pdf` will appear under `"OUTPUT\Example"`:
   ![](examples/OUTPUT/Example/background-noise-estimation.jpg)
4. Run the PMF flare detection algorithm using the `pmf_detect` function:
    ```python
    detections = pmf_detect(light_curve, flare_template, background_noise,
                            sigma=params.SIGMA, output=params.OUTPUT_DIRECTORY)
    ```
    A visualization of the detection will be saved as `examples/OUTPUT/Example/flare-detection.pdf`:
    ![](examples/OUTPUT/Example/flare-detection.jpg)

The complete example is provided in `example.py` located in the `"examples"` subdirectory:

```python
# example.py
import numpy as np

import params
from background_noise_estimation import estimate_background_noise
from pmf_algorithm import pmf_detect
from template_generation import simulate_frsd_template


def main():
    # Load input light curve.
    light_curve = np.load(params.INPUT_LIGHT_CURVE_FILE)
    # Generate "fast rise slow decay" template.
    flare_template = simulate_frsd_template(bin_count=params.TEMPLATE_LENGTH)
    # Estimate the background noise.
    background_noise = estimate_background_noise(light_curve,
                                                 chunks_number=params.NOISE_ESTIMATION_CHUNKS_NUMBER,
                                                 output=params.OUTPUT_DIRECTORY,
                                                 bins_number=params.NOISE_ESTIMATION_BINS_NUMBER)
    # Run the flare detection using the PMF algorithm.
    detections = pmf_detect(light_curve, flare_template, background_noise, sigma=params.SIGMA,
                            output=params.OUTPUT_DIRECTORY)
    print(f"The flare detection times are: {detections}")


if __name__ == "__main__":
    main()
```

In this script, the configuration parameters are defined in `params.py` (which you can edit):

```python
# params.py
SIGMA = 5  # The false alarm in units of Gaussian STDs.
OUTPUT_DIRECTORY = "Example"
INPUT_LIGHT_CURVE_FILE = f"DATA/light_curve_example.npy"
TEMPLATE_LENGTH = 50
NOISE_ESTIMATION_CHUNKS_NUMBER = 10
NOISE_ESTIMATION_BINS_NUMBER = 8
```

If you do not pass the `output=params.OUTPUT_DIRECTORY` argument to the PMF functions, the images won't be produced. Additionally, note that the root `"OUTPUT"` directory is created internally, while the subdirectory `"Example"` is created for each run.

A similar example is provided in the flare detection script, located in the "scripts" folder (explained below).

The `pmf_algorithm.py` file provides the inner functions used to run each step separately:

* `calculate_thresholds`: Computes Fth & Sth as described by Ofek & Zackay.
* `calculate_poisson_pmf`: Implements the PMF formula.
* `compute_poisson_sample`: Generates noise simulations. It is important to note that the background noise is estimated separately from the PMF algorithm, as the background noise estimation and the matched filtering processes are independent.

## How does it work?

The PMF algorithm functions similarly to regular matched filtering but uses the formula `PMF = ln(1 + F/B * Template)`, where `Template` is the same one used in normal matched filtering, `B` is the estimated background noise, and `F` is the total sum of photon flux of the detected flare.

The estimation of `B` is shown in the example above. Since `F` is unknown, Ofek & Zackay introduce an additional condition on `F`, referred to as `Fth`, to determine the value of `F` to be used. This condition utilizes a quantity called `Sf` (refer to their paper).

The computation of `Fth` depends on `sigma` (the false-alarm threshold) and the detection threshold `Sth`. Both `Sth` and `Fth` are computed simultaneously through an iterative process.

The steps of the PMF algorithm are as follows:

1. Estimate the background noise `B` and choose a desired false-alarm threshold `sigma`.
2. Choose an initial value for `Fth` and start an iterative process:
    1. Compute the null hypothesis log-likelihood distribution `Ssim` through simulations.
    2. Use `Ssim` and `sigma` to evaluate `Sth`.
    3. Repeat the computation of `Sth` iteratively while computing `Fth` until the relation between `Sth` and `Fth` satisfies the `Sf` condition.
       At this point, `Sth` and `Fth` are computed.

   It is important to note that these values are determined based on `B`, `sigma`, and the `template`,
   rather than the light curve data itself. Therefore, light curves with similar background noise can use the same results.
3. Use the computed `Fth` to compute the Poisson Matched Filter (PMF).
4. Perform cross-correlation between the PMF and the desired light curves, and identify peaks that exceed the detection threshold `Sth`.

## File Structure

The repository contains several python files used for the detection:

* `backgraound_noise_estimation.py`: Provides a simple method to evaluate the background noise of the light curve. You may need to use a different method depending on your specific requirements.
* `pmf_algorithm.py`: Implements the PMF algorithm for calculating thresholds and filters.
* `detection_utils.py`: Contains generic detection functionalities that are agnostic to the PMF method, such as `cross_correlate`, `detect_peaks`, and `compute_threshold`.
* `tempalte_generation.py`: Enables the generation of templates to be used as input in the detection process, including triangular, Gaussian, and FRSD templates.
* `graphics_utils.py`: Provides generic plotting utilities.
* `utils.py`: Contains utility functions, such as a `@timer` decorator.

Additionally, there is a directory named `"scripts"` that contains different scripts used to test the algorithm and its underlying concepts. Each of these scripts imports functions from the main code files and includes dedicated simulations and important plots relevant to the flare detector research project.

## Notes

The pytest tests folder in this version is currently outdated. To run the tests, pytest must be additionally installed.