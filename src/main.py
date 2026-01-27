from matcher import gale_shapley
from utils import parse_pref, write_matchings, parse_matching, verify_matching

import sys

def main():
    try:
        match_or_verify = sys.argv[1]
        prefs_path = sys.argv[2]
    except:
        print("Usage: match <operation> <filepath>\nOR\nverify <prefs.in> <matching.out>")
        return

    if match_or_verify.lower() == "match":
        h_list, s_list = parse_pref(prefs_path)

        if h_list and s_list:
            matchings, num_offers = gale_shapley(h_list, s_list)
            output_path = write_matchings(prefs_path, matchings)
            print(f"Matching from Gale-Shapley Algorithm written to {output_path}!\nNumber of offers made: {num_offers}")
        else:
            print("No data written.")

    elif match_or_verify.lower() == "verify":
        try:
            matching_path = sys.argv[3]
        except:
            print("Usage: verify <prefs.in> <matching.out>")
            return

        h_list, s_list = parse_pref(prefs_path)
        if not (h_list and s_list):
            print("INVALID (could not parse preferences)")
            return

        matching = parse_matching(matching_path, len(h_list))

        if matching == "TOO_MANY_LINES":
            print(f"INVALID (expected {len(h_list)} matches, got more)")
            return

        if matching is None:
            print("INVALID (could not parse matching file)")
            return

        result = verify_matching(h_list, s_list, matching)
        print(result)

    else:
        print("Usage: <operation> <filepath>")
        print("Operation options are 'match' or 'verify'")
        return

if __name__ == "__main__":
    main()
