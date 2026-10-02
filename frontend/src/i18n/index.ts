import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import ar from './locales/ar.json';
import en from './locales/en.json';
import type { Lang } from '../lib/types';

function storedLanguage(): Lang {
  try {
    return localStorage.getItem('lang') === 'en' ? 'en' : 'ar';
  } catch {
    return 'ar';
  }
}

i18n.use(initReactI18next).init({
  resources: { ar: { translation: ar }, en: { translation: en } },
  lng: storedLanguage(),
  fallbackLng: 'ar',
  interpolation: { escapeValue: false },
});

export default i18n;
