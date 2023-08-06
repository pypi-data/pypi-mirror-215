import itertools

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from detection_utils import detect_peaks, cross_correlate
from graphic_utils import save_jpg
from pmf_algorithm import compute_poisson_sample, calculate_thresholds, calculate_poisson_pmf, compute_threshold
from simulation_utils import simulate_triangular_template
from utils import timer

# Config
plt.rcParams.update({'font.size': 18})
plt.rc('axes', grid=True)
plt.rc('grid', linestyle='-', color='gray')

SUBTRACT_NOISE = False
OUTPUT_DIRECTORY = "Completeness"
SIM_NUM = 1_000_000
NOISE_SIM_NUM = 10_000_000
TEMPLATE_LENGTH = 100
GAMMA = norm.sf(5)
NOISE = 0.5
FLUXES = np.arange(1, 6)  # np.logspace(np.log10(0.005), np.log10(2), num=10, endpoint=True)


def compare_completeness(template, noise, gamma, fluxes, sim_num, noise_sim_num, subtract_noise):
    # Compute thresholds
    simulated_noise_images = compute_poisson_sample(noise, len(template), subtract_noise, sim_num=noise_sim_num)
    f_th, s_th = calculate_thresholds(template, gamma, noise, simulated_noise_images, subtract_noise)
    pmf = calculate_poisson_pmf(noise, f_th, template)
    print(f"PMF: Fth={f_th} | Sth={s_th} | Bck={noise} | Template Length={len(template)} | Sigma={norm.isf(gamma)}")
    plt.plot(pmf / sum(pmf), ls="-", color="k", label="pmf")
    plt.plot(template / sum(template), ls="--", color="k", label="template")
    plt.legend()
    plt.title(f"PMF vs Original Template (Bck={noise}, Sigma={norm.isf(gamma):.5f})")
    save_jpg(f"compare_templates", OUTPUT_DIRECTORY)
    mf_noise_simulation = [sum(sample * template) for sample in simulated_noise_images]
    mf_th = compute_threshold(gamma, mf_noise_simulation)
    print(f"MF_th={mf_th}")
    # Completeness
    completeness = (compute_completeness(flux, mf_th, noise, pmf, s_th, sim_num, subtract_noise, template)
                    for flux in fluxes)
    mf_completeness, pmf_completeness = zip(*completeness)
    print(f"MF completeness: {mf_completeness}")
    print(f"PMF completeness: {pmf_completeness}")
    print(f"Fluxes: {fluxes}")
    plt.title(f"PMF vs Matched Filter Completeness (Bck={noise}, Sigma={norm.isf(gamma):.5f})")
    plt.plot(fluxes, mf_completeness, ls="--", marker=".", color="k", label=f"Normal Matched Filter")
    plt.plot(fluxes, pmf_completeness, ls="-", marker=".", color="k", label=f"Poisson Matched Filter")
    plt.xlabel("Flux")
    plt.ylabel("Completeness")
    plt.legend()
    save_jpg(f"compare_completeness", OUTPUT_DIRECTORY)


@timer
def compute_completeness(flux, mf_th, noise, pmf, s_th, sim_num, subtract_noise, template):
    simulated_flare = np.array(flux / max(template) * template)
    clean_signal = np.full(len(template) * 2, noise, dtype=float)
    flare_time = len(clean_signal) // 2
    clean_signal[flare_time - len(template) // 2:flare_time + int(np.ceil(len(template) / 2))] += simulated_flare
    _light_curves = [np.random.poisson(clean_signal) - noise if subtract_noise else np.random.poisson(clean_signal)
                     for _ in range(sim_num)]
    mf_lc, pmf_lc = itertools.tee(_light_curves)
    mf_successes = count_detections(mf_lc, template, mf_th)
    pmf_successes = count_detections(pmf_lc, pmf, s_th)
    print(f"Flux: {flux}, MF: {mf_successes / sim_num}, PMF: {pmf_successes / sim_num}")
    return mf_successes / sim_num, pmf_successes / sim_num


@timer
def count_detections(light_curves, template, threshold):
    cross_correlation = [cross_correlate(light_curve, template) for light_curve in light_curves]
    detections = [detect_peaks(cc, threshold, len(template)) for cc in cross_correlation]  # TODO make generator
    return sum(1 for i in detections if len(i) > 0)


@timer
def main():
    template = simulate_triangular_template(TEMPLATE_LENGTH)
    compare_completeness(template, NOISE, GAMMA, FLUXES, SIM_NUM, NOISE_SIM_NUM, SUBTRACT_NOISE)


if __name__ == "__main__":
    main()
