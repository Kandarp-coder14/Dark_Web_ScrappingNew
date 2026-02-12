from dwti.parser import parse_html



def test_parse_html_extracts_title_links_indicators() -> None:
    html = """
    <html>
      <head><title>Threat Feed</title></head>
      <body>
        Contact admin@test.org
        Wallet: bc1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
        Mirror: abcdefghijklmnop.onion
        <a href="/next">Next</a>
      </body>
    </html>
    """

    parsed = parse_html("https://example.org/start", html)

    assert parsed.title == "Threat Feed"
    assert "https://example.org/next" in parsed.links
    assert "admin@test.org" in parsed.indicators
    assert "abcdefghijklmnop.onion" in parsed.indicators
