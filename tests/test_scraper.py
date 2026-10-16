import pytest
from app.scraper import scrape_article

def test_invalid_url_is_rejected():
    with pytest.raises(ValueError):
        scrape_article("file:///etc/passwd")

def test_url_without_scheme_is_rejected():
    with pytest.raises(ValueError):
        scrape_article("docs.python.org")
