from codecarbon import OfflineEmissionsTracker

def utils_test_with_codecarbon(func):
    """Utility function to run test and print CodeCarbon metrics."""
    from codecarbon.external.logger import logger
    logger.disabled = True

    with OfflineEmissionsTracker() as tracker:
        func()

def main():
    pass

if __name__ == "__main__":
    main()