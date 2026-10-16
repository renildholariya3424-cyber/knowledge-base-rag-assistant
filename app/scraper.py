import ipaddress
import re
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def _validate_public_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Please provide a complete http:// or https:// URL.")
    host = parsed.hostname.lower()
    if host in {"localhost", "localhost.localdomain"}:
        raise ValueError("Local URLs are not supported. Use a public article URL.")
    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
            }
        except socket.gaierror:
            addresses = set()
    for address in addresses:
        if not address.is_global:
            raise ValueError("Private or non-public network addresses are not supported.")
    return url.strip()


def scrape_article(url: str, timeout: int = 20) -> dict[str, str]:
    url = _validate_public_url(url)
    response = requests.get(
        url, headers={"User-Agent": "KnowledgeBaseQABot/1.0 (educational demo)"},
        timeout=timeout, allow_redirects=True,
    )
    response.raise_for_status()
    final_url = _validate_public_url(response.url)
    if "text/html" not in response.headers.get("content-type", "").lower():
        raise ValueError("This URL did not return an HTML page.")
    soup = BeautifulSoup(response.text, "html.parser")
    for node in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
        node.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else urlparse(final_url).netloc
    main = soup.find("article") or soup.find("main") or soup.body or soup
    parts = [re.sub(r"\s+", " ", node.get_text(" ", strip=True))
             for node in main.find_all(["p", "li", "h1", "h2", "h3"])]
    text = "\n".join(part for part in parts if len(part) > 25)
    if len(text) < 150:
        text = re.sub(r"\s+", " ", main.get_text(" ", strip=True))
    if len(text) < 100:
        raise ValueError("Not enough readable article text was found on this page.")
    return {"url": final_url, "title": title[:300], "text": text}
