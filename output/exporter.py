# output/exporter.py
import os
import logging

from output.excel_writer import write_overall_output, write_seats_left
from output.room_pdf import generate_room_pdfs
from output.student_pdf import generate_student_slips_pdf
from output.attendance_pdf import generate_attendance_pdfs
from output.zip_builder import build_zip

logger = logging.getLogger(__name__)


def export_all(
        output_root: str,
        date: str,
        session: str,
        allocations: dict,
        seats_left: dict,
        roll_name_map: dict,
        photos_folder: str = None
) -> dict:

    # --------------------- CREATE FOLDERS ---------------------
    date_folder = os.path.join(output_root, date)
    session_folder = os.path.join(date_folder, session)

    os.makedirs(session_folder, exist_ok=True)

    logger.info(f"Writing all export files into: {session_folder}")

    results = {}

    # --------------------- 1. Excel: overall + seats left ---------------------
    overall_excel = write_overall_output(session_folder, date, session, allocations)
    seats_left_excel = write_seats_left(session_folder, seats_left)

    results["overall_excel"] = overall_excel
    results["remaining_seats_excel"] = seats_left_excel

    logger.info("Excel outputs written.")

    # --------------------- 2. Build room-wise map ----------------------
    room_map = {}
    for subject, room_data in allocations.items():
        for room, rolls in room_data.items():
            room_map.setdefault(room, []).extend(
                [(subject, r) for r in rolls]
            )

    # --------------------- 3. Room PDFs ----------------------
    room_pdfs = generate_room_pdfs(
        session_folder, room_map, roll_name_map, date, session
    )
    results["room_pdfs"] = room_pdfs

    logger.info(f"Generated {len(room_pdfs)} room PDFs.")

    # --------------------- 4. Attendance PDFs (NEW) ----------------------
    attendance_pdfs = generate_attendance_pdfs(
        session_folder=session_folder,
        room_map=room_map,
        roll_name_map=roll_name_map,
        photos_folder=photos_folder,
        date=date,
        session=session
    )
    results["attendance_pdfs"] = attendance_pdfs

    logger.info(f"Generated {len(attendance_pdfs)} attendance PDFs.")

    # --------------------- 5. Student Slips PDF ----------------------
    student_slips_pdf = generate_student_slips_pdf(
        session_folder, room_map, roll_name_map, date, session, photos_folder
    )
    results["student_slips_pdf"] = student_slips_pdf

    logger.info("Student slips PDF generated.")

    # --------------------- 6. ZIP File ----------------------
    zip_path = build_zip(session_folder, prefix=f"seating_{date}_{session}")
    results["zip"] = zip_path

    logger.info(f"ZIP file created: {zip_path}")

    return results
