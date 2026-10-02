# 🛡️ كاشف روابط التصيّد — Phishing URL Detector

أداة لتحليل الروابط المشبوهة وتحذير المستخدم إذا كان الرابط خطراً، مع شرح واضح لأسباب التقييم بالعربية والإنجليزية.
التحليل يتم محلياً بالكامل عبر قواعد فحص (heuristics) دون إرسال الروابط لأي جهة خارجية ودون الحاجة لمفاتيح API.

*A tool that analyzes suspicious links and warns users when a link is dangerous, explaining every red flag in Arabic and English. Analysis runs fully offline using heuristic rules — no third-party services, no API keys.*

---

## ✨ المميزات | Features

| | العربية | English |
|---|---|---|
| 🔍 | فحص رابط واحد مع درجة خطر من 0 إلى 100 وحكم: آمن / مشبوه / خطر | Single-link scan with a 0–100 risk score and verdict: Safe / Suspicious / Dangerous |
| 📋 | فحص جماعي: الصق رسالة SMS أو بريداً كاملاً لاستخراج كل الروابط وفحصها (يدعم `hxxp` و `[.]`) | Batch scan: paste a whole SMS or e-mail to extract and scan every link (supports `hxxp` and `[.]`) |
| 🧩 | تفكيك الرابط وإبراز النطاق الحقيقي | URL breakdown highlighting the real domain |
| 📊 | سجل الفحوصات مع إحصائيات وأكثر المؤشرات تكراراً | Scan history with statistics and most frequent warning signs |
| 🌐 | واجهة عربية (RTL) وإنجليزية مع زر تبديل | Arabic (RTL) and English UI with a toggle |
| 🌙 | وضع فاتح وداكن | Light and dark mode |
| ⌨️ | أداة سطر أوامر (CLI) | Command-line tool |

## 🧠 قواعد الكشف | Detection rules

| القاعدة | Rule | الخطورة / Severity |
|---|---|---|
| عنوان IP بدل اسم النطاق (يشمل الصيغ العشرية والست عشرية) | IP address host (incl. decimal / hex forms) | High |
| رمز `@` داخل العنوان | `@` in the address | High |
| مخطط `javascript:` / `data:` | `javascript:` / `data:` scheme | High |
| خلط حروف من أبجديات مختلفة | Mixed alphabets (homograph) | High |
| انتحال علامة تجارية (PayPal، Google، Apple، الراجحي، أبشر، STC…) | Brand impersonation | High |
| نطاق مقلّد مثل `paypa1` و `g00gle` و `rnicrosoft` | Typosquatting | High |
| Punycode (`xn--`) | Punycode | Medium |
| امتداد مشبوه (`.tk` `.xyz` `.top` …) | Suspicious TLD | Medium |
| رابط مختصر (`bit.ly` …) | URL shortener | Medium |
| نطاقات فرعية كثيرة، منفذ غير معتاد، إعادة توجيه مخفية | Many subdomains, unusual port, hidden redirect | Medium |
| كلمة `https` داخل اسم النطاق، ملف تنفيذي (`.exe` `.apk`) | `https` inside domain, executable download | Medium |
| شرطات كثيرة، كلمات حساسة، رابط طويل، بدون HTTPS، ترميز مُموِّه | Many hyphens, sensitive keywords, long URL, no HTTPS, obfuscation | Low |

الدرجة = مجموع أوزان المؤشرات (بحد أقصى 100): أقل من 30 **آمن**، من 30 إلى 59 **مشبوه**، 60 فأكثر **خطر**.

*Score = sum of rule weights (capped at 100): below 30 **Safe**, 30–59 **Suspicious**, 60+ **Dangerous**.*

## 🏗️ التقنيات | Tech stack

**Backend:** Python 3.10+ · FastAPI · SQLAlchemy 2 (SQLite) · Pydantic v2 · pytest

**Frontend:** React 18 · TypeScript · Vite · Tailwind CSS · react-i18next · React Router · TanStack Query · lucide-react · Vitest

```
backend/
  app/
    core/      # analyzer, rules, domain helpers, URL extractor, bilingual messages
    api/       # FastAPI routers
    db/        # SQLite models & queries
    cli.py     # command-line interface
  tests/
frontend/
  src/
    pages/       # Scan, Batch, History
    components/  # scan/, batch/, history/, layout/, ui/
    i18n/        # ar.json, en.json
```

## 🚀 التشغيل | Getting started

المتطلبات: Python 3.10+ و Node.js 18+

```bash
make install        # تثبيت الحزم | install dependencies
```

### وضع التطوير | Development

```bash
make dev-backend    # http://localhost:8000  (API docs: /docs)
make dev-frontend   # http://localhost:5173
```

### تشغيل كامل من خادم واحد | Production-style single server

```bash
make run            # builds the frontend and serves everything on http://localhost:8000
```

### الاختبارات | Tests

```bash
make test
make lint
```

## ⌨️ سطر الأوامر | CLI

```bash
cd backend
python -m app.cli "http://paypa1-login.tk/verify"            # Arabic output
python -m app.cli "http://paypa1-login.tk/verify" --lang en  # English output
python -m app.cli "https://example.com" --json                # JSON output
```

رمز الخروج | Exit code: `0` آمن Safe · `1` مشبوه Suspicious · `2` خطر Dangerous · `3` رابط غير صالح Invalid

## 🔌 واجهة API

| Method | Endpoint | الوصف / Description |
|---|---|---|
| `POST` | `/api/analyze` | `{"url": "..."}` → تحليل رابط / analyze one link |
| `POST` | `/api/analyze/batch` | `{"text": "..."}` أو / or `{"urls": [...]}` → فحص جماعي / batch scan |
| `GET` | `/api/history?limit=&offset=&verdict=` | السجل / history |
| `DELETE` | `/api/history/{id}` · `/api/history` | حذف فحص أو مسح السجل / delete one or clear all |
| `GET` | `/api/stats` | الإحصائيات / statistics |
| `GET` | `/api/health` | فحص الحالة / health check |

مثال | Example:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "http://paypal.com@evil.tk/login"}'
```

كل رسالة في الاستجابة متوفرة باللغتين (`{"ar": "...", "en": "..."}`).
*Every message in the response is provided in both languages.*

## ⚙️ الإعدادات | Configuration

متغيرات البيئة (اختيارية) | Environment variables (optional):

| Variable | Default |
|---|---|
| `PUD_DATABASE_URL` | `sqlite:///backend/data/history.db` |
| `PUD_CORS_ORIGINS` | `["http://localhost:5173"]` |
| `PUD_MAX_BATCH` | `50` |

## ⚠️ تنبيه | Disclaimer

النتيجة تقديرية مبنية على قواعد تحليل ولا تضمن الأمان بنسبة 100%. عند الشك، لا تُدخل كلمات المرور أو بيانات البطاقة.

*Results are heuristic estimates and cannot guarantee 100% safety. When in doubt, never enter passwords or card details.*
