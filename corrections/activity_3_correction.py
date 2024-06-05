import math
import urllib.request
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def io_intensive(url):
    write_count = 50
    with urllib.request.urlopen(url, timeout=20) as conn:
        page = conn.read()
        for _ in range(write_count):
            with open("output.txt", "w") as output:
                output.write(str(page))


def test_io_intensive_threads(addrs, n_threads):
    print(f" launching multithreading: {n_threads} io")
    multithreading(io_intensive, addrs, n_threads)


def compute_intensive(x):
    return x * math.cos(x*math.pi)

def test_compute_intensive(n_workers: int=1):
    print(f"launching multiprocessing with {n_workers} workers.")
    multiprocessing(compute_intensive, range(10**3), n_workers)
    return

def main_io(n_threads: int=1):
    addrs = [
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://www.google.com/",
        "https://www.kaggle.com/competitions",
        "https://www.amazon.com/charts/mostread/fiction/",
        "https://www.amazon.com/charts/mostread/nonfiction",
        "https://www.amazon.com/charts/mostsold/nonfiction",
        "https://www.amazon.com/charts/mostsold/fiction",
        "https://www.nytimes.com",
        "https://www.bbc.com/",
        "https://www.lemonde.fr",
        "https://edition.cnn.com",
    ]
    test_io_intensive_threads(addrs, n_threads)


def main_cpu():
    test_compute_intensive(n_workers=1)

if __name__ == "__main__":
    # print("launching io")
    # main_io(n_threads=4)
    print("launching cpu")
    main_cpu(n_workers=4)