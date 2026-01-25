from matcher import gale_shapley
from utils import parse_pref, write_matchings

# This is the main command line interface for the program.
import sys
def main():
    # First argument must be match or verify
    # Second argument must be a filename
    try:
        match_or_verify = sys.argv[1]
        filepath = sys.argv[2]
    except:
        print("Usage: <operation> <filepath>")
        print("Operation options are 'match' or 'verify'")
        return
    if match_or_verify.lower() == "match":
        h_list, s_list = parse_pref(filepath)
        # print(h_list)
        # print(s_list)
        if h_list and s_list:
            matchings, num_offers = gale_shapley(h_list, s_list)
            output_path = write_matchings(filepath, matchings)
            print(f"Matching from Gale-Shapley Algorithm written to {output_path}!\nNumber of offers made: {num_offers}")
        # print(matchings)
        else:
            print("No data written.")
    elif match_or_verify.lower() == "verify":
        pass
    else:
        print("Usage: <operation> <filepath>")
        print("Operation options are 'match' or 'verify'")
        return

if __name__ == "__main__":
    main()