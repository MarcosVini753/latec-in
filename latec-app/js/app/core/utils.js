export function formatDate(dateStr) {
  if (!dateStr) return '';
  const parts = String(dateStr).split('-');
  if (parts.length === 3) {
    const [year, month, day] = parts;
    return `${day.padStart(2, '0')}/${month.padStart(2, '0')}/${year}`;
  }
  const date = new Date(dateStr);
  if (isNaN(date)) return dateStr;
  return date.toLocaleDateString('pt-BR');
}
