import { members } from '../../data/data.js';
import { escapeHTML, renderTags, setActiveLink } from '../components/ui.mjs';

export function renderQuemSomos() {
  setActiveLink('#quem-somos');
  const main = document.getElementById('app');
  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container">' +
        '<div class="section-heading">' +
          '<p class="section-kicker">Institucional</p>' +
          '<h2 class="section-title">Quem Somos</h2>' +
          '<p class="section-lead">Pesquisa, ensino e extensão com foco em tecnologia, biodiversidade e inovação amazônica.</p>' +
        '</div>' +
        '<div class="content-panel prose">' +
          '<p>A LATEC.IN (Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação) é um núcleo de pesquisa, ensino e extensão da Universidade Federal do Acre. Nossa missão é desenvolver soluções tecnológicas e científicas para a Amazônia, promovendo a formação de profissionais capacitados e conscientes do papel da ciência na sociedade.</p>' +
          '<p><strong>Visão:</strong> tornar-se referência nacional em inovação biotecnológica e proteção da biodiversidade amazônica.</p>' +
          '<p><strong>Valores:</strong> ética, inovação, sustentabilidade, colaboração e excelência.</p>' +
        '</div>' +
      '</div>' +
    '</section>' +
    '<section class="page-section compact">' +
      '<div class="container split-grid">' +
        '<div class="content-panel">' +
          '<h3>Linhas de Atuação</h3>' +
          '<ul>' +
            '<li>Inteligência Artificial aplicada à Biotecnologia</li>' +
            '<li>Bootcamp de Startups</li>' +
            '<li>Biodiversidade no setor acadêmico</li>' +
            '<li>Farmacologia e biotecnologia para pesquisas científicas</li>' +
          '</ul>' +
        '</div>' +
        '<div class="content-panel">' +
          '<h3>Como Atuamos</h3>' +
          '<p>Organizamos capacitações, projetos de pesquisa, ações de extensão e protótipos que aproximam estudantes, docentes e parceiros externos.</p>' +
        '</div>' +
      '</div>' +
    '</section>' +
    '<section class="page-section compact">' +
      '<div class="container">' +
        '<div class="section-heading">' +
          '<h2 class="section-title">Nossa Equipe</h2>' +
        '</div>' +
        '<div class="card-grid">' +
          members.map(function(m) {
            return (
              '<article class="card">' +
                '<img class="card-media" src="' + escapeHTML(m.foto) + '" alt="Foto de ' + escapeHTML(m.nome) + '">' +
                '<h3>' + escapeHTML(m.nome) + '</h3>' +
                renderTags([m.funcao]) +
                '<p>' + escapeHTML(m.bio) + '</p>' +
              '</article>'
            );
          }).join('') +
        '</div>' +
      '</div>' +
    '</section>';
}
