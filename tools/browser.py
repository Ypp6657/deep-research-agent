import httpx
from bs4 import BeautifulSoup


def fetch_page(url: str, timeout: int = 20) -> str:
    """
    Fetch a webpage and return cleaned text.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
        )
    }

    response = httpx.get(
        url,
        headers=headers,
        timeout=timeout,
        follow_redirects=True,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(
        ["script", "style", "noscript", "header", "footer", "nav", "aside"]
    ):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return " ".join(text.split())