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

What to do next ?

 - Fix front container to use it instead of running vite server from local. So far there is an error on the page and vite server is not
 accessible.
