import requests
import re
import os

USERNAME = "vishnuas22"
REPO = "vishnuas22"

# Paths to your badge SVGs
BADGES = {
    "followers": "badges/futuristic-followers.svg",
    "stars": "badges/futuristic-stars.svg",
    "views": "badges/futuristic-profile-views.svg",  # For Komarev or similar
}

# Regex patterns to match the number text in your SVG badges.
SVG_PATTERNS = {
    "followers": r'(<text[^>]+x="170"[^>]*>)([^<]+)(</text>)',
    "stars": r'(<text[^>]+x="150"[^>]*>)([^<]+)(</text>)',
    "views": r'(<text[^>]+x="185"[^>]*>)([^<]+)(</text>)',
}

def get_followers():
    url = f"https://api.github.com/users/{USERNAME}"
    resp = requests.get(url)
    return resp.json().get("followers", 0)

def get_stars():
    url = f"https://api.github.com/users/{USERNAME}/repos"
    resp = requests.get(url)
    stars = sum([repo["stargazers_count"] for repo in resp.json() if not repo.get("fork")])
    return stars

def get_views():
    # For Komarev profile views badge, fetch from their API if available, else skip
    # This is a placeholder. Komarev does not provide an API, so you might need to update this manually or omit.
    return "∞"

def update_svg(file, pattern, count):
    with open(file, "r", encoding="utf-8") as f:
        svg = f.read()
    svg_new = re.sub(pattern, r"\1{}\3".format(count), svg)
    with open(file, "w", encoding="utf-8") as f:
        f.write(svg_new)

def main():
    print("Updating badges...")

    followers = get_followers()
    stars = get_stars()
    views = get_views()

    update_svg(BADGES["followers"], SVG_PATTERNS["followers"], followers)
    update_svg(BADGES["stars"], SVG_PATTERNS["stars"], stars)
    update_svg(BADGES["views"], SVG_PATTERNS["views"], views)

    print("Done!")

if __name__ == "__main__":
    main()
