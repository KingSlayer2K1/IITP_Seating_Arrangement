import streamlit as st
import tempfile
import subprocess
import os

st.set_page_config(page_title="IITP Seating Arrangement Generator", layout="centered")

st.title("📚 IIT Patna – Seating Arrangement Generator")
st.write("Upload your exam files and generate seating PDFs + Excel reports.")

uploaded_excel = st.file_uploader("Upload timetable Excel (.xlsx)", type=["xlsx"])
photos_folder = st.text_input("Path to Photos Folder", value="photos")
output_folder = st.text_input("Output Folder", value="output")
buffer = st.number_input("Buffer", min_value=0, max_value=25, value=5)
mode = st.selectbox("Seating Mode", ["dense", "sparse"])

if st.button("Generate Seating Arrangement"):
    if not uploaded_excel:
        st.error("❌ Please upload an Excel file.")
        st.stop()

    # Save Excel temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_excel.read())
        tmp_path = tmp.name

    cmd = [
        "python", "seating_arrangement.py",
        "--input", tmp_path,
        "--photos", photos_folder,
        "--output", output_folder,
        "--buffer", str(buffer),
        "--mode", mode
    ]

    st.info("⚙️ Running backend… This may take a minute.")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # ---------------------------
    # CLEAN OUTPUT UI
    # ---------------------------

    if "completed" in result.stdout.lower():
        st.success("✅ Seating arrangement completed successfully!\nOutputs stored in the output folder.")
    else:
        st.error("⚠️ Something went wrong. Expand logs for details.")

    # Collapsible logs (hidden by default)
    with st.expander("📄 Backend Logs (click to expand)", expanded=False):
        st.text(result.stdout)
        if result.stderr:
            st.text("\n[ERROR STREAM]\n" + result.stderr)

    # ---------------------------
    # SHOW DOWNLOADABLE FILES
    # ---------------------------

    if os.path.exists(output_folder):
        st.subheader("📥 Download Generated Files")

        files = os.listdir(output_folder)
        excel_files = [f for f in files if f.endswith(".xlsx")]
        pdf_files = [f for f in files if f.endswith(".pdf")]
        zip_files = [f for f in files if f.endswith(".zip")]

        # Excel Downloads
        if excel_files:
            st.write("### 📊 Excel Reports")
            for f in excel_files:
                full_path = os.path.join(output_folder, f)
                with open(full_path, "rb") as fp:
                    st.download_button(
                        label=f"⬇️ Download {f}",
                        data=fp,
                        file_name=f,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

        # PDF Downloads
        if pdf_files:
            st.write("### 📘 Room-wise PDFs")
            for f in pdf_files:
                full_path = os.path.join(output_folder, f)
                with open(full_path, "rb") as fp:
                    st.download_button(
                        label=f"⬇️ Download {f}",
                        data=fp,
                        file_name=f,
                        mime="application/pdf"
                    )

        # ZIP Files
        if zip_files:
            st.write("### 📦 All Files (ZIP)")
            for f in zip_files:
                full_path = os.path.join(output_folder, f)
                with open(full_path, "rb") as fp:
                    st.download_button(
                        label=f"⬇️ Download {f}",
                        data=fp,
                        file_name=f,
                        mime="application/zip"
                    )
