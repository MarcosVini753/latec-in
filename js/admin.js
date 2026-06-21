/*
  admin.js
  Simula uma área administrativa com login básico e operações de criação de
  conteúdo. Os dados são salvos no localStorage para persistência durante
  a sessão do navegador.
*/

// Estado de autenticação
let adminLoggedIn = false;

// Carrega dados persistidos do localStorage, se existirem
function loadStoredData() {
  const storedProjects = localStorage.getItem('latec-projects');
  const storedNews = localStorage.getItem('latec-news');
  if (storedProjects) {
    try {
      const projArr = JSON.parse(storedProjects);
      if (Array.isArray(projArr) && projArr.length) {
        // Substitui os projetos existentes (mantendo referência global)
        projects.length = 0;
        projArr.forEach(p => projects.push(p));
      }
    } catch (e) {
      console.error('Erro ao carregar projetos do localStorage', e);
    }
  }
  if (storedNews) {
    try {
      const newsArr = JSON.parse(storedNews);
      if (Array.isArray(newsArr) && newsArr.length) {
        news.length = 0;
        newsArr.forEach(n => news.push(n));
      }
    } catch (e) {
      console.error('Erro ao carregar notícias do localStorage', e);
    }
  }
}

function persistData() {
  localStorage.setItem('latec-projects', JSON.stringify(projects));
  localStorage.setItem('latec-news', JSON.stringify(news));
}

// Renderiza a área administrativa
function showAdminArea() {
  setActiveLink('#admin');
  const main = document.getElementById('app');
  // Verifica se já está logado na sessão
  if (localStorage.getItem('latec-admin') === 'true') {
    adminLoggedIn = true;
  }
  if (!adminLoggedIn) {
    main.innerHTML = `
      <section>
        <div class="container admin-area">
          <h2 class="section-title">Área Administrativa</h2>
          <p>Digite suas credenciais para acessar as funções de gerenciamento.</p>
          <form id="login-form">
            <label for="login-email">E-mail</label>
            <input type="email" id="login-email" required>
            <label for="login-senha">Senha</label>
            <input type="password" id="login-senha" required>
            <button type="submit" class="btn btn-primary" style="margin-top:8px; width:100%">Entrar</button>
          </form>
          <p id="login-error" class="error" style="display:none">Credenciais inválidas. Tente novamente.</p>
        </div>
      </section>
    `;
    const form = document.getElementById('login-form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const senha = document.getElementById('login-senha').value;
      // Credenciais fixas para o protótipo
      if (email === 'admin@latec.in' && senha === 'senha') {
        adminLoggedIn = true;
        localStorage.setItem('latec-admin', 'true');
        loadStoredData();
        renderAdmin();
      } else {
        document.getElementById('login-error').style.display = 'block';
      }
    });
  } else {
    // Área administrativa principal
    main.innerHTML = `
      <section>
        <div class="container admin-area">
          <h2 class="section-title">Bem-vindo, Administrador</h2>
          <button id="logout-btn" class="btn btn-secondary" style="margin-bottom:24px">Sair</button>
          <h3>Adicionar nova notícia</h3>
          <form id="add-news-form" style="margin-bottom:32px">
            <label>Título</label>
            <input type="text" id="news-titulo" required>
            <label>Data (YYYY-MM-DD)</label>
            <input type="date" id="news-data" required>
            <label>Resumo</label>
            <textarea id="news-resumo" rows="3" required></textarea>
            <label>Conteúdo</label>
            <textarea id="news-conteudo" rows="5" required></textarea>
            <button type="submit" class="btn btn-primary" style="margin-top:8px">Adicionar Notícia</button>
          </form>
          <h3>Adicionar novo projeto</h3>
          <form id="add-project-form">
            <label>Título</label>
            <input type="text" id="project-titulo" required>
            <label>Categoria (Ensino/Pesquisa/Extensão)</label>
            <input type="text" id="project-categoria" required>
            <label>Área</label>
            <input type="text" id="project-area" required>
            <label>Status</label>
            <input type="text" id="project-status" required>
            <label>Ano</label>
            <input type="number" id="project-ano" required>
            <label>Resumo</label>
            <textarea id="project-resumo" rows="3" required></textarea>
            <label>Problema</label>
            <textarea id="project-problema" rows="3" required></textarea>
            <label>Solução</label>
            <textarea id="project-solucao" rows="3" required></textarea>
            <button type="submit" class="btn btn-primary" style="margin-top:8px">Adicionar Projeto</button>
          </form>
        </div>
      </section>
    `;
    // Evento de logout
    document.getElementById('logout-btn').addEventListener('click', () => {
      adminLoggedIn = false;
      localStorage.removeItem('latec-admin');
      renderAdmin();
    });
    // Formulário de notícias
    document.getElementById('add-news-form').addEventListener('submit', function (e) {
      e.preventDefault();
      const titulo = document.getElementById('news-titulo').value;
      const data = document.getElementById('news-data').value;
      const resumo = document.getElementById('news-resumo').value;
      const conteudo = document.getElementById('news-conteudo').value;
      const newId = news.length ? Math.max(...news.map(n => n.id)) + 1 : 1;
      news.unshift({ id: newId, titulo, data, resumo, conteudo, imagem: '' });
      persistData();
      alert('Notícia adicionada com sucesso!');
      renderAdmin();
    });
    // Formulário de projetos
    document.getElementById('add-project-form').addEventListener('submit', function (e) {
      e.preventDefault();
      const titulo = document.getElementById('project-titulo').value;
      const categoria = document.getElementById('project-categoria').value;
      const area = document.getElementById('project-area').value;
      const status = document.getElementById('project-status').value;
      const ano = parseInt(document.getElementById('project-ano').value, 10);
      const resumo = document.getElementById('project-resumo').value;
      const problema = document.getElementById('project-problema').value;
      const solucao = document.getElementById('project-solucao').value;
      const newId = projects.length ? Math.max(...projects.map(p => p.id)) + 1 : 1;
      projects.unshift({ id: newId, titulo, categoria, area, status, ano, resumo, problema, solucao, resultados: [], equipe: [], link: '' });
      persistData();
      alert('Projeto adicionado com sucesso!');
      renderAdmin();
    });
  }
}