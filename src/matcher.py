def gale_shapley(h_list, s_list):
    # Source for help determining efficient data structures in Python: https://www.pythonmorsels.com/time-complexities/
    unmatched_hospitals = [len(h_list) - i - 1 for i in range(len(h_list))]
    hospital_pref_index = [0] * len(h_list)
    applicant_matched = [-1] * len(h_list)
    num_offers = 0
    while len(unmatched_hospitals) > 0:
        hospital = unmatched_hospitals[-1]
        h_pref_list = h_list[hospital]
        applicant_index = hospital_pref_index[hospital]
        applicant = h_pref_list[applicant_index]
        current_a_match = applicant_matched[applicant]
        if current_a_match == -1:
            unmatched_hospitals.pop()
            applicant_matched[applicant] = hospital
        # We need to look up the the rankings of the hospitals for the applicant, so we should use a different data structure from an array. 
        # This is because we want to avoid using .index() to look up rankings, which has O(n) complexity
        # If we instead use a dict, lookups by index (key) have constant time complexity.
        # For fast lookup of rankings by hospitals, we need a dictionary with hospitals as keys and student rankings as values. 
        # Data structure is implemented in utils.py
        # Inspiration for using this data structure: 
        # https://towardsdatascience.com/faster-lookups-in-python-1d7503e9cd38/#:~:text=You%20have%20to%20go%20through,Useful%20Links
        elif s_list[applicant][hospital] < s_list[applicant][current_a_match]:
            applicant_matched[applicant] = hospital
            unmatched_hospitals.pop()
            unmatched_hospitals.append(current_a_match)
        # We need hospital preference index to increase each time even if a hospital is not rejected,
        # because if a hospital becomes unmatched, the next student they look at should be
        # after the one they were previously matched to, so they don't double propose.
        hospital_pref_index[hospital] += 1
        num_offers += 1
    # Help with sorting a dict: https://www.freecodecamp.org/news/python-sort-dictionary-by-key/
    final_matchings = dict(sorted({applicant_matched[i] : i for i in range(len(applicant_matched))}.items()))
    return final_matchings, num_offers