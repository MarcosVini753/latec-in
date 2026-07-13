import { courses, materials } from '../../data/data.js';
import { escapeHTML, setActiveLink } from '../components/ui.mjs';
import { formatDate } from '../core/utils.js';

export function renderCapacitacao() {
  setActiveLink('#capacitacao');
  const main = document.getElementById('app');
  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="section-heading">' +
          '<p class="section-kicker">Formação</p>' +
          '<h2 class="section-title">Capacitação e Cursos</h2>' +
          '<p class="section-lead">Trilhas de aprendizagem, workshops e bootcamps para ampliar conhecimentos técnicos e científicos.</p>' +
        '</div>' +
        '<div class="card-grid">' +
          courses.map(function(curso) {
            const inscHtml = curso.link
              ? '<a href="' + escapeHTML(curso.link) + '" class="btn btn-secondary">Inscrever-se</a>'
              : '<span class="tag">Inscrições em breve</span>';
            return (
              '<article class="card">' +
                '<h3>' + escapeHTML(curso.titulo) + '</h3>' +
                '<p>' + escapeHTML(curso.descricao) + '</p>' +
                renderTags(['Data: ' + formatDate(curso.data), curso.status]) +
                '<div class="card-actions">' + inscHtml + '</div>' +
              '</article>'
            );
          }).join('') +
        '</div>' +
      '</div>' +
    '</section>' +
    '<section class="page-section compact">' +
      '<div class="container content-panel">' +
        '<h3>Materiais de apoio</h3>' +
        '<ul>' +
          materials.map(function(mat) {
            return '<li><a href="' + escapeHTML(mat.arquivo) + '" target="_blank" rel="noopener">' + escapeHTML(mat.titulo) + '</a> - ' + escapeHTML(mat.descricao) + '</li>';
          }).join('') +
        '</ul>' +
      '</div>' +
    '</section>';
}
