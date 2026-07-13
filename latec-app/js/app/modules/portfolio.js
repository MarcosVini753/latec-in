import { projects as projectsData, members } from '../../data/data.js';
import { escapeHTML, renderProjectCards, setActiveLink } from '../components/ui.mjs';
import { filtrarPorCategoria, filtrarPorBusca } from '../core/filters.js';

export function renderPortfolio() {
  setActiveLink('#portfolio');
  const main = document.getElementById('app');
  const categories = ['todos'].concat(
    Array.from(new Set(projectsData.map(function(p) { return p.categoria; }).filter(Boolean)))
  );

  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="section-heading">' +
          '<p class="section-kicker">Projetos</p>' +
          '<h2 class="section-title">Portfólio</h2>' +
          '<p class="section-lead">Filtre iniciativas por categoria e busque por título.</p>' +
        '</div>' +
        '<div class="filter-panel" aria-label="Filtros do portfólio">' +
          '<div id="portfolio-filters" class="filter-chips">' +
            '<label class="sr-only" for="portfolio-search">Buscar projetos</label>' +
            '<input id="portfolio-search" type="search" placeholder="Buscar projetos..." autocomplete="off">' +
            '<div id="category-chips">' +
              categories.map(function(cat, index) {
                const active = index === 0 ? ' active' : '';
                const pressed = index === 0 ? 'true' : 'false';
                const label = cat === 'todos' ? 'Todos' : escapeHTML(cat);
                return '<button class="filter-chip' + active + '" type="button" data-filter="' + escapeHTML(cat) + '" aria-pressed="' + pressed + '">' + label + '</button>';
              }).join('') +
            '</div>' +
          '</div>' +
          '<div class="filter-meta">' +
            '<button id="clear-portfolio-filter" class="btn btn-ghost" type="button">Limpar filtros</button>' +
            '<p id="portfolio-count" class="result-count">' + projectsData.length + ' projeto' + (projectsData.length === 1 ? '' : 's') + '</p>' +
          '</div>' +
        '</div>' +
        '<div id="portfolio-list" class="card-grid">' +
          renderProjectCards(projectsData) +
        '</div>' +
      '</div>' +
    '</section>';

  bindPortfolio();
}

export function renderProjectDetail(id) {
  setActiveLink(null);
  const proj = projectsData.find(function(p) { return p.id === id; });
  const main = document.getElementById('app');

  if (!proj) {
    renderNotFound();
    return;
  }

  const equipeNomes = (proj.equipe || []).map(function(eid) {
    const m = members.find(function(it) { return it.id === eid; });
    return m ? m.nome : 'Membro';
  });

  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="detail-actions">' +
          '<a href="#portfolio" class="btn btn-secondary">Voltar para Portfólio</a>' +
        '</div>' +
        '<article class="content-panel detail-panel prose">' +
          '<p class="section-kicker">Projeto</p>' +
          '<h2 class="section-title">' + escapeHTML(proj.titulo) + '</h2>' +
          renderTags([proj.categoria, proj.area, proj.status, String(proj.ano)]) +
          '<h3>Resumo do Problema</h3>' +
          '<p>' + escapeHTML(proj.problema) + '</p>' +
          '<h3>Solução Proposta</h3>' +
          '<p>' + escapeHTML(proj.solucao) + '</p>' +
          '<h3>Resultados / Produtos</h3>' +
          ((proj.resultados || []).length
            ? '<ul>' + proj.resultados.map(function(r) { return '<li>' + escapeHTML(r) + '</li>'; }).join('') + '</ul>'
            : '<p>Resultados ainda não cadastrados.</p>') +
          '<h3>Equipe</h3>' +
          (equipeNomes.length
            ? '<ul>' + equipeNomes.map(function(nome) { return '<li>' + escapeHTML(nome) + '</li>'; }).join('') + '</ul>'
            : '<p>Equipe ainda não cadastrada.</p>') +
          (proj.link ? '<p><a href="' + escapeHTML(proj.link) + '" target="_blank" rel="noopener" class="btn btn-primary">Acessar repositório ou aplicação</a></p>' : '') +
        '</article>' +
      '</div>' +
    '</section>';
}

function bindPortfolio() {
  const list = document.getElementById('portfolio-list');
  const count = document.getElementById('portfolio-count');
  const chips = document.querySelectorAll('#category-chips button');
  const search = document.getElementById('portfolio-search');
  const clear = document.getElementById('clear-portfolio-filter');

  if (!list || !chips.length) return;

  function apply(category, term) {
    term = (term || '').trim().toLowerCase();
    let filtered = filtrarPorCategoria(category, projectsData);
    filtered = filtrarPorBusca(term, filtered);
    list.innerHTML = renderProjectCards(filtered);
    count.textContent = filtered.length + ' projeto' + (filtered.length === 1 ? '' : 's');
  }

  chips.forEach(function(btn) {
    btn.addEventListener('click', function() {
      chips.forEach(function(b) {
        b.classList.remove('active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');
      apply(btn.getAttribute('data-filter'), search ? search.value : '');
    });
  });

  if (search) {
    search.addEventListener('input', function() {
      var active = document.querySelector('#category-chips button.active');
      var cat = active ? active.getAttribute('data-filter') : 'todos';
      apply(cat, search.value);
    });
  }

  if (clear) {
    clear.addEventListener('click', function() {
      var first = document.querySelector('#category-chips button');
      if (first) {
        first.classList.add('active');
        first.setAttribute('aria-pressed', 'true');
      }
      if (search) search.value = '';
      apply('todos', '');
    });
  }
}

export function renderNotFound() {
  const main = document.getElementById('app');
  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container content-panel">' +
        '<h2 class="section-title">Página não encontrada</h2>' +
        '<p>A página solicitada não existe ou não foi encontrada.</p>' +
        '<a href="#home" class="btn btn-secondary">Voltar para Home</a>' +
      '</div>' +
    '</section>';
}
