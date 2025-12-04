# output/zip_builder.py
import os
import zipfile


def build_zip(output_folder: str, prefix: str = "seating") -> str:
    """
    Recursively zip the ENTIRE output folder while preserving the directory tree.

    Example final ZIP structure:
        seating_Sunday_morning_20251203.zip
            Sunday/
                Morning/
                    Overall/
                    Rooms/
                    Slips/
                    remaining_seats.xlsx
                    ...
    """

    os.makedirs(output_folder, exist_ok=True)

    # Timestamp for unique ZIP filename
    try:
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    except Exception:
        ts = "now"

    zip_name = f"{prefix}_{ts}.zip"
    zip_path = os.path.join(output_folder, zip_name)

    # Write ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:

        # Walk through entire output folder
        for root, dirs, files in os.walk(output_folder):

            # Skip adding the ZIP file itself
            files = [f for f in files if not f.lower().endswith(".zip")]

            for f in files:
                full_path = os.path.join(root, f)

                # Relative path inside ZIP — preserves folder hierarchy
                arcname = os.path.relpath(full_path, start=output_folder)

                zf.write(full_path, arcname)

    return zip_path
