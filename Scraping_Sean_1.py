import requests
from bs4 import BeautifulSoup

# Define the base URL and the range of numbers to scrape
base_url = "https://orbilu.uni.lu/handle/10993/"

# Loop through the numbers from 1 to 20000
for i in range(1, 200):
    url = base_url + str(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the page (you can modify this based on the structure of the page)
        text = soup.get_text()
        print(f"Content from page {i}:\n{text}\n")
    else:
        print(f"Failed to retrieve page {i}")
