# An example program to profile
import numpy as np
from codecarbon import OfflineEmissionsTracker


def test_me_best():
    x = np.arange(10**7)
    y = np.random.uniform(0, 100, size=(10**8))


def test_me_worse():
    x = np.array(range(10**7))
    y = np.array(np.random.uniform(0, 100, size=(10**8)))


def test_me_middle():
    x = np.array(range(10**7))
    y = np.random.uniform(0, 100, size=(10**8))


def utils_test_with_codecarbon(func):
    """Utility function to run test and print CodeCarbon metrics."""
    from codecarbon.external.logger import logger
    logger.disabled = True

    with OfflineEmissionsTracker() as tracker:
        for _ in range(5):
            func()
    print("Scenario:", func.__name__)
    print(f"Energy consumption: {tracker.final_emissions_data.energy_consumed * 1e6:.2f} mWh")
    print(f" - cpu: {tracker.final_emissions_data.cpu_energy * 1e6:.2f} mWh")
    print(f" - ram: {tracker.final_emissions_data.ram_energy * 1e6:.2f} mWh")
    print(f"GHG Emissions: {tracker.final_emissions_data.emissions * 1e6:.2f} mgCO2eq\n")


if __name__ == "__main__":
    # Testing with Scalene
    test_me_best()
    # test_me_worse()
    # test_me_middle()

    # Testing with CodeCarbon
    # utils_test_with_codecarbon(test_me_best)
    # utils_test_with_codecarbon(test_me_worse)
