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
            // La vidéo n'est visible que pendant la lecture : en pause ou en
            // chargement, YouTube affiche son icône — on montre alors l'image fixe.
            frame.classList.toggle('is-playing', e.data === YT.PlayerState.PLAYING);
            if (e.data === YT.PlayerState.PLAYING) hero.classList.add('has-video');
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
    if (!modal.classList.contains('is-open')) return;
    if (e.key === 'Escape') { closeModal(); return; }
    // Le focus clavier reste dans la modale tant qu'elle est ouverte
    if (e.key === 'Tab') {
      const focusables = [...modal.querySelectorAll('a[href], button, input, select, textarea, iframe, [tabindex]:not([tabindex="-1"])')]
        .filter(el => !el.disabled && el.offsetParent !== null);
      if (!focusables.length) return;
      const first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------- Reflet des CTA : seulement quand le bouton est à l'écran ---------- */
  if ('IntersectionObserver' in window) {
    const btnIo = new IntersectionObserver(entries => {
      entries.forEach(e => e.target.classList.toggle('est-en-vue', e.isIntersecting));
    });
    document.querySelectorAll('.btn').forEach(b => btnIo.observe(b));
  }

  /* ---------- Travelling lent sur les grandes images ---------- */
  if ('IntersectionObserver' in window) {
    const sceneIo = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('in-view'); sceneIo.unobserve(entry.target); }
      });
    }, { threshold: 0.2 });
    document.querySelectorAll('.scene').forEach(el => sceneIo.observe(el));
  }

  /* ---------- Altimètre (desktop) : du village, 1 650 m, au glacier, 3 600 m ---------- */
  const ALT_MIN = 1650, ALT_MAX = 3600;
  if (window.matchMedia('(min-width: 1400px)').matches) {
    const fmt = n => n.toLocaleString(isEn ? 'en-GB' : 'fr-FR') + ' m';
    const pct = alt => ((alt - ALT_MIN) / (ALT_MAX - ALT_MIN)) * 100;
    const alti = document.createElement('div');
    alti.className = 'alti';
    alti.setAttribute('aria-hidden', 'true');
    let html = '<span class="alti__track"></span>';
    for (let a = 1750; a < ALT_MAX; a += 250) html += `<span class="alti__tick" style="bottom:${pct(a)}%"></span>`;
    const marks = [[ALT_MIN, isEn ? 'Village' : 'Village'], [3200, 'Jandri'], [ALT_MAX, isEn ? 'Glacier' : 'Glacier']];
    marks.forEach(([a, name]) => {
      html += `<span class="alti__tick alti__tick--major" style="bottom:${pct(a)}%"></span>`;
      html += `<span class="alti__label" style="bottom:${pct(a)}%;transform:translateY(50%)">${name}</span>`;
    });
    html += '<span class="alti__mark"></span><span class="alti__read"></span>';
    alti.innerHTML = html;
    document.body.appendChild(alti);
    const mark = alti.querySelector('.alti__mark');
    const read = alti.querySelector('.alti__read');
    const labels = alti.querySelectorAll('.alti__label');

    let ticking = false;
    const update = () => {
      ticking = false;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      const alt = Math.round((ALT_MIN + ratio * (ALT_MAX - ALT_MIN)) / 10) * 10;
      const pos = `${ratio * 100}%`;
      mark.style.bottom = pos;
      read.style.bottom = pos;
      read.textContent = fmt(alt);
      // Le relevé courant remplace l'étiquette fixe qu'il recouvre
      labels.forEach((l, i) => { l.style.opacity = Math.abs(pct(marks[i][0]) - ratio * 100) < 6 ? '0' : ''; });
      alti.classList.toggle('is-on', window.scrollY > window.innerHeight * 0.6);
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

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
