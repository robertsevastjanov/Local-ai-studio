# Local AI Studio — Changelog

## 2026-10-15 — Image Generation UI and CSS Refactoring

### Added
- Image generation form with prompt, steps and seed settings.
- Nuxt API proxy for FastAPI image generation.
- Image preview and expanded generation gallery.
- Image modal and missing-image handling.
- External stylesheet: frontend/app/assets/css/main.css.

### Changed
- Moved 423 CSS lines out of app.vue.
- Configured Nuxt to load the external stylesheet.
- Reduced app.vue from 701 to 276 lines.

### Verified
- Nuxt interface works after server restart.
- Playwright gallery tests: 3 passed.
- Nuxt generation API previously tested manually.

### Not yet implemented
- Gallery pagination: latest 500 images, 50 per page.
- Automated end-to-end test for real image generation.
- Long-prompt optimization using a local language model.

### Next
- Move the main page into pages/index.vue.
- Split the interface into reusable Vue components.

## 2026-10-15 — Nuxt Migration and Y2K UI

### Changed
- Moved the Nuxt home page to `frontend/app/pages/index.vue`.
- Simplified `frontend/app/app.vue` to use `NuxtPage`.
- Updated the interface with glossy Y2K gradients, 3D buttons and stronger image hover effects.
- Updated Playwright configuration to use `localhost`.

### Removed
- Legacy FastAPI HTML route `/` and static mount `/static`.
- Legacy `templates/index.html` and `static/style.css`.

### Verification
- FastAPI route inspection: `/health`, `/generate`, `/history`, `/images` present.
- Legacy `/` and `/static` routes absent.
- Playwright gallery tests: 3 passed.
- Nuxt UI and new CSS visually checked.
- Full image generation was not retested in this change.
