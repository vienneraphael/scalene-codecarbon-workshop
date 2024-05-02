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

if __name__ == "__main__":
    with OfflineEmissionsTracker(country_iso_code="FRA") as tracker:
        test_me_best()