// Jack in the Box NNN Brief — minimal JS
document.addEventListener('DOMContentLoaded', () => {
  // Highlight current nav by path
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href.endsWith(path)) a.classList.add('active');
    // index special
    if ((path === '' || path === 'index.html') && href === 'index.html') a.classList.add('active');
  });
  // Smooth print handling
  document.querySelectorAll('a[href^="http"]').forEach(a=>{
    a.setAttribute('target','_blank');
    a.setAttribute('rel','noopener');
  });
  console.log('Jack in the Box NNN Brief — verified build', new Date().toISOString());
});
