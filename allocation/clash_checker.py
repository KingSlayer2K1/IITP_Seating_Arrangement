def check_clashes(subjects, subject_rolls):
    """
    Checks if any roll number appears in more than one subject on the same day.
    subjects: list of subject codes
    subject_rolls: dict { subject_code: [rolls] }
    """
    
    # Convert each list of rolls into a set
    subject_sets = {subj: set(rolls) for subj, rolls in subject_rolls.items()}

    # Check pairwise intersections
    for i in range(len(subjects)):
        for j in range(i + 1, len(subjects)):
            s1 = subjects[i]
            s2 = subjects[j]

            intersection = subject_sets[s1].intersection(subject_sets[s2])

            if intersection:
                # Return first detected clash
                return {
                    "subject1": s1,
                    "subject2": s2,
                    "roll_numbers": list(intersection)
                }

    return None  # No clashes
