/*
  render.js
  Contém as funções responsáveis por montar o HTML de cada rota do site.
  As funções utilizam os dados definidos em data.js para preencher os
  elementos da página dinamicamente.
*/

/* Auxiliar para definir o link ativo na navegação */
function setActiveLink(route) {
  const links = document.querySelectorAll('.main-nav a');
  links.forEach(link => {
    if (link.getAttribute('href') === route) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/* Renderiza a página inicial (Home) */
function renderHome() {
  setActiveLink('#home');
  const main = document.getElementById('app');
  // Seleciona alguns itens para destaque
  const latestNews = news.slice(0, 2);
  const featuredProjects = projects.slice(0, 2);
  main.innerHTML = `
    <section class="hero">
      <div class="container">
        <h1>Inovação, Biotecnologia e Biodiversidade</h1>
        <p>Somos a LATEC.IN, a liga acadêmica que conecta ciência e tecnologia em prol da Amazônia.</p>
        <a href="#portfolio" class="btn btn-primary">Conheça Nossos Projetos</a>
      </div>
    </section>
    <section>
      <h2 class="section-title">Últimas notícias</h2>
      <div class="container card-grid">
        ${latestNews.map(post => `
          <div class="card">
            <h3>${post.titulo}</h3>
            <p>${post.resumo}</p>
            <a href="#noticia?id=${post.id}" class="btn btn-secondary">Leia mais</a>
          </div>
        `).join('')}
      </div>
    </section>
    <section>
      <h2 class="section-title">Projetos em destaque</h2>
      <div class="container card-grid">
        ${featuredProjects.map(proj => `
          <div class="card">
            <h3>${proj.titulo}</h3>
            <p>${proj.resumo}</p>
            <div class="tags">
              <span class="tag">${proj.categoria}</span>
              <span class="tag">${proj.ano}</span>
            </div>
            <a href="#projeto?id=${proj.id}" class="btn btn-secondary">Detalhes</a>
          </div>
        `).join('')}
      </div>
    </section>
    <section>
      <h2 class="section-title">Nosso Impacto</h2>
      <div class="container impact-grid">
        <div class="impact-item">
          <div class="number">${impactNumbers.membros}</div>
          <div class="label">Membros</div>
        </div>
        <div class="impact-item">
          <div class="number">${impactNumbers.projetos}</div>
          <div class="label">Projetos</div>
        </div>
        <div class="impact-item">
          <div class="number">${impactNumbers.artigos}</div>
          <div class="label">Artigos</div>
        </div>
        <div class="impact-item">
          <div class="number">${impactNumbers.parcerias}</div>
          <div class="label">Parcerias</div>
        </div>
      </div>
    </section>
  `;
}

/* Renderiza a página Quem Somos */
function renderQuemSomos() {
  setActiveLink('#quem-somos');
  const main = document.getElementById('app');
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Quem Somos</h2>
        <p>A LATEC.IN (Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação) é um núcleo de pesquisa, ensino e extensão da Universidade Federal do Acre. Nossa missão é desenvolver soluções tecnológicas e científicas para a Amazônia, promovendo a formação de profissionais capacitados e conscientes do papel da ciência na sociedade.</p>
        <p>Visão: Tornar-se referência nacional em inovação biotecnológica e proteção da biodiversidade amazônica.</p>
        <p>Valores: Ética, Inovação, Sustentabilidade, Colaboração e Excelência.</p>
        <h3 style="margin-top:40px">Linhas de Atuação</h3>
        <ul>
          <li>Inteligência Artificial aplicada à Biotecnologia</li>
          <li>Cyber Defesa e Segurança de Dados Biológicos</li>
          <li>Governança de TI no setor acadêmico</li>
          <li>Desenvolvimento de Software para pesquisas científicas</li>
        </ul>
        <h3 style="margin-top:40px">Nossa Equipe</h3>
        <div class="card-grid">
          ${members.map(m => `
            <div class="card">
              <img src="${m.foto}" alt="Foto de ${m.nome}" style="width:100%; height:120px; object-fit:cover; border-radius:4px 4px 0 0;">
              <h3>${m.nome}</h3>
              <p><strong>${m.funcao}</strong></p>
              <p>${m.bio}</p>
            </div>
          `).join('')}
        </div>
      </div>
    </section>
  `;
}

/* Renderiza a página de Portfólio com filtros */
function renderPortfolio() {
  setActiveLink('#portfolio');
  const main = document.getElementById('app');
  // Inicialmente exibimos todos os projetos
  const projectList = projects;
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Portfólio</h2>
        <div id="portfolio-filters" style="text-align:center; margin-bottom:16px;">
          <button class="btn btn-secondary" data-filter="todos">Todos</button>
          <button class="btn btn-secondary" data-filter="Ensino">Ensino</button>
          <button class="btn btn-secondary" data-filter="Pesquisa">Pesquisa</button>
          <button class="btn btn-secondary" data-filter="Extensão">Extensão</button>
        </div>
        <div id="portfolio-list" class="card-grid">
          ${renderProjectCards(projectList)}
        </div>
      </div>
    </section>
  `;
  // Adiciona eventos aos filtros
  const filterButtons = document.querySelectorAll('#portfolio-filters button');
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-filter');
      let filtered;
      if (category === 'todos') {
        filtered = projects;
      } else {
        filtered = projects.filter(p => p.categoria === category);
      }
      document.getElementById('portfolio-list').innerHTML = renderProjectCards(filtered);
    });
  });
}

/* Gera o HTML de cartões de projetos */
function renderProjectCards(list) {
  return list.map(proj => `
    <div class="card">
      <h3>${proj.titulo}</h3>
      <p>${proj.resumo}</p>
      <div class="tags">
        <span class="tag">${proj.categoria}</span>
        <span class="tag">${proj.ano}</span>
      </div>
      <a href="#projeto?id=${proj.id}" class="btn btn-secondary">Detalhes</a>
    </div>
  `).join('');
}

/* Renderiza a página de detalhes de um projeto */
function renderProjectDetail(id) {
  setActiveLink(null); // rota interna não marca menu
  const proj = projects.find(p => p.id === id);
  const main = document.getElementById('app');
  if (!proj) {
    renderNotFound();
    return;
  }
  // Recupera nomes da equipe
  const equipeNomes = proj.equipe.map(eid => {
    const m = members.find(mem => mem.id === eid);
    return m ? m.nome : 'Membro';
  });
  main.innerHTML = `
    <section>
      <div class="container">
        <a href="#portfolio" class="btn btn-secondary">&larr; Voltar para Portfólio</a>
        <h2 class="section-title" style="margin-top:24px">${proj.titulo}</h2>
        <p><strong>Categoria:</strong> ${proj.categoria} | <strong>Área:</strong> ${proj.area} | <strong>Status:</strong> ${proj.status} | <strong>Ano:</strong> ${proj.ano}</p>
        <h3>Resumo do Problema</h3>
        <p>${proj.problema}</p>
        <h3>Solução Proposta</h3>
        <p>${proj.solucao}</p>
        <h3>Resultados / Produtos</h3>
        <ul>
          ${proj.resultados.map(r => `<li>${r}</li>`).join('')}
        </ul>
        <h3>Equipe</h3>
        <ul>
          ${equipeNomes.map(nome => `<li>${nome}</li>`).join('')}
        </ul>
        ${proj.link ? `<p><a href="${proj.link}" target="_blank" rel="noopener" class="btn btn-primary">Acessar Repositório / Aplicação</a></p>` : ''}
      </div>
    </section>
  `;
}

/* Renderiza a página de capacitações e cursos */
function renderCapacitacao() {
  setActiveLink('#capacitacao');
  const main = document.getElementById('app');
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Capacitação & Cursos</h2>
        <p>Participe de nossas trilhas de aprendizagem, workshops e bootcamps para ampliar seus conhecimentos.</p>
        <div class="card-grid">
          ${courses.map(curso => `
            <div class="card">
              <h3>${curso.titulo}</h3>
              <p>${curso.descricao}</p>
              <p><strong>Data:</strong> ${curso.data}</p>
              <p><strong>Status:</strong> ${curso.status}</p>
              ${curso.link ? `<a href="${curso.link}" class="btn btn-secondary">Inscrever-se</a>` : ''}
            </div>
          `).join('')}
        </div>
        <h3 style="margin-top:40px">Materiais de apoio</h3>
        <ul>
          ${materials.map(mat => `<li><a href="${mat.arquivo}" target="_blank" rel="noopener">${mat.titulo}</a> - ${mat.descricao}</li>`).join('')}
        </ul>
      </div>
    </section>
  `;
}

/* Renderiza a listagem de notícias */
function renderNoticias() {
  setActiveLink('#noticias');
  const main = document.getElementById('app');
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Notícias & Publicações</h2>
        <div class="card-grid">
          ${news.map(post => `
            <div class="card">
              <h3>${post.titulo}</h3>
              <p><em>${formatDate(post.data)}</em></p>
              <p>${post.resumo}</p>
              <a href="#noticia?id=${post.id}" class="btn btn-secondary">Leia mais</a>
            </div>
          `).join('')}
        </div>
      </div>
    </section>
  `;
}

/* Renderiza a página de detalhe de uma notícia */
function renderNewsDetail(id) {
  setActiveLink(null);
  const post = news.find(n => n.id === id);
  const main = document.getElementById('app');
  if (!post) {
    renderNotFound();
    return;
  }
  main.innerHTML = `
    <section>
      <div class="container">
        <a href="#noticias" class="btn btn-secondary">&larr; Voltar para Notícias</a>
        <h2 class="section-title" style="margin-top:24px">${post.titulo}</h2>
        <p><em>${formatDate(post.data)}</em></p>
        ${post.imagem ? `<img src="${post.imagem}" alt="${post.titulo}" style="width:100%; max-height:300px; object-fit:cover; border-radius:4px; margin-bottom:16px;">` : ''}
        <p>${post.conteudo}</p>
      </div>
    </section>
  `;
}

/* Renderiza a página de contato */
function renderContato() {
  setActiveLink('#contato');
  const main = document.getElementById('app');
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Contato & Parcerias</h2>
        <p>Entre em contato conosco para dúvidas, propostas de imprensa ou se desejar tornar-se um parceiro da LATEC.IN.</p>
        <form class="contact-form" id="contact-form">
          <label for="tipo">Motivo do contato</label>
          <select id="tipo" name="tipo" required>
            <option value="">Selecione...</option>
            <option value="duvidas">Dúvidas</option>
            <option value="imprensa">Imprensa</option>
            <option value="parceria">Quero ser Parceiro</option>
          </select>
          <label for="nome">Nome</label>
          <input type="text" id="nome" name="nome" required>
          <label for="email">E-mail</label>
          <input type="email" id="email" name="email" required>
          <label for="mensagem">Mensagem</label>
          <textarea id="mensagem" name="mensagem" rows="5" required></textarea>
          <button type="submit" class="btn btn-primary">Enviar</button>
        </form>
        <p id="contact-success" style="display:none; color: var(--color-deep-green); margin-top:16px;">Mensagem enviada com sucesso! Entraremos em contato em breve.</p>
      </div>
    </section>
  `;
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    // simples feedback; em aplicação real, enviaríamos para servidor
    form.reset();
    document.getElementById('contact-success').style.display = 'block';
  });
}

/* Área de administração (delegada para admin.js) */
function renderAdmin() {
  // A função é implementada em admin.js
  // Aqui apenas chamamos a função global para consistência do roteador.
  if (typeof showAdminArea === 'function') {
    showAdminArea();
  }
}

/* Página não encontrada */
function renderNotFound() {
  const main = document.getElementById('app');
  main.innerHTML = `
    <section>
      <div class="container">
        <h2 class="section-title">Página não encontrada</h2>
        <p>Desculpe, a página solicitada não existe ou não foi encontrada.</p>
        <a href="#home" class="btn btn-secondary">Voltar para Home</a>
      </div>
    </section>
  `;
}

/* Utilitário para formatar datas (YYYY-MM-DD → DD/MM/AAAA) */
function formatDate(dateStr) {
  const date = new Date(dateStr);
  if (isNaN(date)) return dateStr;
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
}