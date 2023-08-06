# TODO - test_should_detect(f_th, snr, peak_times, flare_times)

import pytest
from numpy.testing import assert_allclose

from simulation_utils import simulate_triangular_template

DETECTOR_GAMMA_SIGMA = 5
TESTED_LIGHT_CURVE_LENGTH = 6000
TESTED_PSF_LENGTH = 200
TESTED_BACKGROUND_NOISE = 5
SIMULATED_REGULAR_SOURCE_FLUX = 1400  # Should result in successful detections.
EXPECTED_F_TH_RANGE = (800, 1200)
SIMULATED_LOW_SOURCE_FLUX = 25  # Shouldn't be detected.
SIMULATED_TIME_LOCATIONS = (1000, 2400, 2600, 4000)


@pytest.fixture
def psf():
    return simulate_triangular_template(TESTED_PSF_LENGTH)


@pytest.fixture
def light_curve(psf):
    return simulate_light_curve(length=TESTED_LIGHT_CURVE_LENGTH,
                                psf_flux=SIMULATED_REGULAR_SOURCE_FLUX,
                                background_noise=TESTED_BACKGROUND_NOISE,
                                locations=SIMULATED_TIME_LOCATIONS,
                                normalized_template=psf)


@pytest.fixture
def light_curve_low_source_flux(psf):
    return simulate_light_curve(length=TESTED_LIGHT_CURVE_LENGTH,
                                psf_flux=SIMULATED_LOW_SOURCE_FLUX,
                                background_noise=TESTED_BACKGROUND_NOISE,
                                locations=SIMULATED_TIME_LOCATIONS,
                                normalized_template=psf)


@pytest.fixture
def detector():
    return PoissonMatchedFilterDetector(gamma_sigma=DETECTOR_GAMMA_SIGMA)


def test_run_detection_simulated_flux_higher_than_threshold(detector, light_curve, psf):
    detections = detector.run_detection(light_curve, psf)
    assert len(detections) == len(SIMULATED_TIME_LOCATIONS)
    for detection in detections:
        assert pytest.approx(detection, 0.01 * detection) in SIMULATED_TIME_LOCATIONS


def test_run_detection_simulated_flux_lower_than_threshold(detector, light_curve_low_source_flux, psf):
    # Shouldn't result in any detections, since the light curve is too noisy in comparison to the flux.
    detections = detector.run_detection(light_curve_low_source_flux, psf)
    assert len(detections) == 0


def test_calculate_poisson_flux_threshold(detector, light_curve, psf, monkeypatch):
    f_th = detector._calculate_poisson_flux_threshold(light_curve, psf)
    assert EXPECTED_F_TH_RANGE[0] <= f_th <= EXPECTED_F_TH_RANGE[1]


@pytest.mark.parametrize("const_psf,background_noise,flux", ((Graph(list(range(10))), 5, 100),))
def test_calculate_poisson_pmf(detector, const_psf, background_noise, flux):
    pmf = detector._calculate_poisson_pmf(background_noise, flux, const_psf)
    assert_allclose(pmf, [0.0, 3.044522437723423, 3.713572066704308, 4.110873864173311, 4.394449154672439,
                          4.61512051684126, 4.795790545596741, 4.948759890378168, 5.081404364984463,
                          5.198497031265826])


@pytest.mark.parametrize("background_noise,expected", ((100, 2), (1500, 5)))
def test_get_f_th_guess_value(detector, psf, background_noise, expected):
    assert detector._get_f_th_guess_value(background_noise, psf) == expected


def test_get_f_th_guess_default_value(detector, psf):
    assert detector._get_f_th_guess_value(0, psf) == PoissonMatchedFilterDetector.DEFAULT_F_TH_INITIAL
