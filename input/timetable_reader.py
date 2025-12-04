import pandas as pd


class TimetableReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        """
        Reads the first sheet of input_data_tt.xlsx.
        Expected columns:
            Day | Morning | Evening
        Returns:
            list of (day, session, [subjects])
        """
        df = pd.read_excel(self.filepath, sheet_name="in_timetable")

        # Normalize column names
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Ensure required columns exist
        required = ["day", "morning", "evening"]
        for col in required:
            if col not in df.columns:
                raise KeyError(f"Missing required column: {col}")

        timetable = []

        for _, row in df.iterrows():

            day = str(row["day"]).strip()

            # ---------- MORNING ----------
            morning_raw = str(row["morning"]).strip()
            if morning_raw.upper() != "NO EXAM":
                morning_subjects = [
                    s.strip() for s in morning_raw.split(";") if s.strip()
                ]
            else:
                morning_subjects = []

            # ---------- EVENING ----------
            evening_raw = str(row["evening"]).strip()
            if evening_raw.upper() != "NO EXAM":
                evening_subjects = [
                    s.strip() for s in evening_raw.split(";") if s.strip()
                ]
            else:
                evening_subjects = []

            # Add only if subjects exist
            if morning_subjects:
                timetable.append((day, "morning", morning_subjects))
            if evening_subjects:
                timetable.append((day, "evening", evening_subjects))

        return timetable
