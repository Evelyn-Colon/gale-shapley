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
                h_list_small = [int(j) for j in h_list_small]
                h_list.append(h_list_small)
            for i in range(n):
                s_data = file.readline()
                if not s_data:
                    raise ValueError(f"There are fewer than {n} students in the file!")
                s_list_small = s_data.split()
                s_list_small = [int(j) for j in s_list_small]
                s_list.append(s_list_small)
            return h_list, s_list
    except FileNotFoundError:
        print("File not found!")
    except ValueError as e:
        print(e)
    return ([], [])