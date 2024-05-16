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


def test_io_intensive_threads(addrs):
    print(" launching base io")
    num_tasks = len(addrs)
    for i in range(num_tasks):
        io_intensive(addrs[i])
    print(" launching multithreading: 2 io")
    multithreading(io_intensive, addrs, 2)
    print(" launching multithreading: 4 io")
    multithreading(io_intensive, addrs, 4)
    # multithreading(io_intensive, addrs, 8)


def compute_intensive(x):
    return x * math.cos(x*math.pi)

def test_compute_intensive():
    print(" launching base cpu")
    for i in range(10**3):
        compute_intensive(i)
    print(" launching multithreading:2 cpu")
    multithreading(compute_intensive, range(10**3), 2)
    print(" launching multiprocessing:2 cpu")
    multiprocessing(compute_intensive, range(10**3), 2)
    # multiprocessing(compute_intensive, range(10**7), 4)
    # multiprocessing(compute_intensive, range(10**7), 8)
    return

def main_io():
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
    test_io_intensive_threads(addrs)


def main_cpu():
    test_compute_intensive()

if __name__ == "__main__":
    # print("launching io")
    # main_io()
    print("launching cpu")
    main_cpu()
