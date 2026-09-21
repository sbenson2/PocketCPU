# PocketCPU website

This repository contains the public website, product materials, and support tracker for [PocketCPU](https://sbenson2.github.io/PocketCPU/). The application and companion source are maintained privately and are not published by this site.

Preview:

```sh
python3 -m http.server 8000
```

Check and stage the exact Pages payload:

```sh
./check-site.sh
python3 scripts/build-site.py
```

The project is in development. The build stages only the four pages, stylesheet, robots/sitemap files, `.nojekyll`, and four approved assets into ignored `_site/`. The Pages workflow checks pull requests and deploys `main` automatically; it can also be run manually. There are no external runtime dependencies or tracking scripts.

Use public issues for general support and the [private reporting channel](SECURITY.md) for vulnerabilities. [Asset usage](ASSETS.md) and [design notes](DESIGN.md) describe the public materials. App Store availability, a public relay service, and desktop installers remain planned.
