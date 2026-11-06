/* Shared chrome: injects nav + footer so every page is consistent. */
(function () {
  var NAV = [
    { href: 'index.html', label: 'Dashboard' },
    { href: 'executive-summary.html', label: 'Executive Summary' },
    { href: 'property.html', label: 'Property & Lease' },
    { href: 'market.html', label: 'Central LA Market' },
    { href: 'economy.html', label: 'Economy & Jobs' },
    { href: 'tenant.html', label: 'Tenant: Jack in the Box' },
    { href: 'projections.html', label: 'Projection Model' },
    { href: 'risk.html', label: 'Risk Analysis' },
    { href: 'decision.html', label: 'Sell vs. Renew' },
    { href: 'sources.html', label: 'Sources' },
    { href: 'flagged.html', label: 'Flagged for Review' }
  ];
  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  function navHTML() {
    var links = NAV.map(function (n) {
      var active = n.href === here ? ' class="active"' : '';
      return '<a href="' + n.href + '"' + active + '>' + n.label + '</a>';
    }).join('');
    return '<header class="topbar"><div class="topbar-inner">' +
      '<a class="brand" href="index.html"><span class="logo">JB</span> Project&nbsp;Jack&#8209;in&#8209;the&#8209;Box</a>' +
      '<button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">☰</button>' +
      '<nav class="mainnav" id="mainNav">' + links + '</nav>' +
      '</div></header>';
  }

  function footerHTML() {
    return '<footer class="site"><div class="container"><div class="cols">' +
      '<div><strong>Project Jack&#8209;in&#8209;the&#8209;Box</strong><br>Central Los Angeles NNN lease &mdash; sell vs. renew analysis.<br>' +
      'Prepared 2026&#8209;11&#8209;06. Data retrieved Nov 2026; verify before relying.</div>' +
      '<div><strong>Privacy</strong><br>No personal information appears on this site. The owner is &ldquo;the Owner&rdquo;; the property address and tenant identity details are withheld/anonymized.</div>' +
      '<div><strong>Notice</strong><br>Not financial, legal, or tax advice. Figures carry source links; unverified figures are flagged on the <a href="flagged.html">Flagged for Review</a> page. See <a href="sources.html">Sources</a>.</div>' +
      '</div></div></footer>';
  }

  var headerHost = document.getElementById('site-header');
  if (headerHost) headerHost.innerHTML = navHTML();
  var footerHost = document.getElementById('site-footer');
  if (footerHost) footerHost.innerHTML = footerHTML();

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t && t.id === 'navToggle') {
      var nav = document.getElementById('mainNav');
      if (nav) nav.classList.toggle('open');
    }
  });
})();
