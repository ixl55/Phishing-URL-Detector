import type { Analysis } from '../lib/types';

export const dangerousResult: Analysis = {
  url: 'http://paypal.com@evil.tk/login',
  normalized_url: 'http://paypal.com@evil.tk/login',
  scheme: 'http',
  host: 'evil.tk',
  host_display: 'evil.tk',
  subdomain: '',
  registered_domain: 'evil.tk',
  suffix: 'tk',
  path: '/login',
  score: 100,
  verdict: 'dangerous',
  verdict_label: { ar: 'خطر', en: 'Dangerous' },
  advice: {
    ar: 'تحذير: هذا الرابط على الأرجح احتيالي. لا تفتحه ولا تُدخل أي بيانات فيه.',
    en: "Warning: this link is most likely a scam. Don't open it or enter any information.",
  },
  findings: [
    {
      rule_id: 'at_symbol',
      severity: 'high',
      weight: 45,
      title: { ar: 'رمز @ داخل الرابط', en: '@ symbol in the address' },
      detail: { ar: 'المتصفح يذهب فعلياً إلى evil.tk', en: 'Browsers actually open evil.tk' },
      evidence: 'evil.tk',
    },
  ],
};

export const safeResult: Analysis = {
  ...dangerousResult,
  url: 'https://www.google.com',
  normalized_url: 'https://www.google.com',
  scheme: 'https',
  host: 'www.google.com',
  host_display: 'www.google.com',
  subdomain: 'www',
  registered_domain: 'google.com',
  suffix: 'com',
  path: '',
  score: 0,
  verdict: 'safe',
  verdict_label: { ar: 'آمن', en: 'Safe' },
  advice: { ar: 'لم نجد مؤشرات خطر واضحة.', en: 'No clear warning signs found.' },
  findings: [],
};
