import pytest

from app.core import rules
from app.core.analyzer import parse_url
from app.core.domain import parse_ip


def fires(rule, url: str) -> bool:
    return rule(parse_url(url)) is not None


@pytest.mark.parametrize(
    "host,expected",
    [
        ("192.168.0.1", "192.168.0.1"),
        ("3232235777", "192.168.1.1"),
        ("0xC0A80101", "192.168.1.1"),
        ("0300.0250.01.01", "192.168.1.1"),
        ("[::1]", "::1"),
        ("example.com", None),
        ("1.com", None),
    ],
)
def test_parse_ip(host, expected):
    assert parse_ip(host) == expected


CASES = [
    (rules.ip_address, "http://10.0.0.5/login", "https://example.com"),
    (rules.at_symbol, "https://google.com@evil.com", "https://google.com/@user"),
    (rules.punycode, "http://xn--80ak6aa92e.com", "https://example.com"),
    (rules.mixed_script, "http://xn--pple-43d.com", "https://example.com"),
    (rules.brand_impersonation, "https://paypal-secure.example.net", "https://www.paypal.com/myaccount"),
    (rules.brand_impersonation, "https://appleid.apple.com.verify.io", "https://www.applebees.com"),
    (rules.brand_impersonation, "https://alrajhi-online.top/login", "https://www.alrajhibank.com.sa"),
    (rules.typosquatting, "https://rnicrosoft.com", "https://microsoft.com"),
    (rules.typosquatting, "https://amaz0n.com", "https://example.com"),
    (rules.typosquatting, "https://faceb00k-login.net", "https://facebook.com"),
    (rules.suspicious_tld, "https://free-gift.tk", "https://example.com"),
    (rules.shortener, "https://bit.ly/abc", "https://example.com/bit.ly"),
    (rules.many_subdomains, "https://a.b.c.example.com", "https://www.mail.example.com"),
    (rules.non_standard_port, "http://example.com:8080", "https://example.com:443"),
    (rules.embedded_redirect, "https://example.com/r?u=https://evil.com", "https://example.com/a/b"),
    (rules.embedded_redirect, "https://example.com/go//evil.com", "https://example.com/a/b"),
    (rules.https_in_domain, "https://https-secure-bank.com", "https://example.com/https"),
    (rules.dangerous_file, "https://example.com/invoice.exe", "https://example.com/report.pdf"),
    (rules.many_hyphens, "https://secure-login-update-account.com", "https://my-site.com"),
    (rules.sensitive_keywords, "https://example.com/verify/account", "https://example.com/about"),
    (rules.long_url, "https://example.com/" + "a" * 80, "https://example.com/short"),
    (rules.no_https, "http://example.com", "https://example.com"),
    (rules.obfuscation, "https://example.com/%70%61%79%70%61%6c", "https://example.com/a%20b"),
]


@pytest.mark.parametrize("rule,positive,negative", CASES, ids=[c[0].__name__ for c in CASES])
def test_rule(rule, positive, negative):
    assert fires(rule, positive), f"{rule.__name__} should fire for {positive}"
    assert not fires(rule, negative), f"{rule.__name__} should not fire for {negative}"


def test_typosquatting_reports_target_brand():
    finding = rules.typosquatting(parse_url("https://paypa1.com"))
    assert finding is not None
    assert finding.evidence == "paypa1"
    assert "paypal" in finding.detail["en"]


def test_all_rules_have_messages():
    from app.core.messages import RULE_MESSAGES

    for rule in rules.ALL_RULES:
        assert rule.__name__ in RULE_MESSAGES
