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

# 🐳 Running with Docker

---

# Running This Project Using Docker (Recommended)

This project is fully containerized. Any user can run it without installing Python, Streamlit, ReportLab, or other dependencies.
Only Docker Desktop is required.

### 1. Install Docker Desktop

Download and install Docker Desktop from:
[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

Ensure Docker is running before proceeding.

### 2. Clone the Repository

```bash
git clone https://github.com/KingSlayer2K1/IITP_Seating_Arrangement.git
cd IITP_Seating_Arrangement
```

### 3. Prepare Input Files

The following are required:

1. Timetable Excel file
2. Roll–name mapping Excel or CSV
3. Room capacities Excel
4. Optional: a `photos/` folder containing student images in the format `ROLL.jpg`

Ensure an empty output directory exists:

```bash
mkdir output
```

### 4. Start the Application with Docker Compose

From inside the project folder, run:

```bash
docker compose up --build
```

Docker will:

* Build the image
* Install all dependencies inside the container
* Start Streamlit on port 8501

When the container starts successfully, the terminal will display:

```
You can now view your Streamlit app in your browser:
URL: http://127.0.0.1:8501
```

### 5. Access the Web Application

Open a browser and navigate to:

```
http://localhost:8501
```

From the interface, you can:

* Upload the timetable Excel file
* Enter the photos directory
* Select dense or sparse seating mode
* Generate seating arrangements
* Download PDFs, Excel sheets, and ZIP archives

All generated files are saved under the `output/DATE/SESSION/` structure.

### 6. Stopping the Container

Press:

```
Ctrl + C
```

Then clean up with:

```bash
docker compose down
```

### Notes

* The project directory is mounted inside the container, so code changes are reflected immediately without rebuilding.
* Photos are optional; missing images do not interrupt execution.
* All outputs are automatically organized in the appropriate folder structure.

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

