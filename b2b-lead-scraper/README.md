# 📊 B2B Data Scraper & Formatter

An automated Python web scraping tool built with `requests`, `BeautifulSoup`, and `pandas` that extracts business directory data, cleans raw HTML strings, and exports structured datasets to CSV format.

---

## 🚀 Features
- **HTTP Request Handling:** Custom User-Agent headers to ensure clean HTTP handshake requests.
- **HTML Parsing:** Extracts structured elements (titles, categories, metadata) using `BeautifulSoup`.
- **Dataset Export:** Formats extracted data automatically into a ready-to-use CSV spreadsheet (`leads.csv`) using `pandas`.
- **Throttling Protection:** Includes built-in delay loops (`time.sleep`) to respect host server rate limits.

---

## 🛠️ Prerequisites
- **Python 3.8+** installed on your machine.

---

## 📁 Repository Layout
```text
02-b2b-lead-scraper/
├── scraper.py           # Main scraping script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚙️ Setup & Local Execution

1. **Navigate into the project folder:**
   ```bash
   cd 02-b2b-lead-scraper
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper:**
   ```bash
   python scraper.py
   ```

4. **View Output:**
   - Once execution finishes, check the folder for a newly generated file named `leads.csv`.

---

## 📝 License
This project is open-source and available under the [MIT License](../LICENSE).
