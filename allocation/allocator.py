# allocation/allocator.py

def allocate_students_to_rooms(subject_rolls, room_caps, buffer=0, mode="dense", logger=None):
    """
    RETURNS (allocations, seats_left)

    allocations format (for excel_writer):
    {
        "CS249": {
            "6101": [...],
            "6102": [...],
        },
        "MM304": {
            "10502": [...],
        }
    }

    seats_left format:
    {
        "6101": remaining,
        "6102": remaining,
        ...
    }
    """

    # ---------------- APPLY BUFFER ----------------
    adjusted_caps = {}
    for room, cap in room_caps.items():
        adjusted = max(cap - buffer, 1)
        adjusted_caps[room] = adjusted

    if logger:
        logger.info("Room capacities (after buffer):")
        for r, c in adjusted_caps.items():
            logger.info(f"{r}: {c}")

    # Master seats left
    seats_left = {room: cap for room, cap in adjusted_caps.items()}

    # Sort rooms largest → smallest
    rooms_sorted = sorted(adjusted_caps.items(), key=lambda x: -x[1])

    # This is the final output structure
    final_allocations = {}  # subject -> room -> list rolls

    # ---------------- ALLOCATE SUBJECT BY SUBJECT ----------------
    for subject, rolls in subject_rolls.items():

        if logger:
            logger.info(f"Allocating subject {subject} ({len(rolls)} students)")

        remaining = list(rolls)          # students still to place
        final_allocations[subject] = {}  # create subject entry

        room_index = 0

        while remaining and room_index < len(rooms_sorted):
            room_name, room_capacity = rooms_sorted[room_index]

            free_seats = seats_left[room_name]

            if free_seats <= 0:
                room_index += 1
                continue

            # capacity per mode
            if mode == "dense":
                use_cap = free_seats

            elif mode == "sparse":
                use_cap = max(free_seats // 2, 1)

            elif mode == "mixed":
                use_cap = max(int(0.70 * free_seats), 1)

            else:
                raise ValueError("Invalid mode")

            assign_count = min(use_cap, len(remaining))
            assigned = remaining[:assign_count]

            # Record into subject → room → rolls
            if room_name not in final_allocations[subject]:
                final_allocations[subject][room_name] = []

            final_allocations[subject][room_name].extend(assigned)

            # Update remaining
            remaining = remaining[assign_count:]

            # Update seats_left
            seats_left[room_name] -= assign_count

            if logger:
                logger.info(f"Room {room_name}: assigned {assign_count} students of {subject}")

        if remaining and logger:
            logger.error(f"⚠ Not enough rooms for subject {subject}! {len(remaining)} unassigned students.")

    # Done
    return final_allocations, seats_left
