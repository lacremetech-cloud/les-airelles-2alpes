# Les Airelles aux 2 Alpes — landing de conversion

Site statique (HTML/CSS/JS, sans framework), déployé sur Vercel.

- `/` français · `/en/` anglais · `/brochure/` et `/en/brochure/` (dossier du projet, noindex)
- Langue : seule la racine peut rediriger vers `/en/`, et jamais pour un clic publicitaire
  (`utm_*`, `fbclid`, `gclid`…) ni après un choix manuel. `/en/` ne redirige jamais.
- Formulaire : coller le code d'intégration Prodigio OS dans `#dossierForm` (index.html et en/index.html).
- Brochures : générées par `python3 _tools/gen_brochure.py` — modifier le script, pas les HTML.
  `CONTACT_URL` en tête du script active les boutons de contact.
- Vidéo d'accueil (desktop) : attribut `data-video` de `#hero` (ID YouTube). Mobile : poster seul.
- Images : WebP dans `assets/img` (828/1280/1920/2560 px), plans dans `assets/plans`.
  Photos d'ambiance : Unsplash (licence Unsplash, usage commercial autorisé).
