def gale_shapley(h_list, s_list):
    # Source for help determining efficient data structures in Python: https://www.pythonmorsels.com/time-complexities/
    unmatched_hospitals = [len(h_list) - i - 1 for i in range(len(h_list))]
    # print(f"Unmatched Hospitals: {unmatched_hospitals}")
    applicant_matched = [-1] * len(h_list)
    # print(f"Applicant Matched: {applicant_matched}")
    while len(unmatched_hospitals) > 0:
        hospital = unmatched_hospitals[-1]
        # print(f"Current Unmatched Hospital: {hospital}")
        # print(f"Applicant Matched: {applicant_matched}")
        h_pref_list = h_list[hospital]
        # print(f"Current Hospital Preference List: {h_pref_list}")
        for applicant in h_pref_list:
            # print(f"Current Applicant: {applicant}")
            current_a_match = applicant_matched[applicant]
            # print(f"Current match for {applicant}: {current_a_match}")
            if current_a_match == -1:
                unmatched_hospitals.pop()
                # print(f"Unmatched Hospitals: {unmatched_hospitals}")
                applicant_matched[applicant] = hospital
                break
            # We need to look up the the rankings of the hospitals for the applicant, so we should use a different data structure from array. 
            # This is because we want to avoid using .index which has O(n) complexity
            # If we instead use a dict, lookups by index (key) have constant time complexity.
            # For fast lookup of rankings by hospitals, we need a dictionary with hospitals as keys and student rankings as values. 
            # Data structure is implemented in utils.py
            # Inspiration for using this data structure: https://towardsdatascience.com/faster-lookups-in-python-1d7503e9cd38/#:~:text=You%20have%20to%20go%20through,Useful%20Links
            elif s_list[applicant][hospital] < s_list[applicant][current_a_match]:
                applicant_matched[applicant] = hospital
                unmatched_hospitals.pop()
                unmatched_hospitals.append(current_a_match)
                break
            # We don't need another conditional statement because we will just keep going through the hospital's preferences
    return applicant_matched