(function(){
  var I = {
    building:'<path d="M3 21h18"/><path d="M6 21V4h9v17"/><path d="M15 21V9h3v12"/><path d="M9 7h3M9 11h3M9 15h3"/>',
    receipt:'<path d="M7 2h7l4 4v16H7z"/><path d="M14 2v4h4"/><path d="M10 8h2M10 12h5M10 16h5"/>',
    globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 2.5 15.4 0 18M12 3c-2.5 2.6-2.5 15.4 0 18"/>',
    shieldcheck:'<path d="M12 3l7 3v6c0 4.8-3.3 7.8-7 9-3.7-1.2-7-4.2-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    rand:'<circle cx="12" cy="12" r="9"/><path d="M9 17V7h3.2a2.4 2.4 0 0 1 0 4.8H9M12.6 11.8L15 17"/>',
    headset:'<path d="M5 13v-1a7 7 0 0 1 14 0v1"/><path d="M5 13h1.5A1.5 1.5 0 0 1 8 14.5V18a1.5 1.5 0 0 1-1.5 1.5H5zM19 13h-1.5A1.5 1.5 0 0 0 16 14.5V18a1.5 1.5 0 0 0 1.5 1.5H19z"/><path d="M17.5 19.5A5 5 0 0 1 13 22"/>',
    phone:'<path d="M5.5 3h3l1.5 4.5-2 1.3a11 11 0 0 0 5.2 5.2l1.3-2 4.5 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 3.5 5.2 2 2 0 0 1 5.5 3z"/>',
    mail:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 7l8 6 8-6"/>',
    pin:'<path d="M12 22s7-6.4 7-12a7 7 0 0 0-14 0c0 5.6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    scale:'<path d="M12 3v18M8 21h8"/><path d="M5.5 6.5L18 4"/><path d="M6 7l-3 6a3 3 0 0 0 6 0zM18 4.5l-3 6a3 3 0 0 0 6 0z"/>',
    briefcase:'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5.5A2.5 2.5 0 0 1 10.5 3h3A2.5 2.5 0 0 1 16 5.5V7M3 12h18"/>',
    refresh:'<path d="M20 8a8 8 0 0 0-14-2.5L4 8M4 8V4M4 8h4"/><path d="M4 16a8 8 0 0 0 14 2.5L20 16M20 16v4M20 16h-4"/>',
    chart:'<path d="M4 4v16h16"/><path d="M8 15v-3M12 15V8M16 15v-5"/>',
    calendar:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
    user:'<circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/>',
    coins:'<ellipse cx="8.5" cy="7" rx="5.5" ry="3"/><path d="M3 7v4c0 1.6 2.5 3 5.5 3M14 8.2c0-1.6-2.5-3-5.5-3"/><ellipse cx="15.5" cy="15" rx="5.5" ry="3"/><path d="M10 15v-1M21 15v3.8c0 1.6-2.5 3-5.5 3S10 19.4 10 17.8v-3"/>',
    clipboard:'<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4V3.5A1.5 1.5 0 0 1 10.5 2h3A1.5 1.5 0 0 1 15 3.5V4"/><path d="M9 13l2 2 4-4"/>',
    badgecheck:'<path d="M12 2.5l2.3 1.8 2.9-.3 1 2.7 2.4 1.6-1 2.7 1 2.7-2.4 1.6-1 2.7-2.9-.3L12 21.5l-2.3-1.8-2.9.3-1-2.7L3.4 15l1-2.7-1-2.7 2.4-1.6 1-2.7 2.9.3z"/><path d="M9 12l2 2 4-4"/>',
    home:'<path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
    shield:'<path d="M12 3l7 3v6c0 4.8-3.3 7.8-7 9-3.7-1.2-7-4.2-7-9V6z"/>',
    arrow:'<path d="M5 12h13M12 6l6 6-6 6"/>',
    whatsapp:'<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.4 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5-3.8c-.6-.9-1.2-1.9-1.2-2.9 0-.5.2-1 .5-1.4.1-.1.3-.2.4-.2h.5c.1 0 .3 0 .4.3l.6 1.5c.1.1 0 .3 0 .4l-.4.4c-.1.2-.2.3-.1.5.4.7.9 1.3 1.5 1.8.4.3.8.5 1 .6.2.1.3.1.5-.1l.5-.7c.1-.2.3-.2.5-.1l1.4.7c.2.1.4.2.4.3.1.2.1.7-.1 1.3z"/>'
  };
  function svg(p){ return '<svg viewBox="0 0 24 24" aria-hidden="true">'+p+'</svg>'; }
  document.querySelectorAll('[data-icon]').forEach(function(el){
    var n=el.getAttribute('data-icon'); if(I[n]) el.innerHTML=svg(I[n]);
  });

  var y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();

  var b=document.querySelector('.burger'), m=document.getElementById('menu');
  if(b&&m){ b.addEventListener('click',function(){m.classList.toggle('open');});
    m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){m.classList.remove('open');});}); }

  var nav=document.querySelector('header.nav');
  function ns(){ if(nav) nav.classList.toggle('scrolled', window.scrollY>20); }
  ns(); window.addEventListener('scroll',ns,{passive:true});

  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -7% 0px'});
    els.forEach(function(e){io.observe(e);});
  } else { els.forEach(function(e){e.classList.add('in');}); }
})();
