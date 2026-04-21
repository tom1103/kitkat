# Kitkat - Documentation Danfoss

Ce projet est prêt à être déployé sur **GitHub Pages** en utilisant **Jekyll**.

## Comment déployer sur GitHub Pages

1. **Créez un nouveau dépôt** sur GitHub.
2. **Poussez ces fichiers** sur la branche `main`.
3. Allez dans **Settings** > **Pages** de votre dépôt GitHub.
4. Dans la section **Build and deployment**, choisissez :
   - Source : **Deploy from a branch**
   - Branch : **main** / **(root)**
5. Cliquez sur **Save**.

Votre site sera bientôt disponible à l'adresse `https://votre-pseudo.github.io/votre-depot/`.

## Structure du projet

- `index.md` : Contenu principal (formaté pour Jekyll).
- `_config.yml` : Configuration du site.
- `_layouts/default.html` : Structure HTML (Design Premium).
- `assets/css/style.css` : Styles personnalisés (Glassmorphism).
- `Gemfile` : Dépendances Jekyll.
