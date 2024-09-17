import urllib.robotparser


def can_scrape(url: str, user_agent: str = "*") -> bool:
    # Create an instance of the robot parser
    rp = urllib.robotparser.RobotFileParser()

    # Parse the robots.txt file of the website
    rp.set_url(url + "/robots.txt")
    rp.read()

    # Check if scraping is allowed for the given user agent
    return rp.can_fetch(user_agent, url)


def main() -> None:
    website_url = "https://www.wikipedia.com"
    user_agent = "*"

    if can_scrape(website_url, user_agent):
        print(f"Scraping is allowed on {website_url} for user agent '{user_agent}'.")
    else:
        print(
            f"Scraping is not allowed on {website_url} for user agent '{user_agent}'."
        )


if __name__ == "__main__":
    main()
