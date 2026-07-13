import { escapeHTML, setActiveLink } from '../components/ui.mjs';

export function renderContato() {
  setActiveLink('#contato');
  const main = document.getElementById('app');
  main.innerHTML =
    '<section class="page-section">' +
      '<div class="container form-shell">' +
        '<div class="section-heading">' +
          '<p class="section-kicker">Contato</p>' +
          '<h2 class="section-title">Contato e Parcerias</h2>' +
          '<p class="section-lead">Envie dúvidas, solicitações de imprensa, propostas de parceria ou mensagens sobre processo seletivo.</p>' +
        '</div>' +
        '<form class="form-card" id="contact-form">' +
          '<div class="form-grid">' +
            '<div class="form-field full">' +
              '<label for="tipo">Motivo do contato <span class="required">*</span></label>' +
              '<select id="tipo" name="tipo" required>' +
                '<option value="">Selecione uma categoria</option>' +
                '<option value="duvidas">Dúvidas</option>' +
                '<option value="imprensa">Imprensa</option>' +
                '<option value="parceria">Quero ser parceiro</option>' +
                '<option value="processo-seletivo">Processo seletivo</option>' +
                '<option value="outro">Outro</option>' +
              '</select>' +
              '<p class="help-text">Isso ajuda a direcionar sua mensagem para o fluxo correto.</p>' +
            '</div>' +
            '<div class="form-field">' +
              '<label for="nome">Nome <span class="required">*</span></label>' +
              '<input type="text" id="nome" name="nome" autocomplete="name" required>' +
            '</div>' +
            '<div class="form-field">' +
              '<label for="email">E-mail <span class="required">*</span></label>' +
              '<input type="email" id="email" name="email" autocomplete="email" required>' +
            '</div>' +
            '<div class="form-field full">' +
              '<label for="mensagem">Mensagem <span class="required">*</span></label>' +
              '<textarea id="mensagem" name="mensagem" rows="6" required></textarea>' +
              '<p class="help-text">Inclua contexto, prazos e links úteis, se existirem.</p>' +
            '</div>' +
          '</div>' +
          '<button type="submit" class="btn btn-primary">Enviar mensagem</button>' +
          '<p id="contact-success" class="form-message success" role="status">Mensagem enviada com sucesso. Entraremos em contato em breve.</p>' +
        '</form>' +
      '</div>' +
    '</section>';

  const form = document.getElementById('contact-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    form.reset();
    const success = document.getElementById('contact-success');
    if (success) success.classList.add('is-visible');
  });
}
