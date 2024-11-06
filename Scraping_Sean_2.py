import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://orbilu.uni.lu/handle/10993/8713"

# Send GET request to the webpage
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print the entire HTML content of the page
    print(soup.prettify())  # Pretty-prints the entire HTML structure
else:
    print(f"Failed to retrieve the page")
