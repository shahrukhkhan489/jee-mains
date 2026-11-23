import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw_sources")
SLIDES_DIR = os.path.join(RAW_DIR, "lecture_slides")

os.makedirs(SLIDES_DIR, exist_ok=True)

# 1. Renaming the 2 original PDFs
pdf_moves = [
    (
        "syllabus-jee-main-2027.pdf",
        os.path.join("raw_sources", "JEE_Main_2027_Syllabus_Official_Reference.pdf")
    ),
    (
        "975100621-JEE-Main-Previous-Year-Question-Paper-With-Answer-Keys.pdf",
        os.path.join("raw_sources", "JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf")
    )
]

for src, dst in pdf_moves:
    src_path = os.path.join(BASE_DIR, src)
    dst_path = os.path.join(BASE_DIR, dst)
    if os.path.exists(src_path):
        subprocess.run(["git", "mv", src, dst], check=True, cwd=BASE_DIR)
        print(f"Moved {src} -> {dst}")

# 2. Renaming the 14 images to lecture_slides/
image_moves = [
    ("WhatsApp Image 2026-11-23 at 20.37.51.jpeg", "Slide_01_Chemistry_Weightage_Part1.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.52.jpeg", "Slide_02_Chemistry_Weightage_Part2_ShiftAvg.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.53 (1).jpeg", "Slide_03_Chemistry_Weightage_Part2_Full.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.53.jpeg", "Slide_04_Physics_Weightage_Part1_ShiftAvg.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.54.jpeg", "Slide_05_Physics_Weightage_Part1_Full.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.54 (1).jpeg", "Slide_06_Physics_Weightage_Part2_ShiftAvg.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.55.jpeg", "Slide_07_Physics_Weightage_Part2_Full.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.55 (1).jpeg", "Slide_08_Mathematics_Weightage_Part1_ShiftAvg.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.56.jpeg", "Slide_09_Mathematics_Weightage_Part2_Full.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.56 (1).jpeg", "Slide_10_Mathematics_Weightage_Part2_Instructor.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.57.jpeg", "Slide_11_Mathematics_Weightage_Part2_Annotated.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.57 (1).jpeg", "Slide_12_Mathematics_Weightage_Part1_Handwritten.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.58.jpeg", "Slide_13_Mathematics_Weightage_Part1_Full.jpeg"),
    ("WhatsApp Image 2026-11-23 at 20.37.58 (1).jpeg", "Slide_14_Mathematics_20_Chapters_Checklist.jpeg"),
]

for src_name, dst_name in image_moves:
    src_path = os.path.join("images", src_name)
    dst_path = os.path.join("raw_sources", "lecture_slides", dst_name)
    if os.path.exists(os.path.join(BASE_DIR, src_path)):
        subprocess.run(["git", "mv", src_path, dst_path], check=True, cwd=BASE_DIR)
        print(f"Moved {src_path} -> {dst_path}")

# Check if images directory is now empty
images_dir = os.path.join(BASE_DIR, "images")
if os.path.exists(images_dir) and not os.listdir(images_dir):
    os.rmdir(images_dir)
    print("Removed empty images/ directory")

print("All raw files moved and renamed successfully.")
