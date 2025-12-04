import pandas as pd

class RoomCapacityReader:
    def __init__(self, filepath, logger=None):
        self.filepath = filepath
        self.logger = logger

    def read_room_capacity(self):
        try:
            df = pd.read_excel(self.filepath, sheet_name="in_room_capacity")
        except Exception as e:
            raise Exception(f"Error reading sheet 'in_room_capacity': {str(e)}")

        required_cols = ["Room No.", "Exam Capacity"]

        for col in required_cols:
            if col not in df.columns:
                raise KeyError(
                    f"Column '{col}' missing in room capacity sheet. "
                    f"Found columns: {list(df.columns)}"
                )

        room_capacity = {}

        for _, row in df.iterrows():
            room = str(row["Room No."]).strip().upper()
            cap = row["Exam Capacity"]

            try:
                cap = int(cap)
            except:
                continue  # skip merged cells or invalid values

            if room:
                room_capacity[room] = cap

        return room_capacity


def read_room_capacity(filepath, logger=None):
    reader = RoomCapacityReader(filepath, logger)
    return reader.read_room_capacity()
