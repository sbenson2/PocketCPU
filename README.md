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

The project is in development. The build stages only the four pages, stylesheet, robots/sitemap files, `.nojekyll`, and four approved assets into ignored `_site/`. There are no external runtime dependencies or tracking scripts.

GitHub Pages currently serves the generated `gh-pages` branch with Jekyll disabled. After reviewing and committing source changes, an authenticated maintainer can run:

```sh
python3 scripts/publish-pages.py --publish
```

Without `--publish`, this command only checks and stages the site. Publication uses a temporary checkout and a normal push; it does not switch or reset the source branch. A concurrent update causes a rejected push rather than overwriting another publication. Verify the Pages build and public URL after publishing.

The included Actions workflow validates `main` and pull requests when Actions runners are available. Deployment from that workflow is opt-in: change the Pages source to GitHub Actions and set repository variable `POCKETCPU_PAGES_ACTIONS=true`. Do not use the branch publisher while that mode is enabled. This keeps the working branch publication route independent of custom Actions execution.

Use public issues for general support and the [private reporting channel](SECURITY.md) for vulnerabilities. [Asset usage](ASSETS.md) and [design notes](DESIGN.md) describe the public materials. The site describes development builds only. No App Store download, public relay service, or consumer desktop installer is available.
