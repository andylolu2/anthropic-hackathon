import warnings

import requests
from bs4 import BeautifulSoup, Comment

from claude import Claude
from prompts import CLEAN_HTML_PROMPT


def scrape(url: str, render_js: bool = False):
    if render_js:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            html = page.content()
            browser.close()
    else:
        response = requests.get(url)
        html = response.text

    return html


def clean_html(html: str, claude):
    soup = BeautifulSoup(html, "html.parser")

    # remove all scripts, styles, headers, navigation, footer, svg paths
    for script in soup(["script", "style", "nav", "path"]):
        script.extract()

    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # get the roughly-cleaned html
    small_html = soup.prettify()

    # ask claude to clean it up
    result = claude.ask_claude_md(CLEAN_HTML_PROMPT.format(html=small_html))

    assert "NO CONTENT" not in result, "No content found."

    return result


def query_medwise(query: str = "HIV testing", k: int = 1, render_js: bool = False):
    claude = Claude()
    MEDWISE = "https://ask.medwise.ai/api/ask"

    body = {
        "q": query,
        "product": "main",
        "sources": "NICE CKS,NICE Guidelines,GP notebook",
    }

    post = requests.post(MEDWISE, json=body)
    results = post.json()["results"]

    urls = [result["online_view_url"] for result in results]

    results = []
    for url in urls:
        if url.endswith(".pdf"):  # skip pdfs
            continue
        if len(results) >= k:
            break

        try:
            html = scrape(url, render_js=render_js)
            content = clean_html(html, claude)
            results.append({"url": url, "content": content})
        except Exception as e:
            warnings.warn(f"Could not scrape {url}: {repr(e)}")

    if len(results) < k:
        warnings.warn(f"Only got {len(results)} results, but asked for {k}.")

    return results


if __name__ == "__main__":
    results = query_medwise("causes of tuberculosis", k=3)

    for result in results:
        print(result["url"])
        print(result["content"])
        print()
