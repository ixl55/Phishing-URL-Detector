"""Reference data used by the detection rules."""

# Brand keyword -> official registered domains.
BRANDS: dict[str, tuple[str, ...]] = {
    "paypal": ("paypal.com", "paypal.me"),
    "google": ("google.com", "google.com.sa", "google.ae", "youtube.com", "gmail.com", "goo.gl"),
    "gmail": ("gmail.com", "google.com"),
    "apple": ("apple.com", "icloud.com"),
    "icloud": ("icloud.com", "apple.com"),
    "microsoft": ("microsoft.com", "live.com", "outlook.com", "office.com", "microsoftonline.com"),
    "outlook": ("outlook.com", "live.com", "microsoft.com", "office.com"),
    "office365": ("office.com", "microsoft.com", "office365.com"),
    "amazon": ("amazon.com", "amazon.sa", "amazon.ae", "amazon.co.uk", "amazon.de", "aws.amazon.com"),
    "facebook": ("facebook.com", "fb.com", "fb.me", "meta.com"),
    "instagram": ("instagram.com",),
    "whatsapp": ("whatsapp.com", "whatsapp.net", "wa.me"),
    "netflix": ("netflix.com",),
    "twitter": ("twitter.com", "x.com", "t.co"),
    "linkedin": ("linkedin.com",),
    "snapchat": ("snapchat.com",),
    "tiktok": ("tiktok.com",),
    "telegram": ("telegram.org", "t.me"),
    "binance": ("binance.com",),
    "coinbase": ("coinbase.com",),
    "dhl": ("dhl.com",),
    "fedex": ("fedex.com",),
    "aramex": ("aramex.com",),
    "alrajhi": ("alrajhibank.com.sa", "alrajhibank.com"),
    "alrajhibank": ("alrajhibank.com.sa", "alrajhibank.com"),
    "alahli": ("alahli.com", "snb.com"),
    "snb": ("snb.com", "alahli.com"),
    "riyadbank": ("riyadbank.com",),
    "stc": ("stc.com.sa", "stcpay.com.sa"),
    "stcpay": ("stcpay.com.sa",),
    "absher": ("absher.sa", "moi.gov.sa"),
    "spl": ("splonline.com.sa",),
    "tawakkalna": ("tawakkalna.sdaia.gov.sa", "sdaia.gov.sa"),
    "nafath": ("nafath.sa", "iam.gov.sa"),
}

# Short brand tokens that are too common to match as substrings; only matched as whole labels/tokens.
SHORT_BRANDS = {"snb", "spl", "dhl", "stc"}

# Brands used for typosquatting checks (edit distance against the registered domain label).
TYPO_TARGETS = (
    "paypal", "google", "apple", "microsoft", "amazon", "facebook", "instagram",
    "whatsapp", "netflix", "twitter", "linkedin", "binance", "coinbase", "outlook",
    "icloud", "alrajhibank", "riyadbank", "aramex", "absher", "snapchat", "telegram",
)

SUSPICIOUS_TLDS = {
    "tk", "ml", "ga", "cf", "gq", "xyz", "top", "zip", "mov", "click", "country",
    "kim", "work", "party", "gdn", "loan", "men", "review", "stream", "download",
    "racing", "win", "bid", "trade", "date", "faith", "science", "accountant",
    "cricket", "rest", "fit", "buzz", "monster", "cyou", "icu", "cam", "quest",
    "support", "live", "online", "site", "website", "space", "shop", "info",
}

SHORTENERS = {
    "bit.ly", "bitly.com", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "buff.ly",
    "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy", "tiny.cc", "t.ly", "s.id", "v.gd",
    "bl.ink", "short.io", "lnkd.in", "trib.al", "qrco.de", "shorte.st", "adf.ly",
}

SENSITIVE_KEYWORDS = (
    "login", "log-in", "signin", "sign-in", "verify", "verification", "secure", "account",
    "update", "confirm", "banking", "wallet", "password", "credential", "unlock", "suspend",
    "billing", "payment", "invoice", "recover", "authenticate", "webscr", "otp",
)

DANGEROUS_EXTENSIONS = (
    ".exe", ".apk", ".scr", ".bat", ".cmd", ".msi", ".js", ".vbs", ".jar", ".ps1", ".hta", ".dmg",
)

# Public suffixes made of two labels (registered domain takes three labels).
MULTI_PART_SUFFIXES = {
    "com.sa", "net.sa", "org.sa", "gov.sa", "edu.sa", "med.sa", "sch.sa",
    "com.eg", "gov.eg", "edu.eg", "org.eg",
    "co.ae", "gov.ae", "ac.ae",
    "com.kw", "gov.kw", "com.qa", "gov.qa", "com.bh", "gov.bh", "com.om", "gov.om",
    "com.jo", "gov.jo", "com.lb", "com.iq", "com.ly", "com.tn", "co.ma",
    "co.uk", "org.uk", "ac.uk", "gov.uk",
    "com.au", "net.au", "org.au", "co.nz", "co.jp", "co.in", "co.za",
    "com.br", "com.tr", "com.cn", "com.mx", "com.sg", "com.my", "com.pk",
}

DEFAULT_PORTS = {"http": 80, "https": 443}
