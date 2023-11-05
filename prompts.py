CLEAN_HTML_PROMPT = """
Below is the HTML for a webpage on medical guidelines. Identify the main content of the page. Ignore all headings, footers, navigation blocks, and unimportant information. Try not to re-word the guidelines. Respond with a single whitespace if you don't think there is meaningful content (e.g. a 404 error / the HTML is not rendered properly).

<html>
{html}
</html>
""".strip()
