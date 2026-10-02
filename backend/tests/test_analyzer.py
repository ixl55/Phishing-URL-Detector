import pytest

from app.core.analyzer import InvalidUrlError, analyze_url, parse_url


def rule_ids(url: str) -> set[str]:
    return {f.rule_id for f in analyze_url(url).findings}


@pytest.mark.parametrize(
    "url",
    [
        "https://www.google.com",
        "https://accounts.google.com/signin",
        "https://www.alrajhibank.com.sa",
        "https://github.com/python/cpython",
        "https://www.amazon.sa/dp/B0001",
        "https://login.microsoftonline.com/common/oauth2/authorize",
        "https://web.whatsapp.com",
        "https://en.wikipedia.org/wiki/Phishing",
        "https://www.paypal.com/signin",
        "https://www.applebees.com",
        "example.com",
    ],
)
def test_legitimate_urls_are_safe(url):
    result = analyze_url(url)
    assert result.verdict == "safe", [f.rule_id for f in result.findings]


@pytest.mark.parametrize(
    "url",
    [
        "http://192.168.0.1/paypal/login",
        "http://paypal.com@evil.tk",
        "https://secure-paypal.com.verify-account.xyz/login",
        "http://xn--pple-43d.com",
        "http://g00gle-verify.tk",
        "https://paypa1.com/signin",
        "javascript:alert(1)",
        "http://3232235777/account/verify",
    ],
)
def test_phishing_urls_are_dangerous(url):
    result = analyze_url(url)
    assert result.verdict == "dangerous", (result.score, [f.rule_id for f in result.findings])


@pytest.mark.parametrize(
    "url",
    ["https://bit.ly/3abcd", "http://example.com:8080/", "https://example.xyz"],
)
def test_medium_risk_urls_are_not_safe_or_flagged(url):
    result = analyze_url(url)
    assert result.findings


def test_score_is_capped_and_findings_sorted():
    result = analyze_url("http://paypal.com@192.168.1.1:8080/secure-login/verify-account/update.exe")
    assert result.score == 100
    severities = [f.severity for f in result.findings]
    order = {"high": 0, "medium": 1, "low": 2}
    assert severities == sorted(severities, key=order.get)


def test_scheme_is_added_when_missing():
    parsed = parse_url("www.example.com/path")
    assert parsed.scheme == "http"
    assert parsed.had_scheme is False
    assert "no_https" not in rule_ids("www.example.com/path")


def test_registered_domain_with_multi_part_suffix():
    parsed = parse_url("https://online.alrajhibank.com.sa/login")
    assert parsed.registered_domain == "alrajhibank.com.sa"
    assert parsed.subdomain == "online"
    assert parsed.suffix == "com.sa"


def test_punycode_is_decoded_for_display():
    result = analyze_url("http://xn--pple-43d.com")
    assert result.host_display == "аpple.com"


@pytest.mark.parametrize("bad", ["", "   ", "not a url", "http://", "mailto:someone@example.com", "localhost:abc"])
def test_invalid_input_raises(bad):
    with pytest.raises(InvalidUrlError):
        analyze_url(bad)


def test_messages_are_bilingual():
    for finding in analyze_url("http://paypal.com@evil.tk").findings:
        assert finding.title["ar"] and finding.title["en"]
        assert finding.detail["ar"] and finding.detail["en"]
        assert "{" not in finding.detail["ar"] + finding.detail["en"]
