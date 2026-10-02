export type Lang = 'ar' | 'en';
export type Severity = 'low' | 'medium' | 'high';
export type Verdict = 'safe' | 'suspicious' | 'dangerous';

export interface LocalizedText {
  ar: string;
  en: string;
}

export interface Finding {
  rule_id: string;
  severity: Severity;
  weight: number;
  title: LocalizedText;
  detail: LocalizedText;
  evidence: string;
}

export interface Analysis {
  url: string;
  normalized_url: string;
  scheme: string;
  host: string;
  host_display: string;
  subdomain: string;
  registered_domain: string;
  suffix: string;
  path: string;
  score: number;
  verdict: Verdict;
  verdict_label: LocalizedText;
  advice: LocalizedText;
  findings: Finding[];
}

export interface BatchItem {
  input: string;
  result: Analysis | null;
  error: LocalizedText | null;
}

export interface BatchResponse {
  items: BatchItem[];
  summary: {
    total: number;
    safe: number;
    suspicious: number;
    dangerous: number;
    invalid: number;
  };
}

export interface Scan {
  id: number;
  url: string;
  normalized_url: string;
  host: string;
  score: number;
  verdict: Verdict;
  findings: Finding[];
  source: 'single' | 'batch';
  created_at: string;
}

export interface HistoryPage {
  items: Scan[];
  total: number;
  limit: number;
  offset: number;
}

export interface Stats {
  total: number;
  safe: number;
  suspicious: number;
  dangerous: number;
  top_rules: { rule_id: string; title: LocalizedText; count: number }[];
}
