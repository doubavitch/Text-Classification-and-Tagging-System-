import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize an empty list for all records
all_records = []

# Loop through the range of pages from 8713 to 8800
for page_num in range(1, 10000):
    url = f"https://orbilu.uni.lu/handle/10993/{page_num}"

    # Send GET request
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize a dictionary to store the data
        record = {"URL": url}

        # Find relevant rows for title, abstract, keywords, disciplines, and language
        rows = soup.find_all('div', class_='row')

        for row in rows:
            label = row.find('div', class_='col-12 col-md-3 font-weight-bold text-left text-md-right pr-0')
            content = row.find('div', class_='col-12 col-md-9')

            if label and "Title" in label.text:
                record["Title"] = content.get_text(strip=True)
            elif label and "Abstract" in label.text:
                record["Abstract"] = content.get_text(strip=True)
            elif label and "Keywords" in label.text:
                record["Keywords"] = content.get_text(strip=True)
            elif label and "Disciplines" in label.text:
                record["Disciplines"] = content.get_text(strip=True)
            elif label and "Language" in label.text:
                language = content.get_text(strip=True)
                if "English" in language:  # Only save if the language is English
                    record["Language"] = language

        # Add the record to the list if it has content and the language is English
        if "Language" in record:
            all_records.append(record)

    else:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")

# Save all records to CSV
if all_records:
    df = pd.DataFrame(all_records)
    df.to_csv("scraped_1_10000.csv", index=False)
    print("Data saved to scraped_1_10000.csv")
else:
    print("No data found.")
