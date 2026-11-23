import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAPERS_DIR = os.path.join(BASE_DIR, "papers")
MD_FILE = os.path.join(BASE_DIR, "Gemini", "JEE_Main_Previous_Year_Question_Papers.md")

def parse_section_name(raw_title):
    raw_title = raw_title.replace("### Download", "").replace("Previous Year Queson Papers", "").replace("Previous Year Question Papers", "").strip()
    # Normalize section names into clean folder names
    # e.g. "JEE Main 2025 (January)" -> "2025_Jan"
    m = re.search(r"JEE Main (\d{4})(?:\s*\(([^)]+)\))?", raw_title)
    if m:
        year = m.group(1)
        month = m.group(2)
        if month:
            # take first 3 chars of month
            clean_month = month[:3].capitalize()
            return f"{year}_{clean_month}"
        return year
    if "2011" in raw_title and "2002" in raw_title:
        return "2011-2002"
    cleaned = re.sub(r"[^\w-]", "_", raw_title)
    return cleaned

def sanitize_filename(paper_name):
    # e.g. "JEE Main 2025 (22 Jan Shift 1) Previous Year Paper" -> "JEE_Main_2025_22_Jan_Shift_1.pdf"
    name = re.sub(r"[^\w\s-]", "", paper_name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_Previous_Year_Paper", "", name)
    name = re.sub(r"_+", "_", name)
    return name + ".pdf"

def extract_papers():
    with open(MD_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_section = "General"
    papers = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("### Download"):
            current_section = line
        elif line.startswith("|") and "[Download PDF]" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                sl = parts[1]
                paper_name = parts[2]
                link_m = re.search(r"\((https://links\.mathongo\.com/[^\)]+)\)", parts[3])
                if link_m:
                    link = link_m.group(1)
                    folder = parse_section_name(current_section)
                    filename = sanitize_filename(paper_name)
                    papers.append({
                        "sl": sl,
                        "paper_name": paper_name,
                        "link": link,
                        "folder": folder,
                        "filename": filename
                    })
    return papers

def resolve_mathongo_link(link):
    # Follow redirect to get Google Drive URL
    req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        final_url = resp.geturl()
    
    # Extract file ID
    # Pattern: /file/d/([a-zA-Z0-9_-]+)
    m = re.search(r"/file/d/([a-zA-Z0-9_-]+)", final_url)
    if m:
        return m.group(1)
    # Pattern: id=([a-zA-Z0-9_-]+)
    m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", final_url)
    if m:
        return m.group(1)
    return None

def download_file_from_drive(file_id, dest_path):
    # Try usercontent download first
    download_urls = [
        f"https://drive.usercontent.google.com/download?id={file_id}&export=download",
        f"https://drive.google.com/uc?export=download&id={file_id}"
    ]
    
    for url in download_urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                # Check magic bytes for PDF
                if data.startswith(b"%PDF"):
                    with open(dest_path, "wb") as f:
                        f.write(data)
                    return True, len(data)
                elif b"confirm=" in data:
                    # Parse confirm code
                    m = re.search(r"confirm=([0-9A-Za-z_]+)", data.decode("utf-8", errors="ignore"))
                    if m:
                        confirm_code = m.group(1)
                        confirm_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm={confirm_code}"
                        req2 = urllib.request.Request(confirm_url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req2, timeout=30) as resp2:
                            data2 = resp2.read()
                            if data2.startswith(b"%PDF"):
                                with open(dest_path, "wb") as f:
                                    f.write(data2)
                                return True, len(data2)
        except Exception as e:
            continue
    return False, 0

def process_paper(paper):
    folder_path = os.path.join(PAPERS_DIR, paper["folder"])
    os.makedirs(folder_path, exist_ok=True)
    dest_path = os.path.join(folder_path, paper["filename"])
    
    # Check if exists and valid
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        with open(dest_path, "rb") as f:
            if f.read(4) == b"%PDF":
                return paper["filename"], True, os.path.getsize(dest_path), "already exists"
    
    # Resolve Drive ID
    drive_id = None
    for attempt in range(3):
        try:
            drive_id = resolve_mathongo_link(paper["link"])
            if drive_id:
                break
        except Exception:
            time.sleep(1 + attempt)
            
    if not drive_id:
        return paper["filename"], False, 0, f"failed to resolve link {paper['link']}"
    
    # Download
    for attempt in range(3):
        success, size = download_file_from_drive(drive_id, dest_path)
        if success:
            return paper["filename"], True, size, "downloaded"
        time.sleep(1 + attempt)
        
    return paper["filename"], False, 0, f"download failed for drive id {drive_id}"

def main():
    papers = extract_papers()
    print(f"Total papers found to download: {len(papers)}")
    os.makedirs(PAPERS_DIR, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    total = len(papers)
    start_time = time.time()
    
    print("Starting downloads with ThreadPoolExecutor (max_workers=6)...")
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_paper = {executor.submit(process_paper, p): p for p in papers}
        for idx, future in enumerate(as_completed(future_to_paper), 1):
            fname, ok, size, status = future.result()
            if ok:
                success_count += 1
                size_mb = size / (1024 * 1024)
                print(f"[{idx}/{total}] SUCCESS: {fname} ({size_mb:.2f} MB, {status})")
            else:
                fail_count += 1
                print(f"[{idx}/{total}] FAILED: {fname} ({status})")
                
    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed:.1f}s! Successfully downloaded: {success_count}/{total}, Failed: {fail_count}")

if __name__ == "__main__":
    main()
