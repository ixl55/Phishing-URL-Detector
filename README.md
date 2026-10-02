# 🛡️ Phishing URL Detector — كاشف روابط التصيّد

**[English](#english) · [العربية](#arabic)**

---

<a id="english"></a>

## English

A tool that analyzes suspicious links and warns users when a link is dangerous, explaining every red flag in Arabic and English. Analysis runs fully offline using heuristic rules — no third-party services, no API keys.

### ✨ Features

- 🔍 **Single-link scan** with a 0–100 risk score and a verdict: Safe / Suspicious / Dangerous
- 📋 **Batch scan**: paste a whole SMS or e-mail to extract and scan every link (supports defanged links such as `hxxp` and `[.]`)
- 🧩 **URL breakdown** highlighting the real domain behind the link
- 📊 **Scan history** with statistics and the most frequent warning signs
- 🌐 **Arabic (RTL) and English** interface with a language toggle
- 🌙 **Light and dark mode**
- ⌨️ **Command-line tool**

### 🧠 Detection rules

| Rule | Severity |
|---|---|
| IP address host (incl. decimal / hex / octal forms) | High |
| `@` in the address | High |
| `javascript:` / `data:` scheme | High |
| Mixed alphabets in the domain (homograph) | High |
| Brand impersonation (PayPal, Google, Apple, Al Rajhi, Absher, STC…) | High |
| Typosquatting such as `paypa1`, `g00gle`, `rnicrosoft` | High |
| Punycode (`xn--`) | Medium |
| Suspicious TLD (`.tk`, `.xyz`, `.top`…) | Medium |
| URL shortener (`bit.ly`…) | Medium |
| Many subdomains, unusual port, hidden redirect | Medium |
| `https` inside the domain name, executable download (`.exe`, `.apk`) | Medium |
| Many hyphens, sensitive keywords, long URL, no HTTPS, obfuscated encoding | Low |

**Score** = sum of rule weights (capped at 100): below 30 is **Safe**, 30–59 is **Suspicious**, 60 and above is **Dangerous**.

### 🏗️ Tech stack

- **Backend:** Python 3.10+ · FastAPI · SQLAlchemy 2 (SQLite) · Pydantic v2 · pytest
- **Frontend:** React 18 · TypeScript · Vite · Tailwind CSS · react-i18next · React Router · TanStack Query · lucide-react · Vitest

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

### 🚀 Getting started

Requirements: Python 3.10+ and Node.js 18+

```bash
make install        # install dependencies
```

**Development**

```bash
make dev-backend    # http://localhost:8000  (API docs at /docs)
make dev-frontend   # http://localhost:5173
```

**Single server (production style)**

```bash
make run            # builds the frontend and serves everything on http://localhost:8000
```

**Tests & lint**

```bash
make test
make lint
```

### ⌨️ CLI

```bash
cd backend
python -m app.cli "http://paypa1-login.tk/verify" --lang en  # English output
python -m app.cli "http://paypa1-login.tk/verify"            # Arabic output
python -m app.cli "https://example.com" --json                # JSON output
```

Exit codes: `0` Safe · `1` Suspicious · `2` Dangerous · `3` Invalid URL

### 🔌 API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | `{"url": "..."}` → analyze one link |
| `POST` | `/api/analyze/batch` | `{"text": "..."}` or `{"urls": [...]}` → batch scan |
| `GET` | `/api/history?limit=&offset=&verdict=` | scan history |
| `DELETE` | `/api/history/{id}` · `/api/history` | delete one scan / clear all |
| `GET` | `/api/stats` | statistics |
| `GET` | `/api/health` | health check |

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "http://paypal.com@evil.tk/login"}'
```

Every message in the response is provided in both languages: `{"ar": "...", "en": "..."}`.

### ⚙️ Configuration

Optional environment variables:

| Variable | Default |
|---|---|
| `PUD_DATABASE_URL` | `sqlite:///backend/data/history.db` |
| `PUD_CORS_ORIGINS` | `["http://localhost:5173"]` |
| `PUD_MAX_BATCH` | `50` |

### ⚠️ Disclaimer

Results are heuristic estimates and cannot guarantee 100% safety. When in doubt, never enter passwords or card details.

---

<a id="arabic"></a>

<div dir="rtl">

## العربية

أداة لتحليل الروابط المشبوهة وتحذير المستخدم إذا كان الرابط خطراً، مع شرح واضح لأسباب التقييم بالعربية والإنجليزية. التحليل يتم محلياً بالكامل عبر قواعد فحص (heuristics) دون إرسال الروابط لأي جهة خارجية ودون الحاجة لمفاتيح API.

### ✨ المميزات

- 🔍 **فحص رابط واحد** مع درجة خطر من 0 إلى 100 وحكم: آمن / مشبوه / خطر
- 📋 **فحص جماعي**: الصق رسالة SMS أو بريداً كاملاً لاستخراج كل الروابط وفحصها (يدعم الروابط المموّهة مثل `hxxp` و `[.]`)
- 🧩 **تفكيك الرابط** وإبراز النطاق الحقيقي الذي يؤدي إليه
- 📊 **سجل الفحوصات** مع إحصائيات وأكثر المؤشرات تكراراً
- 🌐 **واجهة عربية (RTL) وإنجليزية** مع زر تبديل
- 🌙 **وضع فاتح وداكن**
- ⌨️ **أداة سطر أوامر (CLI)**

### 🧠 قواعد الكشف

| القاعدة | الخطورة |
|---|---|
| عنوان IP بدل اسم النطاق (يشمل الصيغ العشرية والست عشرية والثمانية) | عالية |
| رمز `@` داخل العنوان | عالية |
| مخطط `javascript:` / `data:` | عالية |
| خلط حروف من أبجديات مختلفة في النطاق | عالية |
| انتحال علامة تجارية (PayPal، Google، Apple، الراجحي، أبشر، STC…) | عالية |
| نطاق مقلّد مثل `paypa1` و `g00gle` و `rnicrosoft` | عالية |
| Punycode (`xn--`) | متوسطة |
| امتداد نطاق مشبوه (`.tk` و `.xyz` و `.top`…) | متوسطة |
| رابط مختصر (`bit.ly`…) | متوسطة |
| نطاقات فرعية كثيرة، منفذ غير معتاد، إعادة توجيه مخفية | متوسطة |
| كلمة `https` داخل اسم النطاق، تنزيل ملف تنفيذي (`.exe` و `.apk`) | متوسطة |
| شرطات كثيرة، كلمات حساسة، رابط طويل، بدون HTTPS، ترميز مُموِّه | منخفضة |

**الدرجة** = مجموع أوزان المؤشرات (بحد أقصى 100): أقل من 30 **آمن**، من 30 إلى 59 **مشبوه**، 60 فأكثر **خطر**.

### 🏗️ التقنيات

- **الخادم (Backend):** Python 3.10+ · FastAPI · SQLAlchemy 2 (SQLite) · Pydantic v2 · pytest
- **الواجهة (Frontend):** React 18 · TypeScript · Vite · Tailwind CSS · react-i18next · React Router · TanStack Query · lucide-react · Vitest

### 🚀 التشغيل

المتطلبات: Python 3.10+ و Node.js 18+

```bash
make install        # تثبيت الحزم
```

**وضع التطوير**

```bash
make dev-backend    # http://localhost:8000  (توثيق الـ API على /docs)
make dev-frontend   # http://localhost:5173
```

**التشغيل الكامل من خادم واحد**

```bash
make run            # يبني الواجهة ويشغّل كل شيء على http://localhost:8000
```

**الاختبارات وفحص الكود**

```bash
make test
make lint
```

### ⌨️ سطر الأوامر

```bash
cd backend
python -m app.cli "http://paypa1-login.tk/verify"            # مخرجات بالعربية
python -m app.cli "http://paypa1-login.tk/verify" --lang en  # مخرجات بالإنجليزية
python -m app.cli "https://example.com" --json                # مخرجات JSON
```

رمز الخروج: `0` آمن · `1` مشبوه · `2` خطر · `3` رابط غير صالح

### 🔌 واجهة API

| Method | Endpoint | الوصف |
|---|---|---|
| `POST` | `/api/analyze` | `{"url": "..."}` → تحليل رابط واحد |
| `POST` | `/api/analyze/batch` | `{"text": "..."}` أو `{"urls": [...]}` → فحص جماعي |
| `GET` | `/api/history?limit=&offset=&verdict=` | سجل الفحوصات |
| `DELETE` | `/api/history/{id}` · `/api/history` | حذف فحص أو مسح السجل |
| `GET` | `/api/stats` | الإحصائيات |
| `GET` | `/api/health` | فحص حالة الخادم |

كل رسالة في الاستجابة متوفرة باللغتين: `{"ar": "...", "en": "..."}`.

### ⚙️ الإعدادات

متغيرات بيئة اختيارية:

| المتغير | القيمة الافتراضية |
|---|---|
| `PUD_DATABASE_URL` | `sqlite:///backend/data/history.db` |
| `PUD_CORS_ORIGINS` | `["http://localhost:5173"]` |
| `PUD_MAX_BATCH` | `50` |

### ⚠️ تنبيه

النتيجة تقديرية مبنية على قواعد تحليل ولا تضمن الأمان بنسبة 100%. عند الشك، لا تُدخل كلمات المرور أو بيانات البطاقة.

</div>
