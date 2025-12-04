# 📚 IIT Patna – Optimal Seating Arrangement Generator

**Automated Exam Seating • Attendance • Room-wise PDFs • Student Slips • Excel Reports • Organized Output Structure**

---

# 📘 Problem Description

This project automates the complete **exam seating arrangement workflow** used at IIT Patna.

It processes:

* **Timetable**
* **Roll → Name mapping**
* **Room capacities**
* **Student photos (optional)**

and generates:

### ✔ Outputs

* **Room-wise seating PDFs**
* **Student slip PDF (with photos)**
* **Excel: Overall seating summary**
* **Excel: Remaining seats**
* **Fully organized folder structure by Date → Session**
* **ZIP file containing all output files**

### ✔ Seating Constraints

* Seats students from different subjects in a **mixed** pattern.
* Ensures **no two students of the same subject** sit next to each other.
* Does not exceed room capacities (supports `buffer` seats).
* Handles **dense** or **sparse** seating modes.
* Detects **subject clash** for students enrolled in multiple subjects.

---

# 📂 Input Requirements

## 1️⃣ Timetable Excel (Required)

Contains:

* Dates
* Sessions (Morning/Evening)
* Subjects under each session

## 2️⃣ Roll–Name Excel (Required)

Used in:

* Attendance sheets
* Student slips
* Room-wise PDFs

## 3️⃣ Room Capacities Excel (Required)

Each room should have:

* Room number
* Capacity

## 4️⃣ Photos Folder (Optional but Recommended)

Store photos as:

```
photos/<ROLL>.jpg
```

Example:

```
photos/2101CS01.jpg
```

If a photo is missing → **no crash** (placeholder omitted gracefully).

---

# 📁 Output Folder Structure

The system automatically organizes outputs like this:

```
output/
│
├── 2025-11-10/
│   ├── Morning/
│   │   ├── room_6101.pdf
│   │   ├── room_6102.pdf
│   │   ├── student_slips.pdf
│   │   ├── overall.xlsx
│   │   ├── seats_left.xlsx
│   │   └── seating_2025-11-10_morning.zip
│   │
│   └── Evening/
│       └── ...
│
└── 2025-11-11/
    └── ...
```

Everything is structured cleanly for exam-day handling.

---

# ▶️ Running from Python (Backend)

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the generator

```bash
python seating_arrangement.py \
  --input timetable.xlsx \
  --photos photos \
  --output output \
  --buffer 5 \
  --mode dense
```

### Argument Summary

| Argument   | Description                                       |
| ---------- | ------------------------------------------------- |
| `--input`  | Timetable Excel                                   |
| `--photos` | Folder containing student photos                  |
| `--output` | Main output directory                             |
| `--buffer` | Reduce effective room capacity by this many seats |
| `--mode`   | `dense` or `sparse` seating                       |
| `--log`    | Log file path                                     |

---

# 💻 Streamlit Frontend (Web App)

Start the app:

```bash
streamlit run streamlit_app.py
```

### Features

* Upload timetable Excel
* Input photos folder path
* Choose dense/sparse mode
* View live backend logs
* Download Excel/PDF/ZIP with one click
* Clean UI for exam staff

---

# 🐳 Running with Docker

## 1. Build Docker image

```bash
docker build -t seating-app .
```

## 2. Run container

```bash
docker run -p 8501:8501 \
  -v "$(pwd)/output":/app/output \
  -v "$(pwd)/photos":/app/photos \
  seating-app
```

Open the app:

👉 **[http://localhost:8501](http://localhost:8501)**

---

# 🧠 Internal Pipeline

1. Read input Excel files
2. Validate & load roll–name mapping
3. Read room capacities
4. Detect subject clashes
5. Allocate students optimally (mixed seating)
6. Normalize structure
7. Generate:

   * PDFs
   * Excel files
   * ZIP archive
   * Organized folder structure
8. Finish cleanly with logs

---

# ⚠️ Notes

* Photos are **optional** – system never crashes.
* Output folders are **auto-created**.
* Fully Docker-compatible.
* Designed for deployment on GitHub or servers.

---

# 🤝 Contributors

### **Ayush Dutt (IIT Patna)**

*Solo Developer*

