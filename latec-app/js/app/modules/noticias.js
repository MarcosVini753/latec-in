import { news } from '../../data/data.js';
import { escapeHTML, setActiveLink, renderNewsCards } from '../components/ui.mjs';
import { formatDate } from '../core/utils.js';

export function renderNoticias() {
  setActiveLink('#noticias');
  const main = document.getElementById('app');
  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="section-heading">' +
          '<p class="section-kicker">Comunicação</p>' +
          '<h2 class="section-title">Notícias e Publicações</h2>' +
          '<p class="section-lead">Acompanhe editais, eventos e publicações da LATEC.IN.</p>' +
        '</div>' +
        '<div class="card-grid">' +
          renderNewsCards(news) +
        '</div>' +
      '</div>' +
    '</section>';
}

export function renderNewsDetail(id) {
  setActiveLink(null);
  const post = news.find(function(n) { return n.id === id; });
  const main = document.getElementById('app');

  if (!post) {
    renderNotFound();
    return;
  }

  const categoria = post.categoria || post.tag || 'Notícia';
  const data = formatDate(post.data);
  const imagem = post.imagem
    ? '<img src="' + escapeHTML(post.imagem) + '" alt="' + escapeHTML(post.titulo) + '">'
    : '';

  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="detail-actions">' +
          '<a href="#noticias" class="btn btn-secondary">Voltar para Notícias</a>' +
        '</div>' +
        '<article class="content-panel detail-panel prose">' +
          '<p class="section-kicker">' + escapeHTML(categoria) + ' - ' + escapeHTML(data) + '</p>' +
          '<h2 class="section-title">' + escapeHTML(post.titulo) + '</h2>' +
          imagem +
          '<p>' + escapeHTML(post.conteudo) + '</p>' +
        '</article>' +
      '</div>' +
    '</section>';
}
