import re

def parse_pref(filepath):
    # Source for help with Python file i/o: https://www.geeksforgeeks.org/python/how-to-read-from-a-file-in-python/
    try:
        with open(filepath, 'r') as file:
            line = file.readline()
            h_list = []
            s_list = []
            if line:
                n = int(line)
            else:
                raise ValueError("File is empty!")
            for i in range(n):
                h_data = file.readline()
                if not h_data:
                    raise ValueError(f"There are fewer than {n} hospitals in the file!")
                h_list_small = h_data.split()
                if len(h_list_small) != n:
                    raise ValueError(f"Number of student preferences != {n}!")
                h_list_small = [int(j) - 1 for j in h_list_small]
                h_list.append(h_list_small)
            for i in range(n):
                s_data = file.readline()
                if not s_data:
                    raise ValueError(f"There are fewer than {n} students in the file!")
                s_list_small = s_data.split()
                if len(s_list_small) != n:
                    raise ValueError(f"Number of hospital preferences != {n}!")
                # We need a dictionary for the student preferences because we need fast lookup in the Gale-Shapley algorithm.
                s_dict = {int(s_list_small[j]) - 1 : j for j in range(len(s_list_small))}
                s_list.append(s_dict)
            return h_list, s_list
    except FileNotFoundError:
        print("File not found!")
    except ValueError as e:
        print(e)
    return ([], [])

def write_matchings(filepath, matchings):
    # Help with regex syntax: https://www.w3schools.com/python/python_regex.asp
    # Help with capturing groups: 
    # https://stackoverflow.com/questions/10059673/named-regular-expression-group-pgroup-nameregexp-what-does-p-stand-for
    name_match = re.search("(?P<path>.*\/)?(?P<name>[^\.]*)(\..*)?", filepath)
    output_full_path = "data/matchings.out"
    if name_match is not None:
        output_full_path = name_match.group("path") + name_match.group("name") + ".out"
    with open(f"{output_full_path}", 'w') as file:
        for hospital, student in matchings.items():
            file.write(f"{hospital + 1} {student + 1}\n")
    return output_full_path

def parse_matching(filepath):
    # Reads a matching output file with lines like:
    # 1 2
    # 2 3
    # 3 1
    # Returns dict {hospital_index: student_index} using 0-based indices.
    try:
        matching = {}
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    return None
                h = int(parts[0]) - 1
                s = int(parts[1]) - 1
                matching[h] = s
        return matching
    except:
        return None


def verify_matching(h_list, s_list, matching):
    # Checks:
      # (a) validity: perfect matching, no duplicates, in range
      # (b) stability: no blocking pairs

    # Returns a string:
      # "VALID STABLE" or "INVALID (...)" or "UNSTABLE (...)"
    n = len(h_list)

    if len(matching) > n:
        return "INVALID (too many hospitals in matching)"

    seen_students = set()
    for h in range(n):
        if h not in matching:
            return f"INVALID (hospital {h+1} missing from matching)"

        s = matching[h]

        if not (0 <= s < n):
            return f"INVALID (hospital {h+1} matched to out-of-range student {s+1})"

        if s in seen_students:
            return f"INVALID (student {s+1} matched more than once)"

        seen_students.add(s)

    # build reverse map student -> hospital
    student_to_hospital = [-1] * n
    for h, s in matching.items():
        student_to_hospital[s] = h

    if any(h == -1 for h in student_to_hospital):
        return "INVALID (some student is unmatched)"

    # Stability 
    # blocking pair (h, s):
    # hospital h prefers s over its current match
    # student s prefers h over their current match
    for h in range(n):
        current_s = matching[h]

        # scan hospital preference list until we hit current match
        for s in h_list[h]:
            if s == current_s:
                break

            current_h_of_s = student_to_hospital[s]
            if s_list[s][h] < s_list[s][current_h_of_s]:
                return f"UNSTABLE (blocking pair: hospital {h+1}, student {s+1})"

    return "VALID STABLE"

