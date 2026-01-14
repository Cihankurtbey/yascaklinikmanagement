import { format, parseISO } from 'date-fns';
import { tr } from 'date-fns/locale';

export const formatDate = (date, formatStr = 'dd.MM.yyyy') => {
  if (!date) return '';
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    return format(dateObj, formatStr, { locale: tr });
  } catch (error) {
    return date;
  }
};

export const formatDateTime = (date, formatStr = 'dd.MM.yyyy HH:mm') => {
  if (!date) return '';
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    return format(dateObj, formatStr, { locale: tr });
  } catch (error) {
    return date;
  }
};

export const formatTime = (time) => {
  if (!time) return '';
  if (typeof time === 'string') {
    return time.substring(0, 5); // HH:mm formatına çevir
  }
  return time;
};

export const getRoleLabel = (role) => {
  const labels = {
    admin: 'Yönetici',
    doctor: 'Diş Hekimi',
    assistant: 'Asistan',
  };
  return labels[role] || role;
};

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('tr-TR', {
    style: 'currency',
    currency: 'TRY',
  }).format(amount);
};
