import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_leads():
    # User-Agent header makes your request mimic a standard browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    target_url = "https://quotes.toscrape.com"
    print(f"📡 Fetching target directory: {target_url}...")

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ HTTP Error. Status Code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        extracted_data = []

        # Find all HTML container blocks
        items = soup.find_all("div", class_="quote")
        print(f"🔍 Found {len(items)} entries. Extracting data...")

        for item in items:
            text = item.find("span", class_="text").get_text(strip=True).strip('“”')
            author = item.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in item.find_all("a", class_="tag")]

            extracted_data.append({
                "Company / Author": author,
                "Quote / Details": text,
                "Categories": ", ".join(tags),
                "Scraped At": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Small delay between parsing items to mimic human activity
            time.sleep(0.2)

        # Export dataset using Pandas
        df = pd.DataFrame(extracted_data)
        output_filename = "leads.csv"
        df.to_csv(output_filename, index=False)
        print(f"✅ Success! Exported {len(extracted_data)} structured rows to '{output_filename}'.")

    except Exception as e:
        print(f"❌ An error occurred during extraction: {str(e)}")

if __name__ == "__main__":
    scrape_leads()