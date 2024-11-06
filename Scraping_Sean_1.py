import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize an empty list for all records
all_records = []
page_count = 0  # Counter to track the number of pages processed

# Loop through the range of pages from 1 to 80000
for page_num in range(1, 80000):
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

        # Add the record to the list if it has content and the language is English, and abstract is not empty
        if "Language" in record and "Abstract" in record and record["Abstract"]:
            all_records.append(record)

        # Update the page counter
        page_count += 1

        # Save to CSV every 500 pages
        if page_count % 500 == 0:
            df = pd.DataFrame(all_records)
            df.to_csv(f"scraped_page_{page_count}.csv", index=False)
            print(f"Saved data from {page_count} pages to scraped_page_{page_count}.csv")
            all_records = []  # Reset the list after saving

    else:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")

# Save any remaining records if pages left after the loop
if all_records:
    df = pd.DataFrame(all_records)
    df.to_csv(f"scraped_page_{page_count}.csv", index=False)
    print(f"Saved the final data from {page_count} pages to scraped_page_{page_count}.csv")
else:
    print("No data found.")
