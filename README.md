# NamUs Missing Persons Data Scraper

## 📌 Overview
This project is a Python-based OSINT automation tool that scrapes publicly available missing persons case listings from the **NamUs (National Missing and Unidentified Persons System)** website.

It was originally developed during my internship at **Paradigm Intelligence** to support research workflows related to missing children investigations.

---

## 🚀 Features
- Automated scraping of NamUs missing persons listings
- Filters cases by:
  - State
  - Age range
- Pagination support
- Downloads associated case images
- Saves results in structured JSON format

---

## 🛠 Tech Stack
- Python 3
- Selenium (dynamic automation)
- BeautifulSoup4 (HTML parsing)
- Requests (image downloading)

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Harshath132001/Namus.git
cd Namus

Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run scraper with CLI arguments:

python src/run_scraper.py --state Texas --min-age 6 --max-age 16

📂 Output

Results are saved in:

output/<STATE>_results.json

output/<STATE>_images/

Example JSON entry:

{
  "result_number": 1,
  "state": "Texas",
  "raw_text": "Missing Person ...",
  "image_file": "output/Texas_images/case_1.jpg"
}

⚠️ Disclaimer

This project is intended strictly for educational and research purposes.

It only collects publicly available information and must not be used for unlawful, unethical, or privacy-violating activities.

👤 Author

Harshath EM
MS Cybersecurity Student | CompTIA Security+ Certified


---

# ✅ FILE 6: LICENSE

On GitHub:

Add file → LICENSE → Select **MIT License**

---

# ✅ FINAL UPLOAD INSTRUCTIONS (Cleanest Way)

1. Delete old repo
2. Create fresh repo with README + MIT
3. Upload these files all at once
4. Commit message:



Initial professional NamUs scraper project setup


---

# ⭐ RESULT

After this, recruiters will see:

✅ Real OSINT automation project  
✅ Internship-based tool  
✅ Clean repo structure  
✅ CLI usage  
✅ Proper documentation  
✅ Ethical disclaimer  

---

If you want, next I can give you the **exact LinkedIn post** to announce this project professionally.
