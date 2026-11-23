import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
RAW_DIR = os.path.join(BASE_DIR, "raw_sources")
SLIDES_DIR = os.path.join(RAW_DIR, "lecture_slides")

# Image mapping
IMAGE_MAP = [
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

# -------------------------------------------------------------
# 1. UPDATE docs/01_Syllabus_2027.md
# -------------------------------------------------------------
def build_syllabus_md():
    syllabus_path = os.path.join(DOCS_DIR, "01_Syllabus_2027.md")
    with open(syllabus_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace old raw source reference
    text = text.replace("`syllabus-jee-main-2027.pdf`", "[`raw_sources/JEE_Main_2027_Syllabus_Official_Reference.pdf`](../raw_sources/JEE_Main_2027_Syllabus_Official_Reference.pdf)")
    
    with open(syllabus_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated docs/01_Syllabus_2027.md")

# -------------------------------------------------------------
# 2. UPDATE docs/02_Chapterwise_Weightage_Analysis.md
# -------------------------------------------------------------
def build_weightage_md():
    weightage_path = os.path.join(DOCS_DIR, "02_Chapterwise_Weightage_Analysis.md")
    with open(weightage_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace source folder references
    text = text.replace("`images/`", "[`raw_sources/lecture_slides/`](../raw_sources/lecture_slides/)")
    text = text.replace("slide `WhatsApp Image 2026-11-23 at 20.37.58 (1).jpeg`", "[`Slide_14_Mathematics_20_Chapters_Checklist.jpeg`](../raw_sources/lecture_slides/Slide_14_Mathematics_20_Chapters_Checklist.jpeg)")
    text = text.replace("in `images/` (`WhatsApp Image 2026-11-23 at 20.37.51` to `20.37.58`)", "in [`raw_sources/lecture_slides/`](../raw_sources/lecture_slides/) (`Slide_01` to `Slide_14`)")

    # Replace each individual WhatsApp slide header
    for old_name, new_name in IMAGE_MAP:
        text = text.replace(f"`{old_name}`", f"[`{new_name}`](../raw_sources/lecture_slides/{new_name})")
        text = text.replace(f"({old_name})", f"({new_name})")
        text = text.replace(f"frame ({old_name[:8]}", f"frame ({new_name}")

    with open(weightage_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated docs/02_Chapterwise_Weightage_Analysis.md")

# -------------------------------------------------------------
# 3. UPDATE docs/03_Question_Papers_Catalog.md
# -------------------------------------------------------------
def build_papers_catalog_md():
    catalog_path = os.path.join(DOCS_DIR, "03_Question_Papers_Catalog.md")
    with open(catalog_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace old raw source reference
    text = text.replace("`975100621-JEE-Main-Previous-Year-Question-Paper-With-Answer-Keys.pdf`", "[`raw_sources/JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf`](../raw_sources/JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf)")

    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated docs/03_Question_Papers_Catalog.md")

# -------------------------------------------------------------
# 4. UPDATE ROOT README.md
# -------------------------------------------------------------
def build_master_readme():
    readme_path = os.path.join(BASE_DIR, "README.md")
    out = []
    out.append("# JEE Main Master Resource & Preparation Archive")
    out.append("\n> Comprehensive repository containing the **Official JEE Main Syllabus**, **2024–2026 Chapter-Wise Weightage Analysis**, and **173 Downloaded Previous Year Question Papers (2002–2025)** with complete answer keys.\n")
    out.append("---\n")
    out.append("## Repository Directory Structure\n")
    out.append("```")
    out.append("Jee Mains/")
    out.append("├── README.md                            # 🌟 Master Guide: Unified syllabus, weightage & papers hub")
    out.append("├── docs/                                # 📚 Clean, structured curriculum & analysis guides")
    out.append("│   ├── 01_Syllabus_2027.md              # Full 52-unit syllabus tables (Math, Physics, Chemistry)")
    out.append("│   ├── 02_Chapterwise_Weightage_Analysis.md # 2024-2026 question trends, tiers & slide audit")
    out.append("│   └── 03_Question_Papers_Catalog.md    # Shift-by-shift catalog with local & web links")
    out.append("├── papers/                              # 📁 173 downloaded question papers (792 MB)")
    out.append("│   ├── 2025_Jan/                        # 10 shift-wise papers (Jan 22 - Jan 29)")
    out.append("│   ├── 2024_Apr/ & 2024_Jan/            # 20 shift-wise papers")
    out.append("│   ├── 2023_Apr/ & 2023_Jan/            # 24 shift-wise papers")
    out.append("│   ├── 2022_Jul/ & 2022_Jun/            # 22 shift-wise papers")
    out.append("│   ├── 2021_Feb/ to 2021_Aug/           # 26 shift-wise papers")
    out.append("│   ├── 2020_Jan/ & 2020_Sep/            # 16 shift-wise papers")
    out.append("│   ├── 2019_Jan/ & 2019_Apr/            # 16 shift-wise papers")
    out.append("│   ├── 2018/ to 2012/                   # 29 shift-wise & online papers")
    out.append("│   ├── 2011-2002/                       # 10 annual original papers")
    out.append("│   └── README.md                        # Local shift catalog & file size index")
    out.append("├── raw_sources/                         # 📦 Preserved original raw inputs (properly named)")
    out.append("│   ├── JEE_Main_2027_Syllabus_Official_Reference.pdf # Original 26-page syllabus PDF")
    out.append("│   ├── JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf # Original 12-page MathonGo PDF")
    out.append("│   └── lecture_slides/                  # 14 lecture screenshots (Slide_01 to Slide_14)")
    out.append("└── scripts/                             # ⚙️ Automation & organization utilities")
    out.append("    ├── download_papers.py               # Multi-threaded batch PDF downloader")
    out.append("    ├── organize_docs.py                 # Document formatting & index generator")
    out.append("    └── rename_raw_sources.py            # Raw files reorganization utility")
    out.append("```\n")
    out.append("---\n")
    out.append("## 1. High-Yield Scoring Roadmap & Weightage Summary\n")
    out.append("Based on multi-year shift analysis across 2024, 2025, and 2026, here are the top scoring topics per subject:\n")
    out.append("| Subject | Top Scoring Units (Tier 1) | Expected Qs / Shift | High-ROI Quick Win Units |")
    out.append("| :--- | :--- | :---: | :--- |")
    out.append("| **Mathematics** | • Coordinate Geometry (Lines, Circles, Conics)<br>• Matrices & Determinants<br>• Vectors & 3D Geometry<br>• Sequence & Series | **3 – 4** (Coord Geo)<br>**1 – 2** (3D / Vectors)<br>**1 – 2** (Matrices) | • Statistics (1 direct Q)<br>• Area Under Curve (1 direct Q)<br>• Binomial Theorem |")
    out.append("| **Physics** | • Heat & Thermodynamics<br>• Current Electricity (48 Qs in 2026)<br>• Electrostatics & Capacitors<br>• Properties of Matter | **2 – 3** (Thermodynamics)<br>**1 – 2** (Current Elec)<br>**1 – 2** (Ray Optics) | • Modern Physics (Atoms/Nuclei, Dual Nature, Semiconductors)<br>• Units & Measurements |")
    out.append("| **Chemistry** | • General Organic Chemistry (GOC)<br>• Coordination Compounds<br>• Aldehydes, Ketones & Acids<br>• Chemical Bonding | **2 – 3** (GOC)<br>**2 – 3** (Coordination)<br>**1 – 2** (Bonding) | • Biomolecules (1 direct Q)<br>• Periodic Table (1 direct Q)<br>• d- & f-Block Elements |")
    out.append("\n👉 *For full shift statistics and notes, view [docs/02_Chapterwise_Weightage_Analysis.md](./docs/02_Chapterwise_Weightage_Analysis.md)*\n")
    out.append("---\n")
    out.append("## 2. Official Syllabus Overview (52 Units)\n")
    out.append("| Subject | Total Units | Branch / Division | Link to Full Syllabus |")
    out.append("| :--- | :---: | :--- | :--- |")
    out.append("| **Mathematics** | 14 Units | Sets, Algebra, Calculus, Coordinate Geometry, Vectors & 3D, Statistics | [View Mathematics Syllabus](./docs/01_Syllabus_2027.md#1-mathematics-syllabus-14-units) |")
    out.append("| **Physics** | 19 Units | Mechanics, Thermal Physics, Electrodynamics, Optics, Modern Physics | [View Physics Syllabus](./docs/01_Syllabus_2027.md#2-physics-syllabus-19-units) |")
    out.append("| **Chemistry** | 19 Units | Physical (Units 1–8), Inorganic (Units 9–12), Organic (Units 13–19) | [View Chemistry Syllabus](./docs/01_Syllabus_2027.md#3-chemistry-syllabus-19-units) |")
    out.append("\n👉 *For topic-by-topic details, view [docs/01_Syllabus_2027.md](./docs/01_Syllabus_2027.md)*\n")
    out.append("---\n")
    out.append("## 3. Question Papers Archive (2002 – 2025)\n")
    out.append("All 173 shift-wise question papers are saved locally on disk under `papers/` with their official answer keys:\n")
    out.append("| Session Group | Time Span | Total Papers | Direct Folder Access |")
    out.append("| :--- | :---: | :---: | :--- |")
    out.append("| **Recent Shifts** | 2025 | 10 Papers | [`papers/2025_Jan/`](./papers/2025_Jan/) |")
    out.append("| **NTA Shift Series** | 2024 – 2022 | 74 Papers | [`papers/2024_Jan/`](./papers/2024_Jan/) • [`papers/2024_Apr/`](./papers/2024_Apr/) • [`papers/2023_Jan/`](./papers/2023_Jan/) • [`papers/2023_Apr/`](./papers/2023_Apr/) |")
    out.append("| **Multiple Sessions Era** | 2021 – 2019 | 58 Papers | [`papers/2021_Aug/`](./papers/2021_Aug/) • [`papers/2020_Sep/`](./papers/2020_Sep/) • [`papers/2019_Jan/`](./papers/2019_Jan/) |")
    out.append("| **Online / Offline Transition**| 2018 – 2012 | 21 Papers | [`papers/2018/`](./papers/2018/) • [`papers/2017/`](./papers/2017/) • [`papers/2016/`](./papers/2016/) • [`papers/2015/`](./papers/2015/) |")
    out.append("| **Classic JEE Main (AIEEE)** | 2011 – 2002 | 10 Papers | [`papers/2011-2002/`](./papers/2011-2002/) |")
    out.append("\n👉 *For individual shift links and online mirrors, view [docs/03_Question_Papers_Catalog.md](./docs/03_Question_Papers_Catalog.md)*\n")
    out.append("---\n")
    out.append("## 4. Preserved Raw Sources Archive\n")
    out.append("| Resource | Proper Clean Name | Description |")
    out.append("| :--- | :--- | :--- |")
    out.append("| **Official Syllabus PDF** | [`JEE_Main_2027_Syllabus_Official_Reference.pdf`](./raw_sources/JEE_Main_2027_Syllabus_Official_Reference.pdf) | Original 26-page Vedantu syllabus PDF |")
    out.append("| **PYQ Link Index PDF** | [`JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf`](./raw_sources/JEE_Main_Previous_Year_Papers_Index_MathonGo.pdf) | Original 12-page MathonGo index PDF |")
    out.append("| **Lecture Video Slides** | [`raw_sources/lecture_slides/`](./raw_sources/lecture_slides/) | 14 original screenshots renamed by subject & slide topic |")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Updated root README.md")

if __name__ == "__main__":
    build_syllabus_md()
    build_weightage_md()
    build_papers_catalog_md()
    build_master_readme()
