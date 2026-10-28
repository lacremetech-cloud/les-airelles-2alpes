/* ============================================================
   LES AIRELLES AUX 2 ALPES — Interactivité
============================================================ */

(() => {
  'use strict';

  const isEn = document.documentElement.lang === 'en';

  /* ---------- Nav : état au scroll ---------- */
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  const burger = document.getElementById('navBurger');
  const navMobile = document.getElementById('navMobile');
  const closeMenu = () => {
    navMobile.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };
  burger.addEventListener('click', () => {
    const open = navMobile.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  });
  navMobile.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));

  /* ---------- Langue : mémorise le choix manuel ---------- */
  document.querySelectorAll('.nav__lang a[data-lang]').forEach(link => {
    link.addEventListener('click', () => {
      try { localStorage.setItem('langChoice', link.dataset.lang); } catch (e) {}
    });
  });

  /* ---------- Bouton fixe mobile : visible après l'accueil ---------- */
  const hero = document.getElementById('hero');
  const sticky = document.getElementById('stickyCta');
  if (hero && sticky && 'IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      const show = !entry.isIntersecting;
      sticky.classList.toggle('is-visible', show);
      sticky.setAttribute('aria-hidden', String(!show));
      sticky.querySelector('button').tabIndex = show ? 0 : -1;
    }, { threshold: 0.1 }).observe(hero);
  }

  /* ---------- Vidéo d'accueil : desktop uniquement ----------
     Sur mobile (trafic publicitaire), seule l'image poster s'affiche :
     aucun octet de vidéo n'est chargé. */
  const canPlayHeroVideo = () => {
    if (!hero || !hero.dataset.video) return false;
    if (!window.matchMedia('(min-width: 769px)').matches) return false;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return false;
    const conn = navigator.connection;
    if (conn && (conn.saveData || /2g/.test(conn.effectiveType || ''))) return false;
    return true;
  };

  const loadYouTubeApi = () => new Promise(resolve => {
    if (window.YT && window.YT.Player) return resolve();
    const prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { if (prev) prev(); resolve(); };
    const s = document.createElement('script');
    s.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(s);
  });

  const startHeroVideo = () => {
    if (!canPlayHeroVideo()) return;
    const id = hero.dataset.video;
    const start = parseInt(hero.dataset.start || '0', 10);
    const holder = document.createElement('div');
    hero.querySelector('.hero__media').insertBefore(holder, hero.querySelector('.hero__overlay'));
    loadYouTubeApi().then(() => {
      const player = new YT.Player(holder, {
        videoId: id,
        host: 'https://www.youtube-nocookie.com',
        playerVars: {
          autoplay: 1, mute: 1, controls: 0, disablekb: 1, fs: 0, rel: 0,
          playsinline: 1, iv_load_policy: 3, modestbranding: 1, start
        },
        events: {
          onReady: e => { e.target.mute(); e.target.playVideo(); },
          onStateChange: e => {
            const frame = player.getIframe();
            if (e.data === YT.PlayerState.PLAYING) {
              frame.classList.add('is-playing');
              hero.classList.add('has-video');
            }
            // Boucle : on relance avant la fin pour ne jamais montrer l'écran de fin YouTube
            if (e.data === YT.PlayerState.ENDED) { player.seekTo(start); player.playVideo(); }
          }
        }
      });
      const frame = player.getIframe();
      frame.classList.add('hero__video');
      frame.setAttribute('aria-hidden', 'true');
      frame.setAttribute('tabindex', '-1');
      frame.title = '';
      // Pause quand l'accueil sort de l'écran
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(([entry]) => {
          if (!player.playVideo) return;
          entry.isIntersecting ? player.playVideo() : player.pauseVideo();
        }, { threshold: 0.05 }).observe(hero);
      }
    });
  };
  // Après le chargement complet : l'image et le texte passent d'abord
  if (document.readyState === 'complete') setTimeout(startHeroVideo, 600);
  else window.addEventListener('load', () => setTimeout(startHeroVideo, 600));

  /* ---------- Film 3D du projet : chargé seulement au clic ---------- */
  const film = document.getElementById('film');
  if (film) {
    film.querySelector('.js-play-film').addEventListener('click', () => {
      const start = parseInt(film.dataset.start || '0', 10);
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube-nocookie.com/embed/${film.dataset.video}?autoplay=1&start=${start}&rel=0&modestbranding=1&playsinline=1`;
      iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      iframe.title = isEn ? 'Les Airelles — 3D film of the project' : 'Les Airelles — film 3D du projet';
      film.appendChild(iframe);
      film.querySelector('.js-play-film').remove();
    });
  }

  /* ---------- Avant / après ---------- */
  document.querySelectorAll('.ba').forEach(ba => {
    const input = ba.querySelector('input');
    input.addEventListener('input', () => ba.style.setProperty('--pos', input.value + '%'));
  });

  /* ---------- Révélations au scroll ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('is-visible'));
  }

  /* ---------- Modale du dossier ---------- */
  const modal = document.getElementById('dossierModal');
  let lastFocus = null;
  let savedY = 0;
  const openModal = e => {
    if (e) e.preventDefault();
    closeMenu();
    lastFocus = document.activeElement;
    savedY = window.scrollY;
    // Verrou de scroll compatible iOS
    Object.assign(document.body.style, { position: 'fixed', top: `-${savedY}px`, left: '0', right: '0', width: '100%' });
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    sticky && sticky.classList.remove('is-visible');
    modal.querySelector('.modal__close').focus();
    if (window.fbq) window.fbq('track', 'ViewContent', { content_name: 'Dossier Les Airelles' });
  };
  const closeModal = () => {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    Object.assign(document.body.style, { position: '', top: '', left: '', right: '', width: '' });
    window.scrollTo(0, savedY);
    onScroll();
    if (lastFocus) lastFocus.focus();
  };
  document.querySelectorAll('.js-open-dossier').forEach(b => b.addEventListener('click', openModal));
  document.querySelectorAll('.js-close-modal').forEach(b => b.addEventListener('click', closeModal));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
  });

  /* ---------- Ancres : compense la nav fixe ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target || link.getAttribute('href') === '#top') return;
      e.preventDefault();
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 70, behavior: 'smooth' });
    });
  });
})();
