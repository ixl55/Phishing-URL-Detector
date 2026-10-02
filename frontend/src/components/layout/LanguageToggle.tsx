import { Languages } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useDirection } from '../../hooks/useDirection';
import { Button } from '../ui/Button';

export function LanguageToggle() {
  const { t } = useTranslation();
  const { toggle } = useDirection();
  return (
    <Button variant="ghost" size="sm" onClick={toggle} aria-label={t('toggle.languageLabel')}>
      <Languages className="h-4 w-4" aria-hidden />
      <span>{t('toggle.language')}</span>
    </Button>
  );
}
