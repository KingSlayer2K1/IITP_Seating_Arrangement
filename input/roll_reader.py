import pandas as pd

class RollReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_subject_rolls(self, subject_code):
        """
        Reads all roll numbers for a given subject (course_code).
        Excel sheet: in_course_roll_mapping
        Columns: rollno, course_code
        """
        df = pd.read_excel(self.filepath, sheet_name="in_course_roll_mapping")

        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        if "rollno" not in df.columns or "course_code" not in df.columns:
            raise KeyError("❌ Expected columns: rollno, course_code in sheet in_course_roll_mapping")

        df_filtered = df[df["course_code"].astype(str).str.strip() == subject_code]

        # Convert to clean roll list
        rolls = sorted(df_filtered["rollno"].astype(str).str.strip().tolist())

        return rolls

    def read_roll_name_map(self):
        """
        Reads mapping of roll number → student name.
        Excel sheet: in_roll_name_mapping
        Columns: Roll, Name
        """
        df = pd.read_excel(self.filepath, sheet_name="in_roll_name_mapping")

        df.columns = [c.strip().lower() for c in df.columns]

        if "roll" not in df.columns or "name" not in df.columns:
            raise KeyError("❌ Expected columns: Roll, Name in sheet in_roll_name_mapping")

        roll_name_map = {
            str(row["roll"]).strip(): str(row["name"]).strip()
            for _, row in df.iterrows()
        }

        return roll_name_map


def read_subject_rolls(filepath, subject_code):
    reader = RollReader(filepath)
    return reader.read_subject_rolls(subject_code)


def read_roll_name_map(filepath):
    reader = RollReader(filepath)
    return reader.read_roll_name_map()
