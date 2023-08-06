import pytest

from background_noise_estimation import estimate_background_noise
from simulation_utils import simulate_triangular_template, simulate_light_curve

# These are constant for all test, therefor saved as constants and not as fixtures.
TESTED_PSF_LENGTH = 20
TESTED_LIGHT_CURVE_LENGTH = TESTED_PSF_LENGTH * 10
_RELATIVE_FLARE_TIMES = (0.3, 0.6)
FLARE_TIMES = tuple([int(t * TESTED_LIGHT_CURVE_LENGTH) for t in _RELATIVE_FLARE_TIMES])
assert all(
    TESTED_PSF_LENGTH <= t <= TESTED_LIGHT_CURVE_LENGTH - TESTED_PSF_LENGTH for t in FLARE_TIMES)  # Assure valid times.

SIMULATED_BACKGROUND_NOISES = (1, 5, 10)
SNR = (1.1, 1.5, 2)

SUBTRACT_NOISE = False


@pytest.fixture(params=SIMULATED_BACKGROUND_NOISES)
def background_noise(request):
    return request.param


@pytest.fixture(params=SNR)
def snr(request):
    return request.param


@pytest.fixture
def psf():
    return simulate_triangular_template(TESTED_PSF_LENGTH)


@pytest.fixture
def light_curve_simulation(psf, background_noise, snr):
    return simulate_light_curve(TESTED_LIGHT_CURVE_LENGTH, psf, FLARE_TIMES, background_noise,
                                snr, SUBTRACT_NOISE)


def test_background_noise_estimation(light_curve_simulation, background_noise):
    assert estimate_background_noise(light_curve_simulation) == pytest.approx(background_noise, rel=0.1,
                                                                              abs=0.5)
