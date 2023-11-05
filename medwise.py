import warnings

import requests
from bs4 import BeautifulSoup, Comment
from llm_diag import Claude
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

    return result


def query_medwise(query: str = "HIV testing", k: int = 1, render_js: bool = False):
    claude = Claude()
    MEDWISE = "https://ask.medwise.ai/api/ask"

    body = {
        "q": query,
        "product": "main",
        "sources": "NICE CKS,NICE Guidelines,custom:gAAAAABlFsfVaNVerb3WACPpggH5x7r5JXuHN7ppGVWiWa7oom5Kff1fRUABBXuNLZIMjoc1ZvGXDQM8yidoljN6kG6ep0k2oA1gwIs4ds5aRSWbGuYtNxpAuU4kM_aD8kaH8d99bZZK,Dermnet NZ,custom:gAAAAABkgISwXSuSfTr6IcHBRlbiUEZdCyWpFRRJXQu5egxi3NTvstxoHjK5C6zhdaV3MFEAmO6VSW9g0_hXll_UL8mcez6MN0B7UEpTw9z0WFIvF7wSc-U=,FSRH,Patient.info,GP notebook,custom:gAAAAABilObmOrsvO3l-V4iEE-fILic1lyVn1v3tNKIMkWNee-3kImOShGL9otB4QTdBwMTeNFiS2sx8G6moWXR2taThIyFs6-YrJeYwUJxFNdLiXuH_Ngf7DMp2DBEuaNYYlUQ8_14i,custom:gAAAAABioJx5uI3h90fKn9FVB_ZeA-nSYLIZlzeOlVkNwZAHp0aGJYevS2IKoUd561GuKrBnEVjHpfVDp1WoNh13Nb_U1cppD3niTmFRJeVFtmU0mYOkVcyLDgWX6q1RrnVd3DyiRF4r2cRq48rXrjCPj56CywiI_Q==,custom:gAAAAABioJ0FjSD0LB7GOD-FwiEmbG20xcJUrOqHLjxw205cDhgAWI31p4lx8LjrcFq8J2PZBHFlFUlDzATsaXS1_Lub6wrtPWUU4TInFWS0jTETL5uQD9E=,custom:gAAAAABiVuqaDzZ-GYYmm0zAH-VYTxI0fUhCJxIb4qzi3PLtHrDH_KFusqBkPc9DkAx-lOKRjbc6ZqPeyjt9VjZzRzVVYoOAM-tr2rI_si-KFpyHuuHrXn82AqSDf8m_oGv4zPWoNwq1zwgkeOuigw5UQGVB5h8RmgsDrSWENpIXICN_FynpnUE=,custom:gAAAAABioKHXxwgVcrQ6Rzs6pkuSCjAGo6Vuy9-JG6O8muQfUO-dxmAMybaAty7u7h2-yu85JkcuLbLkL-miE-dYVOdKlNAhERhQ6gd3MGOpJwVcnfe1yyk=,custom:gAAAAABijgOlJr4siI6iUMPJZsiaI4YgpnquE45terIsYVmNPumak5J_eylHbQVVT2N1-DScNO7UQ3k_-npNJ1mDzItbACc75sxoJNbE0evhOgb2bVinQrE=,custom:gAAAAABioJw05CF886qL5B_MOvp9YurjQYCIyE7vmECq90L7xVHVxq1F64kIRBkcpdbRESb_GrIag-nlinQ0JsIFczG7-2FURBAq15WVwmIVH8m8ZsETJKU=,custom:gAAAAABiwrZccrjJWqY3gO9RFEPLd58WNECZY47G-D6hfSWZc1A5DWcDUfshgmEoP1WrVQsOU8msrRTJSFYrf3VqFGQtJmw-EVQs0-zdB6DHYMq11e7uvxE=,custom:gAAAAABjwTpWbr78hyUHKcCEVq4qhNQZSxhwoxUf7jHvUkyrEUnNczxE81KWsJDPifi2ODytD3SJJcobXUinyy7GnBaBqB4KG6vls0D0rrUFoy7ASalnuGTe3M0HnpgKW7Nfsb9pjsFu",
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
            content = clean_html(html)
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
