import { useCallback, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import type { Lang } from '../lib/types';

/** Current language plus a toggle; keeps <html lang/dir> and localStorage in sync. */
export function useDirection() {
  const { i18n } = useTranslation();
  const lang: Lang = i18n.language === 'en' ? 'en' : 'ar';

  useEffect(() => {
    const root = document.documentElement;
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    try {
      localStorage.setItem('lang', lang);
    } catch {
      /* storage unavailable */
    }
  }, [lang]);

  const toggle = useCallback(() => {
    i18n.changeLanguage(lang === 'ar' ? 'en' : 'ar');
  }, [i18n, lang]);

  return { lang, dir: lang === 'ar' ? 'rtl' : 'ltr', toggle } as const;
}
