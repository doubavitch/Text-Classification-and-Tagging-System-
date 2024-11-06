import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define base URL and initialize an empty list for records
base_url = "https://orbilu.uni.lu/handle/10993/..."
all_records = []

# Loop through each page
for page_num in range(8700, 8750):
    url = f"{base_url}?page={page_num}"  # Adjust according to the site's URL pattern

    # Fetch page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find records
    rows = soup.find_all('div', class_='row')

    record = {}
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

    # Add the record to the list if it has content
    if record:
        all_records.append(record)

    # Respectful delay to avoid overloading the server
    time.sleep(1)

# Convert list to DataFrame and save to CSV
df = pd.DataFrame(all_records)
df.to_csv("scraped_data_test.csv", index=False)
print("Data saved to scraped_data_test.csv")
