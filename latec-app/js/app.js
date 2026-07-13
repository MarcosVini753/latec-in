/*
  latec-app
  Ponto de entrada da aplicação.
*/
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('mobile-menu-toggle');
  const nav = document.getElementById('main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });

    document.querySelectorAll('.main-nav a').forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
});
