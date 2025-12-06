# output/attendance_pdf.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_attendance_pdfs(
    session_folder: str,
    room_map: dict,
    roll_name_map: dict,
    photos_folder: str,
    date: str,
    session: str
) -> list:
    """
    Generates one attendance PDF per room.

    Attendance Format:
    ----------------------------------------------
    | Photo | Roll | Name | Signature |
    ----------------------------------------------

    Photos are optional. Missing photos do NOT break.
    """

    os.makedirs(session_folder, exist_ok=True)
    styles = getSampleStyleSheet()
    header = styles["Heading2"]
    normal = styles["Normal"]

    pdf_paths = []

    for room, entries in room_map.items():
        filename = f"attendance_{room}.pdf"
        out_path = os.path.join(session_folder, filename)

        doc = SimpleDocTemplate(out_path, pagesize=A4,
                                topMargin=15*mm, bottomMargin=15*mm,
                                leftMargin=15*mm, rightMargin=15*mm)

        elements = []

        title = Paragraph(f"Attendance Sheet – Room {room}<br/>{date} — {session}", header)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Table Header
        data = [["Photo", "Roll Number", "Student Name", "Signature"]]

        for subj, roll in entries:
            name = roll_name_map.get(roll, "")

            # Load photo ONLY if exists
            photo_path = os.path.join(photos_folder, f"{roll}.jpg") if photos_folder else None
            if photo_path and os.path.exists(photo_path):
                try:
                    img = Image(photo_path, width=25*mm, height=30*mm)
                except Exception:
                    img = Paragraph("No Photo", normal)
            else:
                img = Paragraph("No Photo", normal)

            data.append([img, roll, name, ""])

        table = Table(
            data,
            colWidths=[30*mm, 40*mm, 60*mm, 50*mm]
        )

        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.6, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(table)

        doc.build(elements)
        pdf_paths.append(out_path)

    return pdf_paths
