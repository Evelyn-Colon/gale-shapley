# gale-shapley
Programming Assignment 1: Gale-Shapley Algorithm

This project implements the Gale-Shapley algorithm for the hospital-student stable matching problem, along with a verifier that checks whether a proposed matching is valid and stable.

## Team
1. Evelyn Colon, UFID: 46048391
2. Imaan Edhi, UFID: 28443010

## Project Structure
matcher.py # Gale-Shapley matching engine
utils.py # Parsing and verification logic
main.py # Command-line interface
analysis.py # Part C scalability testing

examples/
example1.in
example1.out
example2.in
example2.out
example3.in
example3.out
example4.in
example5.out
invalid_duplicate_hospital.out
invalid_duplicate_student.out
invalid_example.out
invalid_missing_hospital.out
invalid_out_of_range.out

tests/
pref_lists/ # Generated preference files for Part C
matchings/ # Output matchings for Part C
plot.png # Runtime graph

## Requirements
- Python 3.8 or higher  
- matplotlib (only required for Part C)

To install matplotlib:

```bash
pip3 install matplotlib

On macOS (if pip is blocked):

brew install python-matplotlib

## How to Run
Run the Matching Algorithm (Task A)
python3 src/main.py match examples/example1.in

This generates:
examples/example1.out


Run the Verifier (Task B)
python3 src/main.py verify examples/example1.in examples/example1.out


Possible outputs:

VALID STABLE

INVALID (with reason)

UNSTABLE (with blocking pair)

Example invalid test:

python3 src/main.py verify examples/example1.in examples/invalid_duplicate_student.out


Part C: Scalability Testing

To run the scalability experiment and generate the graph:

python3 src/analysis.py


This:

Runs both the matcher and verifier on increasing values of n

Measures runtime for each

Produces a line graph saved as: tests/plot.png

## Assumptions

Input format:

n
hospital preference lists
student preference lists


Rankings are strict permutations of 1..n

File I/O time is included in runtime measurements

Matcher and verifier are tested on the same generated inputs

## Part C Analysis (Conclusion)
From the generated graph, we observe:

The matching algorithm grows approximately O(n²), which matches the theoretical time complexity of the Gale-Shapley algorithm.

The verifier shows similar quadratic growth since it must check all possible blocking pairs.

Both implementations scale predictably and perform efficiently for moderate input sizes up to n = 512.

These results confirm the expected theoretical behavior.

![Runtime Graph](tests/plot.png)
