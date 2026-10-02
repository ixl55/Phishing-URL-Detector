"""Bilingual (Arabic / English) texts for every rule and verdict."""

RULE_MESSAGES: dict[str, dict[str, dict[str, str]]] = {
    "ip_address": {
        "title": {"ar": "عنوان IP بدل اسم نطاق", "en": "IP address instead of a domain"},
        "detail": {
            "ar": "الرابط يستخدم عنوان IP ({evidence}) بدل اسم موقع، وهذا أسلوب شائع لإخفاء هوية مواقع التصيّد.",
            "en": "The link points to an IP address ({evidence}) instead of a named website, a common trick to hide a phishing site.",
        },
    },
    "at_symbol": {
        "title": {"ar": "رمز @ داخل الرابط", "en": "@ symbol in the address"},
        "detail": {
            "ar": "المتصفح يتجاهل كل ما قبل @ ويذهب فعلياً إلى {evidence}، فالجزء الظاهر مضلِّل.",
            "en": "Browsers ignore everything before @ and actually open {evidence}; the visible part is a decoy.",
        },
    },
    "dangerous_scheme": {
        "title": {"ar": "نوع رابط خطير", "en": "Dangerous link scheme"},
        "detail": {
            "ar": "الرابط يبدأ بـ {evidence} وقد يشغّل كوداً أو يعرض صفحة مزيّفة مباشرة داخل المتصفح.",
            "en": "The link starts with {evidence}, which can run code or render a fake page directly in the browser.",
        },
    },
    "punycode": {
        "title": {"ar": "حروف مُقلَّدة (Punycode)", "en": "Look-alike characters (Punycode)"},
        "detail": {
            "ar": "اسم النطاق مكتوب بحروف من لغات أخرى تشبه الحروف اللاتينية ويظهر فعلياً كـ {evidence}.",
            "en": "The domain uses characters from other alphabets that look like Latin letters; it really reads {evidence}.",
        },
    },
    "mixed_script": {
        "title": {"ar": "خلط حروف من لغات مختلفة", "en": "Mixed alphabets in domain"},
        "detail": {
            "ar": "اسم النطاق يخلط حروفاً من أبجديات مختلفة ({evidence})، وهي حيلة لتقليد مواقع معروفة.",
            "en": "The domain mixes letters from different alphabets ({evidence}), a trick used to imitate known sites.",
        },
    },
    "brand_impersonation": {
        "title": {"ar": "انتحال علامة تجارية", "en": "Brand impersonation"},
        "detail": {
            "ar": "الرابط يذكر «{evidence}» لكنه لا ينتمي إلى موقعها الرسمي، بل إلى {domain}.",
            "en": "The link mentions “{evidence}” but does not belong to its official website; it belongs to {domain}.",
        },
    },
    "typosquatting": {
        "title": {"ar": "نطاق يشبه موقعاً معروفاً", "en": "Look-alike domain (typosquatting)"},
        "detail": {
            "ar": "النطاق «{evidence}» يشبه «{brand}» مع تغيير بسيط في الحروف لخداع العين.",
            "en": "The domain “{evidence}” closely resembles “{brand}” with small letter changes meant to fool the eye.",
        },
    },
    "suspicious_tld": {
        "title": {"ar": "امتداد نطاق مشبوه", "en": "Suspicious domain extension"},
        "detail": {
            "ar": "الامتداد .{evidence} رخيص أو مجاني ويُستخدم كثيراً في مواقع الاحتيال.",
            "en": "The .{evidence} extension is cheap or free and frequently abused by scam sites.",
        },
    },
    "shortener": {
        "title": {"ar": "رابط مختصر", "en": "Shortened link"},
        "detail": {
            "ar": "خدمة الاختصار {evidence} تُخفي الوجهة الحقيقية للرابط. لا تفتحه إلا إذا كنت تثق بالمرسل.",
            "en": "The {evidence} shortener hides the real destination. Only open it if you trust the sender.",
        },
    },
    "many_subdomains": {
        "title": {"ar": "نطاقات فرعية كثيرة", "en": "Too many subdomains"},
        "detail": {
            "ar": "الرابط يحتوي {evidence} مستويات فرعية، وهذا يُستخدم لدفن الاسم الحقيقي للموقع في آخر الرابط.",
            "en": "The link has {evidence} subdomain levels, often used to bury the real site name at the end.",
        },
    },
    "non_standard_port": {
        "title": {"ar": "منفذ غير معتاد", "en": "Unusual port"},
        "detail": {
            "ar": "الرابط يستخدم المنفذ {evidence}، والمواقع الموثوقة نادراً ما تفعل ذلك.",
            "en": "The link uses port {evidence}; legitimate websites rarely do this.",
        },
    },
    "embedded_redirect": {
        "title": {"ar": "إعادة توجيه مخفية", "en": "Hidden redirect"},
        "detail": {
            "ar": "الرابط يحتوي رابطاً آخر بداخله ({evidence}) وقد يحوّلك إلى موقع مختلف.",
            "en": "The link contains another link inside it ({evidence}) and may forward you to a different site.",
        },
    },
    "https_in_domain": {
        "title": {"ar": "كلمة https داخل اسم النطاق", "en": "“https” inside the domain name"},
        "detail": {
            "ar": "اسم النطاق يحتوي «{evidence}» ليوحي بالأمان، والمواقع الحقيقية لا تفعل ذلك.",
            "en": "The domain name contains “{evidence}” to look secure; real websites don't do this.",
        },
    },
    "dangerous_file": {
        "title": {"ar": "تنزيل ملف خطير", "en": "Dangerous file download"},
        "detail": {
            "ar": "الرابط يؤدي إلى ملف {evidence} قد يكون برنامجاً ضاراً. لا تقم بتشغيله.",
            "en": "The link leads to a {evidence} file that may be malware. Do not run it.",
        },
    },
    "many_hyphens": {
        "title": {"ar": "شرطات كثيرة في النطاق", "en": "Many hyphens in domain"},
        "detail": {
            "ar": "اسم النطاق يحتوي {evidence} شرطات، وهو نمط شائع في نطاقات التصيّد مثل secure-login-update.",
            "en": "The domain contains {evidence} hyphens, a common pattern in phishing domains like secure-login-update.",
        },
    },
    "sensitive_keywords": {
        "title": {"ar": "كلمات حساسة", "en": "Sensitive keywords"},
        "detail": {
            "ar": "الرابط يحتوي كلمات تستدرج لإدخال بياناتك: {evidence}.",
            "en": "The link contains words used to lure you into entering your details: {evidence}.",
        },
    },
    "long_url": {
        "title": {"ar": "رابط طويل جداً", "en": "Very long link"},
        "detail": {
            "ar": "طول الرابط {evidence} حرفاً، والروابط الطويلة تُستخدم لإخفاء الجزء المشبوه.",
            "en": "The link is {evidence} characters long; long links are used to hide the suspicious part.",
        },
    },
    "no_https": {
        "title": {"ar": "اتصال غير مشفّر", "en": "Unencrypted connection"},
        "detail": {
            "ar": "الرابط لا يستخدم HTTPS، فأي بيانات تُدخلها قد تُرسل دون تشفير.",
            "en": "The link does not use HTTPS, so anything you enter may be sent unencrypted.",
        },
    },
    "obfuscation": {
        "title": {"ar": "ترميز مُموِّه", "en": "Obfuscated encoding"},
        "detail": {
            "ar": "الرابط يحتوي {evidence} رموز مُرمَّزة (%xx) تُستخدم لإخفاء محتواه الحقيقي.",
            "en": "The link contains {evidence} encoded characters (%xx) used to disguise its real content.",
        },
    },
}

VERDICT_LABELS = {
    "safe": {"ar": "آمن", "en": "Safe"},
    "suspicious": {"ar": "مشبوه", "en": "Suspicious"},
    "dangerous": {"ar": "خطر", "en": "Dangerous"},
}

VERDICT_ADVICE = {
    "safe": {
        "ar": "لم نجد مؤشرات خطر واضحة. ومع ذلك تأكد دائماً من المرسل قبل إدخال بياناتك.",
        "en": "No clear warning signs found. Still, always verify the sender before entering your details.",
    },
    "suspicious": {
        "ar": "الرابط يحمل مؤشرات مشبوهة. لا تُدخل كلمات المرور أو بيانات البطاقة قبل التأكد من مصدره.",
        "en": "This link shows suspicious signs. Don't enter passwords or card details until you verify its source.",
    },
    "dangerous": {
        "ar": "تحذير: هذا الرابط على الأرجح احتيالي. لا تفتحه ولا تُدخل أي بيانات فيه.",
        "en": "Warning: this link is most likely a scam. Don't open it or enter any information.",
    },
}

ERRORS = {
    "empty": {"ar": "الرجاء إدخال رابط.", "en": "Please enter a link."},
    "invalid": {"ar": "هذا لا يبدو رابطاً صالحاً.", "en": "This doesn't look like a valid link."},
    "no_urls": {"ar": "لم يتم العثور على روابط في النص.", "en": "No links were found in the text."},
}


def render(rule_id: str, **params: object) -> dict[str, dict[str, str]]:
    """Return ``{"title": {ar, en}, "detail": {ar, en}}`` with *params* substituted."""
    texts = RULE_MESSAGES[rule_id]
    return {
        "title": dict(texts["title"]),
        "detail": {lang: tpl.format(**params) for lang, tpl in texts["detail"].items()},
    }
