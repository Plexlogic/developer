# Plexus Developer

![GitHub Pages](https://github.com/Plexlogic/developer/actions/workflows/gh_pages.yml/badge.svg)

This is the source code for [developer.plexus.co](https://developer.plexus.co).

It uses [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

GitHub Actions is configured to publish the `main` branch automatically.

You can edit the content directly in <https://github.dev/Plexlogic/developer> or by clicking <kbd>.</kbd> in the [GitHub repository](https://github.com/Plexlogic/developer).

To develop locally, just run `mkdocs serve` or launch VS Code in dev container (`.devcontainer` configured).

## Office Add-in Manifests

The production Office add-in manifest files are hosted at:

- `developer.plexus.co/office-addins/manifest-plexus-outlook.xml`
- `developer.plexus.co/office-addins/manifest-plexus-word.xml`

These are copies of the production manifests from the [`ltm-outlook-add-in`](https://github.com/Plexlogic/ltm-outlook-add-in) repo. If the manifests are updated there, copy the new versions here:

```bash
cp /path/to/ltm-outlook-add-in/manifest-plexus-outlook-production.xml docs/office-addins/manifest-plexus-outlook.xml
cp /path/to/ltm-outlook-add-in/manifest-plexus-word-production.xml docs/office-addins/manifest-plexus-word.xml
```

Then commit and push to `main` to deploy.