export function filtrarPorCategoria(categoria, lista) {
  if (!categoria || categoria.toLowerCase() === 'todos') return lista;
  return lista.filter(function(item) {
    return (item.categoria || '').toLowerCase() === categoria.toLowerCase();
  });
}

export function filtrarPorBusca(termo, lista) {
  if (!termo) return lista;
  const t = termo.toLowerCase();
  return lista.filter(function(item) {
    const texto = (item.titulo || item.nome || '').toLowerCase();
    return texto.indexOf(t) !== -1;
  });
}
