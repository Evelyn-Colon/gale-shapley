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