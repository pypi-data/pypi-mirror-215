import concurrent.futures

import numpy as np
import pytest
from scipy.stats import norm

from pmf_algorithm import pmf_detect
from simulation_utils import simulate_triangular_template, simulate_light_curve
from utils import timer

# Input consts.
PSF_LENGTH = 10
LC_LENGTH = PSF_LENGTH * 5
_RELATIVE_FLARE_TIMES = (0.5,)
FLARE_TIMES = tuple([int(t * LC_LENGTH) for t in _RELATIVE_FLARE_TIMES])
assert all(PSF_LENGTH <= t <= LC_LENGTH - PSF_LENGTH for t in FLARE_TIMES)  # Assure valid times.

SUBTRACT_NOISE = False
BACKGROUND_NOISES = (0.5,)  # (0.5, 5, 10)
SIMULATED_FLUX = (5,)  # (5, 10, 100)
GAMMA_STD = (3,)  # (3, 4.5, 4)

RUNS_COUNT = 100_000  # Change to 1M runs


@pytest.fixture
def psf():
    return simulate_triangular_template(PSF_LENGTH)


@pytest.fixture(params=BACKGROUND_NOISES)
def background_noise(request):
    return request.param


@pytest.fixture(params=SIMULATED_FLUX)
def flux(request):
    return request.param


@pytest.fixture
def light_curve(psf, background_noise, flux):
    snr = flux / background_noise
    return simulate_light_curve(LC_LENGTH, psf, FLARE_TIMES, background_noise, snr, SUBTRACT_NOISE)


@pytest.fixture(params=GAMMA_STD)
def gamma_std(request):
    return request.param


@timer
def test_false_alarm(psf, light_curve, background_noise, gamma_std, runs_count=RUNS_COUNT):
    gamma = norm.sf(gamma_std)
    false_alarm_count = 0
    for i in range(runs_count):
        detections = pmf_detect(light_curve, psf, background_noise, gamma_std, SUBTRACT_NOISE)
        false_alarm_count += _count_false_alarms(detections, FLARE_TIMES)
    false_alarm_percentile = false_alarm_count / runs_count
    print(f"Gamma: {gamma:.3f} | Computed False Alarm: {false_alarm_percentile:.3f} | B={background_noise}")
    assert gamma == pytest.approx(false_alarm_percentile, rel=1e-3)


@timer
def test_false_alarm(psf, light_curve, background_noise, gamma_std, runs_count=RUNS_COUNT):
    gamma = norm.sf(gamma_std)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        false_alarm_counts = [executor.submit(pmf_detect, light_curve, psf, background_noise, gamma_std, SUBTRACT_NOISE) for
                              _ in range(runs_count)]
        results = [f.result() for f in false_alarm_counts]
    detections, false_alarm = zip(*results)
    false_alarm_rate = np.mean(detections) / np.mean(false_alarm)
    print(f"Gamma: {gamma:.3f} | Computed False Alarm: {false_alarm_rate:.3f} | B={background_noise}")
    assert gamma == pytest.approx(false_alarm_rate, rel=1e-3)


def _count_false_alarms(detection_times, simulation_times):
    false_alarm = [detection for detection in detection_times if
                   pytest.approx(detection, 0.01 * detection) not in simulation_times]
    correct_detections = [detection for detection in detection_times if
                          pytest.approx(detection, 0.01 * detection) not in simulation_times]
    return len(correct_detections), len(false_alarm)


# @timer
# def find_y_with_gamma(B: float, a: List[float], gamma: float, epsilon: float = 1e-8) -> float:
#     lower_limit, upper_limit = 0, int(100 * B * len(a))
#     middle_point = (lower_limit + upper_limit) / 2
#     i = 0
#     while upper_limit - lower_limit > epsilon:
#         print(i)
#         cdf = sum(poisson.pmf(middle_point - k, B) * a[k] for k in range(middle_point + 1))
#         lower_limit, upper_limit = (middle_point, upper_limit) if cdf < 1 - gamma else (lower_limit, middle_point)
#         middle_point = (lower_limit + upper_limit) / 2
#         i += 1
#     return middle_point
