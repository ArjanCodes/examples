import requests
from bs4 import BeautifulSoup


def main():
    url = "https://arjancodes.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all the links
    for link in soup.find_all("a"):
        print(link.get("href"))


if __name__ == "__main__":
    main()
