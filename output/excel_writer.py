import os
import pandas as pd


def write_overall_output(output_folder, date, session, allocations):
    """
    Creates an Excel file storing the overall seating allocation for a day+session.
    
    allocations format:
    {
        "CS249": {
            "6101": ["1401AI01", "1401AI02", ...],
            "6102": [...],
            ...
        },
        "MM304": { ... },
        ...
    }
    """

    os.makedirs(output_folder, exist_ok=True)

    rows = []

    for subject, room_data in allocations.items():
        for room, rolls in room_data.items():
            rows.append({
                "Date": date,
                "Session": session,
                "Subject": subject,
                "Room": room,
                "Count": len(rolls),
                "Roll_Numbers": ";".join(rolls)
            })

    df = pd.DataFrame(rows)

    # Filename for summary
    filename = f"{date}_{session}_overall.xlsx".replace(" ", "_")
    out_path = os.path.join(output_folder, filename)

    df.to_excel(out_path, index=False)
    return out_path



def write_seats_left(output_folder, seats_left):
    """
    seats_left format:
    {
        "6101": 10,
        "6102": 2,
        ...
    }
    """

    os.makedirs(output_folder, exist_ok=True)

    rows = [
        {"Room": room, "Seats_Left": left}
        for room, left in seats_left.items()
    ]

    df = pd.DataFrame(rows)

    out_path = os.path.join(output_folder, "remaining_seats.xlsx")
    df.to_excel(out_path, index=False)

    return out_path
