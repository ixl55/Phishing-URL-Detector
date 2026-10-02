from app.core.extractor import extract_urls, refang


def test_extracts_urls_from_sms():
    text = (
        "عميلنا العزيز، تم إيقاف حسابك. لتحديث البيانات اضغط: https://alrajhi-update.top/login، "
        "أو زر www.example.com. Track: bit.ly/3xYz!"
    )
    assert extract_urls(text) == [
        "https://alrajhi-update.top/login",
        "www.example.com",
        "bit.ly/3xYz",
    ]


def test_refangs_defanged_links():
    assert refang("hxxps://evil[.]com/path") == "https://evil.com/path"
    assert extract_urls("see hxxp://bad(.)tk/x and hxxps://evil[.]com") == ["http://bad.tk/x", "https://evil.com"]


def test_deduplicates_and_limits():
    text = " ".join(["https://a.com"] * 3 + [f"https://site{i}.com" for i in range(10)])
    urls = extract_urls(text, limit=5)
    assert urls[0] == "https://a.com"
    assert len(urls) == 5


def test_strips_trailing_punctuation_and_parentheses():
    assert extract_urls("(see https://example.com/page).") == ["https://example.com/page"]


def test_no_urls():
    assert extract_urls("hello world, no links here") == []
