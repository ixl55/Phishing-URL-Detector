import { useState, type FormEvent } from 'react';
import { FileText, ScanSearch } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../ui/Button';
import { Spinner } from '../ui/Spinner';

const SAMPLE = {
  ar: `عميلنا العزيز، تم تعليق حسابك في مصرف الراجحي بسبب نشاط غير معتاد.
لإعادة التفعيل خلال 24 ساعة: https://alrajhi-online.top/update/account
أو عبر: hxxp://paypa1-secure[.]com/login
تتبع شحنتك من أرامكس: bit.ly/3Ar4mX
الموقع الرسمي للمصرف: https://www.alrajhibank.com.sa`,
  en: `Dear customer, your account has been suspended due to unusual activity.
Reactivate within 24 hours: https://secure-paypal.com.verify-account.xyz/login
or via: hxxp://g00gle-verify[.]tk/signin
Track your parcel: bit.ly/3Ar4mX
Official website: https://www.paypal.com`,
};

interface Props {
  loading: boolean;
  onSubmit: (text: string) => void;
}

export function BatchInput({ loading, onSubmit }: Props) {
  const { t, i18n } = useTranslation();
  const [text, setText] = useState('');

  const submit = (event: FormEvent) => {
    event.preventDefault();
    if (text.trim()) onSubmit(text);
  };

  const useSample = () => {
    const sample = SAMPLE[i18n.language === 'en' ? 'en' : 'ar'];
    setText(sample);
    onSubmit(sample);
  };

  return (
    <form onSubmit={submit} className="space-y-3">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={7}
        placeholder={t('batch.placeholder')}
        className="w-full resize-y rounded-xl border border-slate-300 bg-white p-4 text-sm leading-relaxed text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-brand-500 focus:ring-4 focus:ring-brand-500/15 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
      />
      <div className="flex flex-wrap items-center gap-2">
        <Button type="submit" disabled={loading || !text.trim()}>
          {loading ? <Spinner /> : <ScanSearch className="h-4 w-4" aria-hidden />}
          {t('batch.button')}
        </Button>
        <Button type="button" variant="secondary" onClick={useSample} disabled={loading}>
          <FileText className="h-4 w-4" aria-hidden />
          {t('batch.sample')}
        </Button>
        <span className="ms-auto text-xs text-slate-500 dark:text-slate-400">{t('batch.max')}</span>
      </div>
    </form>
  );
}
