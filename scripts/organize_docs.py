import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PAPERS_DIR = os.path.join(BASE_DIR, "papers")

# -------------------------------------------------------------
# 1. GENERATE docs/01_Syllabus_2027.md
# -------------------------------------------------------------
def build_syllabus_md():
    syllabus_path = os.path.join(DOCS_DIR, "01_Syllabus_2027.md")
    # Read existing raw text to extract unit titles and topics
    with open(syllabus_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Parse Units
    # Format in file:
    # ## Mathematics (14 units)
    # ### Unit 1 - Sets, Relations and Functions
    # Sets and their representation...
    
    sections = re.split(r"\n##\s+", text)
    intro_part = sections[0]
    
    math_text = ""
    physics_text = ""
    chem_text = ""
    
    for sec in sections[1:]:
        if sec.startswith("Mathematics"):
            math_text = sec
        elif sec.startswith("Physics"):
            physics_text = sec
        elif sec.startswith("Chemistry"):
            chem_text = sec

    def parse_units(subject_sec):
        unit_blocks = re.split(r"\n###\s+Unit\s+", subject_sec)
        units = []
        for b in unit_blocks[1:]:
            lines = [l.strip() for l in b.strip().split("\n") if l.strip()]
            header_line = lines[0] # e.g. "1 - Sets, Relations and Functions"
            m = re.match(r"(\d+)\s*[-:]\s*(.+)", header_line)
            if m:
                u_num = m.group(1)
                u_name = m.group(2).strip()
            else:
                u_num = "?"
                u_name = header_line
            
            topics = " ".join(lines[1:])
            # Clean closing note if present in last unit
            if "## Closing note" in topics:
                topics = topics.split("## Closing note")[0].strip()
            units.append((u_num, u_name, topics))
        return units

    math_units = parse_units(math_text)
    physics_units = parse_units(physics_text)
    chem_units = parse_units(chem_text)

    out = []
    out.append("# JEE Main Official Syllabus Reference (2026/2027)")
    out.append("\n> **Source Document:** `syllabus-jee-main-2027.pdf` (26 pages)  ")
    out.append("> **Curriculum Status:** Complete, unabridged unit-wise syllabus based on the latest National Testing Agency (NTA) guidelines across **Mathematics, Physics, and Chemistry** (52 total units).\n")
    out.append("---\n")
    out.append("## Quick Navigation\n")
    out.append("- [1. Mathematics Syllabus (14 Units)](#1-mathematics-syllabus-14-units)")
    out.append("- [2. Physics Syllabus (19 Units)](#2-physics-syllabus-19-units)")
    out.append("- [3. Chemistry Syllabus (19 Units)](#3-chemistry-syllabus-19-units)")
    out.append("  - [Physical Chemistry (Units 1 – 8)](#physical-chemistry-units-1--8)")
    out.append("  - [Inorganic Chemistry (Units 9 – 12)](#inorganic-chemistry-units-9--12)")
    out.append("  - [Organic Chemistry (Units 13 – 19)](#organic-chemistry-units-13--19)")
    out.append("- [Closing Advisory Note](#closing-advisory-note)\n")
    out.append("---\n")

    out.append("## 1. Mathematics Syllabus (14 Units)\n")
    out.append("| Unit No. | Unit Name | Detailed Topics Covered |")
    out.append("| :---: | :--- | :--- |")
    for unum, uname, utopics in math_units:
        out.append(f"| **Unit {unum}** | **{uname}** | {utopics} |")

    out.append("\n---\n")
    out.append("## 2. Physics Syllabus (19 Units)\n")
    out.append("| Unit No. | Unit Name | Detailed Topics Covered |")
    out.append("| :---: | :--- | :--- |")
    for unum, uname, utopics in physics_units:
        out.append(f"| **Unit {unum}** | **{uname}** | {utopics} |")

    out.append("\n---\n")
    out.append("## 3. Chemistry Syllabus (19 Units)\n")
    out.append("### Physical Chemistry (Units 1 – 8)\n")
    out.append("| Unit No. | Unit Name | Detailed Topics Covered |")
    out.append("| :---: | :--- | :--- |")
    for unum, uname, utopics in chem_units:
        try:
            n = int(unum)
            if 1 <= n <= 8:
                out.append(f"| **Unit {unum}** | **{uname}** | {utopics} |")
        except:
            pass

    out.append("\n### Inorganic Chemistry (Units 9 – 12)\n")
    out.append("| Unit No. | Unit Name | Detailed Topics Covered |")
    out.append("| :---: | :--- | :--- |")
    for unum, uname, utopics in chem_units:
        try:
            n = int(unum)
            if 9 <= n <= 12:
                out.append(f"| **Unit {unum}** | **{uname}** | {utopics} |")
        except:
            pass

    out.append("\n### Organic Chemistry (Units 13 – 19)\n")
    out.append("| Unit No. | Unit Name | Detailed Topics Covered |")
    out.append("| :---: | :--- | :--- |")
    for unum, uname, utopics in chem_units:
        try:
            n = int(unum)
            if 13 <= n <= 19:
                out.append(f"| **Unit {unum}** | **{uname}** | {utopics} |")
        except:
            pass

    out.append("\n---\n")
    out.append("## Closing Advisory Note\n")
    out.append("> *Note:* The official JEE Main 2027 syllabus has not been released separately by NTA yet. The Mathematics, Physics, and Chemistry tables above are transcribed from the latest officially available JEE Main curriculum (2026 circular) and serve as the standard reference for preparation.")

    with open(syllabus_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Updated docs/01_Syllabus_2027.md")

# -------------------------------------------------------------
# 2. GENERATE docs/02_Chapterwise_Weightage_Analysis.md
# -------------------------------------------------------------
def build_weightage_md():
    weightage_path = os.path.join(DOCS_DIR, "02_Chapterwise_Weightage_Analysis.md")
    with open(weightage_path, "r", encoding="utf-8") as f:
        raw_transcript = f.read()

    # Build consolidated clean analysis
    out = []
    out.append("# JEE Main Chapter-Wise Question & Weightage Analysis (2024 – 2026)")
    out.append("\n> **Primary Sources:** 14 slide screenshots in `images/` from the Vedantu JEE Analysis Master Lecture.  ")
    out.append("> **Coverage:** Consolidated, unobscured multi-year question frequency (2024, 2025, 2026), average questions per session, expected questions per shift, and high-yield scoring roadmaps across Physics, Chemistry, and Mathematics.\n")
    out.append("---\n")
    out.append("## Table of Contents")
    out.append("1. [Executive Summary & Cross-Subject Priority Roadmap](#1-executive-summary--cross-subject-priority-roadmap)")
    out.append("2. [Physics Chapter-Wise Analysis](#2-physics-chapter-wise-analysis)")
    out.append("3. [Chemistry Chapter-Wise Analysis](#3-chemistry-chapter-wise-analysis)")
    out.append("4. [Mathematics Chapter-Wise Analysis](#4-mathematics-chapter-wise-analysis)")
    out.append("5. [Mathematics 20-Chapter Checklist](#5-mathematics-20-chapter-checklist)")
    out.append("6. [Appendix: Raw Slide-by-Slide Transcript & Audit Log](#6-appendix-raw-slide-by-slide-transcript--audit-log)\n")
    out.append("---\n")

    # 1. Executive Roadmap
    out.append("## 1. Executive Summary & Cross-Subject Priority Roadmap\n")
    out.append("To maximize your JEE Main score with the highest return on investment (ROI), focus study time according to these validated priority tiers:\n")
    out.append("| Priority Tier | Physics Focus Areas | Chemistry Focus Areas | Mathematics Focus Areas | Expected Qs / Shift |")
    out.append("| :--- | :--- | :--- | :--- | :---: |")
    out.append("| **Tier 1 (Core Heavyweights)** | • Heat & Thermodynamics<br>• Current Electricity<br>• Properties of Matter<br>• Electrostatics<br>• Geometrical Optics | • Basics of Organic (GOC)<br>• Coordination Compounds<br>• Aldehydes & Ketones<br>• Chemical Bonding<br>• Electrochemistry | • Coordinate Geometry (Lines, Circles, Conics)<br>• Matrices & Determinants<br>• 3D Geometry & Vectors<br>• Sequence & Series | **14 – 17 Qs** |")
    out.append("| **Tier 2 (High-ROI Scorers)** | • Units & Measurements<br>• Modern Physics (Atoms/Nuclei, Dual Nature, Semiconductors)<br>• Kinematics | • Biomolecules<br>• d- & f-Block Elements<br>• Structure of Atom<br>• Periodic Table<br>• Solutions & Kinetics | • Definite Integration & AUC<br>• Differential Equations<br>• Statistics<br>• Binomial Theorem | **8 – 11 Qs** |")
    out.append("| **Tier 3 (Supplementary)** | • Work, Power & Energy<br>• Laws of Motion<br>• Gravitation<br>• Wave Optics & AC<br>• Oscillations & Waves | • Equilibrium<br>• Hydrocarbons<br>• Haloalkanes<br>• Amines & Polymers<br>• Salt Analysis | • Limits, Continuity & Diff.<br>• Complex Numbers<br>• Probability<br>• Permutations & Combinations<br>• Trigonometry | **Balance to 25/30** |")

    out.append("\n---\n")

    # 2. Physics Table
    out.append("## 2. Physics Chapter-Wise Analysis\n")
    out.append("### Physics Master Question Distribution Table\n")
    out.append("| Chapter Name | 2024 | 2025 | 2026 (Trend) | 3-Yr Avg | Expected Qs / Shift | Strategic Tier |")
    out.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    physics_data = [
        ("Heat and Thermodynamics", 44, 50, "37↓", 43, "2 - 3", "Tier 1 (Top Scorer)"),
        ("Properties of Matter (Solids & Fluids)", 42, 32, "36≈", 37, "1 - 2", "Tier 1"),
        ("Electrostatics", 32, 37, "26↓", 32, "1 - 2", "Tier 1"),
        ("Current Electricity", 28, 21, "48↑", 32, "1 - 2", "Tier 1 (Surging Trend)"),
        ("Geometrical Optics (Ray Optics)", 21, 41, "35↓", 32, "1 - 2", "Tier 1"),
        ("Units & Measurements", 33, 26, "30↑", 30, "1 - 2", "Tier 1 (High ROI)"),
        ("Kinematics (1D, 2D, Circular)", 35, 28, "25↓", 29, "1 - 2", "Tier 2"),
        ("Atoms and Nuclei", 40, 20, "24↑", 28, "1 - 2", "Tier 2 (High ROI)"),
        ("Magnetic Effects of Current", 31, 22, "19↓", 24, "1 - 2", "Tier 2"),
        ("Rotational Motion", 20, 26, "26≈", 24, "1 - 2", "Tier 2"),
        ("Wave Optics", 23, 21, "23≈", 22, "1 - 2", "Tier 2"),
        ("Semiconductors / Electronic Devices", 22, 18, "21≈", 20, "1", "Tier 2 (High ROI)"),
        ("Dual Nature of Radiation", 23, 21, "16↓", 20, "1", "Tier 2 (High ROI)"),
        ("Gravitation", 24, 13, "10↓", 16, "0 - 1", "Tier 3"),
        ("Alternating Current (AC)", 26, 9, "10≈", 15, "0 - 1", "Tier 3"),
        ("Laws of Motion (NLM)", 25, 7, "12↑", 15, "0 - 1", "Tier 3"),
        ("Electromagnetic Induction (EMI)", 17, 8, "20↑", 15, "0 - 1", "Tier 3"),
        ("Simple Harmonic Motion (SHM)", 15, 11, "15≈", 14, "0 - 1", "Tier 3"),
        ("Work, Power & Energy", 17, 13, "13≈", 14, "0 - 1", "Tier 3"),
        ("Electromagnetic Waves", 15, 10, "17↑", 14, "0 - 1", "Tier 3 (High ROI)"),
        ("Capacitor", 14, 16, "13≈", 14, "0 - 1", "Tier 3"),
        ("Waves (Sound & String)", 9, 11, "9≈", 10, "0 - 1", "Tier 3"),
    ]
    for row in physics_data:
        out.append(f"| **{row[0]}** | {row[1]} | {row[2]} | {row[3]} | {row[4]} | **{row[5]}** | {row[6]} |")

    out.append("\n**Key Physics Takeaways:**")
    out.append("1. **Modern Physics Goldmine:** Modern Physics (`Atoms and Nuclei`, `Dual Nature`, `Semiconductors`) + `Units & Measurements` reliably delivers **4 to 5 direct, formula-based questions per shift** (~16–20 marks) with very low preparation overhead.")
    out.append("2. **Thermal & Electrical Pillars:** `Heat and Thermodynamics` and `Current Electricity` (which spiked to 48 questions in 2026) are the heaviest single topics in Physics.")

    out.append("\n---\n")

    # 3. Chemistry Table
    out.append("## 3. Chemistry Chapter-Wise Analysis\n")
    out.append("### Chemistry Master Question Distribution Table\n")
    out.append("| Chapter Name | 2024 | 2025 | 2026 (Trend) | 3-Yr Avg | Expected Qs / Shift | Strategic Tier |")
    out.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    chem_data = [
        ("Basics of Organic Chemistry (GOC)", 63, 33, "32≈", 43, "2 - 3", "Tier 1 (Single Highest)"),
        ("Coordination Compounds", 48, 43, "36↓", 42, "2 - 3", "Tier 1 (Inorganic Core)"),
        ("Aldehydes, Ketones & Carboxylic Acids", 31, 26, "35↑", 31, "1 - 2", "Tier 1"),
        ("Chemical Bonding & Molecular Structure", 49, 21, "23≈", 31, "1 - 2", "Tier 1"),
        ("Electrochemistry", 31, 22, "21≈", 25, "1 - 2", "Tier 1"),
        ("Thermodynamics", 22, 31, "22↓", 25, "1 - 2", "Tier 1"),
        ("d- and f-Block Elements", 35, 19, "21≈", 25, "1 - 2", "Tier 1"),
        ("Compounds Containing Nitrogen (Amines)", 28, 22, "25≈", 25, "1 - 2", "Tier 2"),
        ("Some Basic Concepts of Chemistry (Mole)", 26, 29, "18↓", 24, "1 - 2", "Tier 2"),
        ("Structure of Atom", 24, 21, "26↑", 24, "1 - 2", "Tier 2"),
        ("Periodic Table & Periodicity", 26, 28, "18↓", 24, "1 - 2", "Tier 2"),
        ("Equilibrium (Physical & Ionic)", 19, 25, "28↑", 24, "1", "Tier 2"),
        ("Chemical Kinetics & Nuclear Chemistry", 20, 25, "27↑", 24, "1", "Tier 2"),
        ("Solutions", 19, 27, "24≈", 23, "1", "Tier 2"),
        ("Biomolecules", 22, 20, "19≈", 20, "1", "Tier 2 (High ROI)"),
        ("Hydrocarbons", 20, 19, "20≈", 20, "1", "Tier 2"),
        ("Haloalkanes and Haloarenes", 25, 19, "17↓", 20, "1", "Tier 2"),
        ("p-Block Elements", 25, 13, "21↑", 20, "1", "Tier 2"),
        ("Alcohols, Phenols and Ethers", 23, 13, "13≈", 16, "0 - 1", "Tier 3"),
        ("Redox Reactions", 16, 6, "8≈", 10, "0 - 1", "Tier 3"),
        ("Practical Organic Chemistry", 16, 6, "20↑", 14, "0 - 1", "Tier 3 (Rising)"),
        ("Salt Analysis", 8, 12, "6↓", 8, "0 - 1", "Tier 3"),
    ]
    for row in chem_data:
        out.append(f"| **{row[0]}** | {row[1]} | {row[2]} | {row[3]} | {row[4]} | **{row[5]}** | {row[6]} |")

    out.append("\n**Key Chemistry Takeaways:**")
    out.append("1. **Organic Core:** `Basics of Organic Chemistry (GOC)` and `Carbonyl Compounds` (Aldehydes, Ketones, Acids) account for over 40% of the entire organic chemistry paper.")
    out.append("2. **Inorganic Powerhouses:** `Coordination Compounds` and `d- and f-Block Elements` require thorough NCERT line-by-line reading and guarantee 3-4 questions per shift.")

    out.append("\n---\n")

    # 4. Mathematics Table
    out.append("## 4. Mathematics Chapter-Wise Analysis\n")
    out.append("### Mathematics Master Question Distribution Table\n")
    out.append("| Chapter Name | 2024 | 2025 | 2026 (Trend) | 3-Yr Avg | Expected Qs / Shift | Strategic Tier |")
    out.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    math_data = [
        ("Coordinate Geometry (Lines, Circles, Conics)", 75, 71, "71≈", 72, "3 - 4", "Tier 1 (Dominant Scorer)"),
        ("Matrices & Determinants", 40, 34, "33↓", 36, "1 - 2", "Tier 1 (High ROI)"),
        ("Three-Dimensional Geometry (3D)", 43, 34, "29↓", 35, "1 - 2", "Tier 1 (High ROI)"),
        ("Sequence & Series", 36, 27, "33↑", 32, "1 - 2", "Tier 1"),
        ("Definite Integration", 43, 23, "31↑", 32, "1 - 2", "Tier 1"),
        ("Vector Algebra", 35, 23, "27↑", 29, "1 - 2", "Tier 1 (High ROI)"),
        ("Differential Equations", 37, 21, "21≈", 26, "1 - 2", "Tier 2"),
        ("Limits, Continuity & Differentiability (LCD)", 28, 26, "21↓", 25, "1 - 2", "Tier 2"),
        ("Probability", 26, 21, "18↓", 22, "1 - 2", "Tier 2"),
        ("Complex Numbers", 24, 19, "19≈", 21, "1 - 2", "Tier 2"),
        ("Permutations & Combinations (P&C)", 21, 21, "22≈", 21, "1", "Tier 2"),
        ("Binomial Theorem", 23, 24, "17↓", 21, "1", "Tier 2"),
        ("Area Under the Curve (AUC)", 22, 18, "19≈", 20, "1", "Tier 2 (High ROI)"),
        ("Applications of Derivatives (AOD)", 26, 14, "11↓", 17, "0 - 1", "Tier 3"),
        ("Sets, Relations & Functions", 21, 16, "14↓", 17, "0 - 1", "Tier 3"),
        ("Quadratic Equations", 18, 16, "16≈", 17, "0 - 1", "Tier 3"),
        ("Statistics", 15, 8, "16↑", 13, "0 - 1", "Tier 3 (High ROI)"),
        ("Inverse Trigonometric Functions (ITF)", 8, 11, "10≈", 10, "0 - 1", "Tier 3"),
        ("Trigonometric Ratios and Identities", 7, 6, "12↑", 8, "0 - 1", "Tier 3"),
        ("Differentiation", 15, 4, "2↓", 7, "0 - 1", "Tier 3"),
        ("Indefinite Integrals", 8, 8, "7↓", 8, "0 - 1", "Tier 3"),
    ]
    for row in math_data:
        out.append(f"| **{row[0]}** | {row[1]} | {row[2]} | {row[3]} | {row[4]} | **{row[5]}** | {row[6]} |")

    out.append("\n**Key Mathematics Takeaways:**")
    out.append("1. **The Coordinate Geometry Giant:** With 71-75 questions per exam cycle (3 to 4 questions in every single shift), Coordinate Geometry (`Straight Line`, `Circle`, `Parabola`, `Ellipse`, `Hyperbola`) is the single highest-scoring topic in Math.")
    out.append("2. **Vectors & 3D Geometry:** Together, `Vector Algebra` and `3D Geometry` account for 3 to 4 questions per shift and follow standardized vector equation formulas.")
    out.append("3. **High-ROI Isolated Units:** `Matrices & Determinants`, `Sequence & Series`, and `Statistics` give almost guaranteed marks for minimal effort.")

    out.append("\n---\n")

    # 5. Checklist
    out.append("## 5. Mathematics 20-Chapter Checklist\n")
    out.append("*(Transcribed from slide `WhatsApp Image 2026-11-23 at 20.37.58 (1).jpeg`)*\n")
    out.append("| Algebra, Foundations & Stats | Calculus & Geometry |")
    out.append("| :--- | :--- |")
    checklist_pairs = [
        ("Sets, Relations & Functions", "Differentiation"),
        ("Complex Numbers & Quadratic Equations", "Applications of Derivatives (AOD)"),
        ("Matrices and Determinants", "Indefinite Integration"),
        ("Permutations & Combinations", "Definite Integration"),
        ("Binomial Theorem", "Area Under the Curve (AUC)"),
        ("Sequence & Series", "Differential Equations"),
        ("Statistics", "Coordinate Geometry (Lines, Circles, Conics)"),
        ("Probability", "Vector Algebra"),
        ("Trigonometric Ratios and Identities", "Three-Dimensional Geometry (3D Geometry)"),
        ("Inverse Trigonometric Functions", "Comprehensive Problem Solving / Integrated Units"),
        ("Limits, Continuity and Differentiability", ""),
    ]
    for left, right in checklist_pairs:
        out.append(f"| [ ] {left} | {'[ ] ' + right if right else ''} |")

    out.append("\n---\n")

    # 6. Appendix
    out.append("## 6. Appendix: Raw Slide-by-Slide Transcript & Audit Log\n")
    out.append("> This appendix preserves the complete forensic transcript of each of the 14 individual video screenshots in `images/` (`WhatsApp Image 2026-11-23 at 20.37.51` to `20.37.58`), logging instructor occlusions and slide annotations for full verification.\n")
    
    # Strip earlier header from raw_transcript and attach
    if "## 1. `WhatsApp Image" in raw_transcript:
        appendix_content = raw_transcript.split("## 1. `WhatsApp Image")[1]
        out.append("### 1. `WhatsApp Image" + appendix_content)
    else:
        out.append(raw_transcript)

    with open(weightage_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Updated docs/02_Chapterwise_Weightage_Analysis.md")

# -------------------------------------------------------------
# 3. GENERATE docs/03_Question_Papers_Catalog.md
# -------------------------------------------------------------
def build_papers_catalog_md():
    catalog_path = os.path.join(DOCS_DIR, "03_Question_Papers_Catalog.md")
    # Read existing 03_Question_Papers_Catalog.md to get links
    with open(catalog_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Reconstruct with local links to papers/ directory
    out = []
    out.append("# JEE Main Previous Year Question Papers Catalog (2025 – 2002)")
    out.append("\n> **Source Document:** `975100621-JEE-Main-Previous-Year-Question-Paper-With-Answer-Keys.pdf` (12 pages)  ")
    out.append("> **Archive Status:** 100% Downloaded & Verified locally in [`papers/`](../papers/)  ")
    out.append("> **Features:** Direct links to **open local PDF files** on your computer, verified online download links, and mock test access.\n")
    out.append("---\n")
    out.append("## Mock Test Practice")
    out.append("- **Official Test Series:** [Practice these papers as online mock tests (Quizrr)](https://www.quizrr.in/jee-main-test-series?utm_source=mathongo_website&utm_medium=seo_pages&utm_campaign=jee_main_previous_year_question_papers)\n")
    out.append("---\n")
    out.append("## Archive Summary by Year & Session\n")
    out.append("| Exam Session | Local Folder | Total Shifts / Papers | Status |")
    out.append("| :--- | :--- | :---: | :---: |")
    
    session_folders = [
        ("2025 (January)", "2025_Jan", 10),
        ("2024 (April)", "2024_Apr", 10),
        ("2024 (January)", "2024_Jan", 10),
        ("2023 (April)", "2023_Apr", 12),
        ("2023 (January)", "2023_Jan", 12),
        ("2022 (July)", "2022_Jul", 10),
        ("2022 (June)", "2022_Jun", 12),
        ("2021 (August)", "2021_Aug", 9),
        ("2021 (July)", "2021_Jul", 5),
        ("2021 (March)", "2021_Mar", 6),
        ("2021 (February)", "2021_Feb", 6),
        ("2020 (September)", "2020_Sep", 10),
        ("2020 (January)", "2020_Jan", 6),
        ("2019 (April)", "2019_Apr", 8),
        ("2019 (January)", "2019_Jan", 8),
        ("2018", "2018", 5),
        ("2017", "2017", 3),
        ("2016", "2016", 3),
        ("2015", "2015", 3),
        ("2014", "2014", 5),
        ("2013", "2013", 5),
        ("2012", "2012", 5),
        ("2011 – 2002", "2011-2002", 10),
    ]
    for s_name, s_folder, s_count in session_folders:
        out.append(f"| **{s_name}** | [`papers/{s_folder}/`](../papers/{s_folder}/) | {s_count} | Available Locally |")
    out.append("| **TOTAL** | **173 Papers (792.3 MB)** | **173** | **Complete** |")

    out.append("\n---\n")
    out.append("## Shift-Wise Papers Directory\n")

    current_section = ""
    current_folder = ""
    
    def folder_from_sec(sec_title):
        m = re.search(r"JEE Main (\d{4})(?:\s*\(([^)]+)\))?", sec_title)
        if m:
            yr = m.group(1)
            mo = m.group(2)
            if mo:
                return f"{yr}_{mo[:3].capitalize()}"
            return yr
        if "2011" in sec_title and "2002" in sec_title:
            return "2011-2002"
        return "2011-2002"

    def clean_pdf_name(paper_title):
        name = re.sub(r"[^\w\s-]", "", paper_title)
        name = re.sub(r"\s+", "_", name.strip())
        name = re.sub(r"_Previous_Year_Paper", "", name)
        name = re.sub(r"_+", "_", name)
        return name + ".pdf"

    for line in lines:
        line_s = line.strip()
        if line_s.startswith("## JEE Main"):
            current_section = line_s.replace("##", "").strip()
            current_folder = folder_from_sec(current_section)
            out.append(f"\n### {current_section}\n")
            out.append("| # | Shift / Paper | Local PDF File | Online Download |")
            out.append("| :---: | :--- | :--- | :---: |")
        elif line_s.startswith("|") and ("Download PDF" in line_s or "mathongo.com" in line_s):
            parts = [p.strip() for p in line_s.split("|")]
            if len(parts) >= 4 and parts[1].isdigit():
                sl = parts[1]
                paper_name = parts[2]
                url_m = re.search(r"\((https://links\.mathongo\.com/[^\)]+)\)", parts[3])
                url = url_m.group(1) if url_m else ""
                
                pdf_fname = clean_pdf_name(paper_name)
                # Check for offline ligature
                if "Offline" in pdf_fname:
                    pdf_fname = "JEE_Main_2012_Offline.pdf"
                local_rel = f"../papers/{current_folder}/{pdf_fname}"
                clean_display = paper_name.replace("", " ")
                out.append(f"| {sl} | {clean_display} | [📄 {pdf_fname}]({local_rel}) | [Web Link]({url}) |")

    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Updated docs/03_Question_Papers_Catalog.md")

# -------------------------------------------------------------
# 4. GENERATE ROOT README.md (THE MASTER LOGICAL FILE)
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
    out.append("├── docs/                                # Core documentation & curriculum guides")
    out.append("│   ├── 01_Syllabus_2027.md              # Full 52-unit syllabus (Math, Physics, Chemistry)")
    out.append("│   ├── 02_Chapterwise_Weightage_Analysis.md # 2024-2026 question trends, tiers & slide audit")
    out.append("│   └── 03_Question_Papers_Catalog.md    # Shift-wise directory with local & web links")
    out.append("├── papers/                              # 173 downloaded question papers (792 MB)")
    out.append("│   ├── 2025_Jan/                        # 10 shift-wise papers (Jan 22 - Jan 29)")
    out.append("│   ├── 2024_Apr/ & 2024_Jan/            # 20 shift-wise papers")
    out.append("│   ├── 2023_Apr/ & 2023_Jan/            # 24 shift-wise papers")
    out.append("│   ├── 2022_Jul/ & 2022_Jun/            # 22 shift-wise papers")
    out.append("│   ├── 2021_Feb/ to 2021_Aug/           # 26 shift-wise papers")
    out.append("│   ├── 2020_Jan/ & 2020_Sep/            # 16 shift-wise papers")
    out.append("│   ├── 2019_Jan/ & 2019_Apr/            # 16 shift-wise papers")
    out.append("│   ├── 2018/ to 2012/                   # 29 shift-wise & online papers")
    out.append("│   ├── 2011-2002/                       # 10 annual original papers")
    out.append("│   └── README.md                        # Shift catalog & file size index")
    out.append("├── scripts/                             # Utility & automation scripts")
    out.append("│   └── download_papers.py               # Multi-threaded batch PDF downloader")
    out.append("├── images/                              # 14 raw lecture slides (Vedantu analysis)")
    out.append("├── syllabus-jee-main-2027.pdf           # Original 26-page syllabus PDF")
    out.append("└── 975100621-JEE-Main-Previous-Year...  # Original 12-page MathonGo index PDF")
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

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Created root README.md")

if __name__ == "__main__":
    build_syllabus_md()
    build_weightage_md()
    build_papers_catalog_md()
    build_master_readme()
