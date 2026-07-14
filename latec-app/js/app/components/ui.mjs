import { members, projects, news, courses, materials, awards, impactNumbers } from '../../data/data.mjs';
import { formatDate } from '../core/utils.js';

export function escapeHTML(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export function setActiveLink(route) {
  const links = document.querySelectorAll('.main-nav a');
  links.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === route);
  });
}

export function renderTags(tags) {
  return (
    '<div class="tags">' +
    tags.filter(Boolean).map(tag => `<span class="tag">${escapeHTML(tag)}</span>`).join('') +
    '</div>'
  );
}

export function renderNewsCards(list) {
  if (!list.length) {
    return '<div class="empty-state">Nenhuma notícia cadastrada ainda.</div>';
  }

  return list.map(post => {
    const imageHtml = post.imagem
      ? `<img class="card-media" src="${escapeHTML(post.imagem)}" alt="">`
      : '';
    const tagValue = post.categoria || post.tag || '';
    const dateFormatted = formatDate(post.data);

    return (
      '<article class="card">' +
        imageHtml +
        `<h3>${escapeHTML(post.titulo)}</h3>` +
        renderTags([tagValue, dateFormatted]) +
        `<p>${escapeHTML(post.resumo)}</p>` +
        `<div class="card-actions">` +
          `<a href="#noticia?id=${post.id}" class="btn btn-secondary">Leia mais</a>` +
        '</div>' +
      '</article>'
    );
  }).join('');
}

export function renderProjectCards(list) {
  if (!list.length) {
    return '<div class="empty-state">Nenhum projeto encontrado para esse filtro.</div>';
  }

  return list.map(proj => {
    const tagsHtml = renderTags([proj.categoria, proj.area, String(proj.ano)]);

    return (
      '<article class="card">' +
        `<h3>${escapeHTML(proj.titulo)}</h3>` +
        `<p>${escapeHTML(proj.resumo)}</p>` +
        tagsHtml +
        '<div class="card-actions">' +
          `<a href="#projeto?id=${proj.id}" class="btn btn-secondary">Detalhes</a>` +
        '</div>' +
      '</article>'
    );
  }).join('');
}
