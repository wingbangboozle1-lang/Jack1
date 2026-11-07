(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var sidebar = document.getElementById('site-nav');
  if (!toggle || !sidebar) return;
  toggle.addEventListener('click', function () {
    var open = sidebar.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();
