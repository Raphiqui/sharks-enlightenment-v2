# sharks-enlightenment-v2
Improvement of sharks-enlightenment version 1. Goal is to make it more maintainable and start fresh.

Django-Vite Architecture Summary
In Development:

The front/ directory contains Vue source code and runs a Vite dev server (via Docker or locally)
Django connects to this dev server to enable hot module reload (HMR) for instant updates
The front/ container exists purely for development convenience

In Production:

Only the back/ directory is deployed
Run npm run build in front/ to generate static assets into back/static/dist/
Django serves these pre-built assets as regular static files
The front/ directory is never deployed - it's just a build tool

Key Insight:
Think of the frontend as a "compiler" - the source code (front/src/) gets compiled into static bundles (back/static/dist/), and only the compiled output goes to production. Vite's dev server is purely for development ergonomics (HMR, fast rebuilds), not a production requirement.
Docker Setup:

Development: Both back and front containers run
Production: Only deploy the back/ directory with built assets included

## Internationalization (i18n)

This project supports English, French, and Spanish. Static text in Django templates and Vue components is translated based on the current URL locale (e.g., `/fr/`, `/es/`).

### Compiling Translation Messages

After modifying `.po` files or extracting new strings, compile them to binary `.mo` files:

```bash
cd back && python manage.py compilemessages
```

### Extracting New Strings

To scan the codebase for new translatable strings and update `.po` files:

```bash
cd back && python manage.py makemessages -l fr -l es
```

### Vue Component Translations

Vue components use a custom `front/src/i18n.js` module. To add or modify translations, edit the locale objects in that file. The language is automatically detected from Django via `window.DJANGO_LANGUAGE`.

### Railway

If somehow the changes are not reflected, try to change the `CACHE_BUST` variable to something else.
