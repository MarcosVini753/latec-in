/*
  Este arquivo contém dados simulados para o protótipo da plataforma LATEC.IN.
  Em uma aplicação real, essas informações seriam buscadas de um banco de dados
  ou API. Aqui utilizamos objetos e arrays estáticos para facilitar a
  demonstração da navegação e dos filtros.
*/

// Membros da liga
const members = [
  {
    id: 1,
    nome: 'Marta Adelino',
    funcao: 'Coordenadora',
    bio: 'Professora doutora e coordenadora da LATEC.IN, com larga experiência em biotecnologia e gestão de projetos.',
    foto: 'https://via.placeholder.com/150?text=Marta'
  },
  {
    id: 2,
    nome: 'Gabriel Daniel',
    funcao: 'Estagiário',
    bio: 'Estudante de Sistemas de Informação na UFAC, responsável pela criação deste protótipo.',
    foto: 'https://via.placeholder.com/150?text=Gabriel'
  },
  {
    id: 3,
    nome: 'Ana Souza',
    funcao: 'Pesquisadora',
    bio: 'Discente pesquisadora focada em bioinformática e biodiversidade amazônica.',
    foto: 'https://via.placeholder.com/150?text=Ana'
  }
];

// Projetos desenvolvidos
const projects = [
  {
    id: 1,
    titulo: 'Fábrica de Ensino: Bootcamp de Python',
    categoria: 'Ensino',
    area: 'Fábrica de Ensino',
    status: 'Concluído',
    ano: 2025,
    resumo: 'Bootcamp intensivo de Python para novos membros da LATEC.IN.',
    problema: 'Falta de capacitação em programação entre os integrantes.',
    solucao: 'Proporcionar um treinamento prático e imersivo em Python.',
    resultados: ['Relatório de atividades', 'Apostila digital'],
    equipe: [1, 2, 3],
    link: ''
  },
  {
    id: 2,
    titulo: 'Pesquisa de Bioativos da Amazônia',
    categoria: 'Pesquisa',
    area: 'Projetos de Pesquisa',
    status: 'Em andamento',
    ano: 2026,
    resumo: 'Estudo dos compostos bioativos presentes em espécies amazônicas.',
    problema: 'Necessidade de explorar novos fármacos e compostos naturais.',
    solucao: 'Investigar propriedades bioativas de plantas da região amazônica.',
    resultados: ['Artigo científico', 'Protótipo de extrato'],
    equipe: [1, 3],
    link: ''
  },
  {
    id: 3,
    titulo: 'Extensão em Tecnologias Sustentáveis',
    categoria: 'Extensão',
    area: 'Extensão Tecnológica',
    status: 'Planejado',
    ano: 2026,
    resumo: 'Iniciativa para aplicar tecnologia verde em comunidades locais.',
    problema: 'Falta de acesso a tecnologias sustentáveis em regiões remotas.',
    solucao: 'Desenvolver protótipos de baixo custo e treinamentos comunitários.',
    resultados: ['Manual de boas práticas'],
    equipe: [2, 3],
    link: ''
  }
];

// Notícias / artigos
const news = [
  {
    id: 1,
    titulo: 'Edital de Ingresso 2026 aberto',
    data: '2026-06-01',
    resumo: 'Está aberto o edital para novos membros da LATEC.IN. Participe e faça parte da inovação na UFAC!',
    conteudo: 'O edital de ingresso para o ano de 2026 encontra-se disponível. Alunos de graduação e pós-graduação interessados em biotecnologia, biodiversidade e inovação podem se inscrever até o dia 15 de julho. Consulte o edital completo para mais informações.',
    imagem: 'https://via.placeholder.com/400x200?text=Edital'
  },
  {
    id: 2,
    titulo: 'LATEC.IN participa do congresso nacional de inovação',
    data: '2026-05-15',
    resumo: 'A LATEC.IN apresentou três projetos no congresso nacional, recebendo destaque na sessão de biotecnologia.',
    conteudo: 'No congresso nacional de inovação tecnológica, a LATEC.IN foi representada pelos projetos “Fábrica de Ensino”, “Pesquisa de Bioativos da Amazônia” e “Extensão em Tecnologias Sustentáveis”. As apresentações foram bem recebidas e destacaram o potencial dos alunos da UFAC.',
    imagem: 'https://via.placeholder.com/400x200?text=Congresso'
  }
];

// Cursos e capacitações
const courses = [
  {
    id: 1,
    titulo: 'Bootcamp de Python',
    descricao: 'Aprenda Python do zero ao avançado em um bootcamp intensivo.',
    data: '2026-07-10',
    status: 'Inscrições abertas',
    materiais: ['Apostila Python.pdf'],
    link: ''
  },
  {
    id: 2,
    titulo: 'Workshop de Inteligência Artificial',
    descricao: 'Fundamentos de IA e Machine Learning aplicados à biotecnologia.',
    data: '2026-08-15',
    status: 'Em breve',
    materiais: [],
    link: ''
  }
];

// Materiais de apoio
const materials = [
  {
    id: 1,
    titulo: 'Apostila de Python',
    descricao: 'Apostila utilizada no bootcamp de Python da LATEC.IN.',
    arquivo: 'assets/images/apostila-python.pdf'
  }
];

// Premiações e honrarias
const awards = [
  {
    id: 1,
    titulo: 'Prêmio Inovação UFAC 2025',
    descricao: 'Projeto Fábrica de Ensino premiado no evento de inovação da UFAC em 2025.',
    data: '2025-11-20'
  }
];

// Números de impacto para o painel dinâmico
const impactNumbers = {
  membros: 15,
  projetos: 20,
  artigos: 12,
  parcerias: 5
};

// Exportação global para facilitar o acesso nos arquivos de renderização
// (em ambiente real usaríamos módulos ou bundlers)
window.members = members;
window.projects = projects;
window.news = news;
window.courses = courses;
window.materials = materials;
window.awards = awards;
window.impactNumbers = impactNumbers;