import random
from os import listdir
from os.path import isfile, join
from matcher import *
from utils import *
from pathlib import Path
import re
import time
import matplotlib.pyplot as plt


N_LIST = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512)

def generate_pref_list(n):
    """Generates a file of preference lists for n hospitals and n students."""
    vals = range(1, n+1)
    pref_list = []
    for i in range(n*2):
        pref_list.append(random.sample(vals, n))
    with open(f"tests/pref_lists/prefs_{n}.in", "w") as file:
        file.write(str(n) + "\n")
        for prefs in pref_list:
            prefs = [str(pref) for pref in prefs]
            file.write(" ".join(prefs) + "\n")

def generate_all(n_list):
    """Generates a file of preference lists for each number of hospitals and students (n) in a provided list."""
    for n in n_list:
        generate_pref_list(n)

def run_matcher_and_verifier(dir_path):
    """Runs the timing experiment on the matcher and verifier for each generated list
    Assumption: Timing includes file i/o operations required for each operation."""
    # Source - https://stackoverflow.com/a/3207973
    # Posted by pycruft, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-01-29, License - CC BY-SA 4.0
    matching_runtimes = {}
    verifier_runtimes = {}
    only_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for file in only_files:
        # Run all matching steps first (Assumption: running time includes file i/o)
        # Source for time module info: https://sentry.io/answers/measure-elapsed-time-in-python/
        start = time.perf_counter()

        h_list, s_list = parse_pref(file)

        if h_list and s_list:
            # Source for help with pathlib: https://www.pythonmorsels.com/pathlib-module/
            matchings, num_offers = gale_shapley(h_list, s_list)
            output_path = write_matchings(str(Path(file)), matchings, f"tests/matchings/{str(Path(file).stem)}.out")
            print(f"Matching from Gale-Shapley Algorithm written to {output_path}!\nNumber of offers made: {num_offers}")
        else:
            print("No data written.")

        end = time.perf_counter()
        matching_runtimes[len(h_list)] = (end - start) * 1000 # elapsed time in milliseconds

        # Run all verification steps second (Assumption: running time includes file i/o)
        # Redundancy is intentional to measure true running time of verifier
        start = time.perf_counter()

        h_list, s_list = parse_pref(file)
        if not (h_list and s_list):
            print("INVALID (could not parse preferences)")
            return
        # Source: https://www.geeksforgeeks.org/python/python-program-to-get-the-file-name-from-the-file-path/
        matching = parse_matching(f"tests/matchings/{str(Path(file).stem)}.out", len(h_list))

        if matching == "TOO_MANY_LINES":
            print(f"INVALID (expected {len(h_list)} matches, got more)")
            return

        if matching is None:
            print("INVALID (could not parse matching file)")
            return
        
        result = verify_matching(h_list, s_list, matching)
        print(result)

        end = time.perf_counter()
        verifier_runtimes[len(h_list)] = (end - start) * 1000  # elapsed time in milliseconds
    # Source for help sorting dictionary by key: https://www.geeksforgeeks.org/python/python-sort-python-dictionaries-by-key-or-value/
    matching_runtimes = {k: v for k, v in sorted(matching_runtimes.items(), key=lambda item: item[0])}
    verifier_runtimes = {k: v for k, v in sorted(verifier_runtimes.items(), key=lambda item: item[0])}
    return matching_runtimes, verifier_runtimes

def plot_runtimes(matching_runtimes, verifier_runtimes):
    # Source for help with matplotlib line charts: https://www.geeksforgeeks.org/python/line-chart-in-matplotlib-python/
    """Plots matching/verifying runtime versus number of hospitals and students for each hospital."""
    plt.figure()
    x1 = list(matching_runtimes.keys())
    y1 = list(matching_runtimes.values())

    x2 = list(verifier_runtimes.keys())
    y2 = list(verifier_runtimes.values())

    plt.plot(x1, y1, label='Matching Engine')
    plt.plot(x2, y2, label='Verifier')

    plt.xlabel("Number of Hospitals/Students")
    plt.ylabel("Runtime (ms)")
    plt.title("Runtime of Matching and Verifying v.s. Number of Hospitals/Students")
    # Source: https://stackoverflow.com/questions/23238041/move-and-resize-legends-box-in-matplotlib
    plt.legend(loc = "lower right")
    plt.savefig("tests/plot.png")
    plt.show()
    

def run_tests():
    """Runs the full experiment for Part C."""
    generate_all(N_LIST)
    matching_runtimes, verifier_runtimes = run_matcher_and_verifier("tests/pref_lists")
    plot_runtimes(matching_runtimes, verifier_runtimes)
    