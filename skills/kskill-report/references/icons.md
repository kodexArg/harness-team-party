# Icon Reference — kskill-report

Icon set: **Lucide** (stroke-width 1.75, round caps/joins, 24×24 grid).  
Brand logos: **Simple Icons** (CDN or inline).

---

## 1. Why Inline SVG Is the Default

WhatsApp's in-app webview loads HTML attachments **offline** — no network,
no CDN, no external requests. Inline SVG is the only approach that renders
reliably in that context. Copy the path data directly into your HTML and
it works everywhere: WhatsApp, iMessage, email clients, offline browsers.

The CDN alternative is documented below for convenience when building in a
browser context where network access is guaranteed.

---

## 2. Inline SVG Conventions

Every Lucide icon follows this template:

```html
<!-- Annotated template -->
<svg
  class="icon"           <!-- .icon = 1.1em / .icon-lg = hero size -->
  viewBox="0 0 24 24"    <!-- always 24×24 Lucide grid -->
  fill="none"            <!-- icons are stroked, not filled -->
  stroke="currentColor"  <!-- inherits text color from parent -->
  stroke-width="1.75"    <!-- Lucide house style -->
  stroke-linecap="round" <!-- rounded caps on open paths -->
  stroke-linejoin="round"<!-- rounded joins at corners -->
  width="1.1em"          <!-- overridden by CSS class -->
  height="1.1em"
  aria-hidden="true"
>
  <!-- path data goes here -->
  <polyline points="20 6 9 17 4 12"/>
</svg>
```

CSS to add to your report:

```css
.icon    { width: 1.1em; height: 1.1em; vertical-align: -0.15em; flex-shrink: 0; }
.icon-lg { width: 2em;   height: 2em;   }
```

---

## 3. CDN Alternative (online contexts only)

```html
<!-- In <head> -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>

<!-- Usage -->
<i data-lucide="check"></i>
<i data-lucide="arrow-right"></i>

<!-- Before </body> -->
<script>lucide.createIcons();</script>
```

> **Do not use CDN** for WhatsApp or any offline-first report. Use inline SVG.

---

## 4. Ready-to-Paste Inline SVGs

### check

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"/>
</svg>
```

### x

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <line x1="18" y1="6" x2="6" y2="18"/>
  <line x1="6" y1="6" x2="18" y2="18"/>
</svg>
```

### arrow-right

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
</svg>
```

### chevron-right

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="9 18 15 12 9 6"/>
</svg>
```

### git-branch

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <line x1="6" y1="3" x2="6" y2="15"/>
  <circle cx="18" cy="6" r="3"/>
  <circle cx="6" cy="18" r="3"/>
  <path d="M18 9a9 9 0 0 1-9 9"/>
</svg>
```

### git-commit

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="4"/>
  <line x1="1.05" y1="12" x2="7" y2="12"/>
  <line x1="17.01" y1="12" x2="22.96" y2="12"/>
</svg>
```

### code

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="16 18 22 12 16 6"/>
  <polyline points="8 6 2 12 8 18"/>
</svg>
```

### terminal

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="4 17 10 11 4 5"/>
  <line x1="12" y1="19" x2="20" y2="19"/>
</svg>
```

### alert-triangle

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
  <line x1="12" y1="9" x2="12" y2="13"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>
```

### info

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="8" x2="12" y2="12"/>
  <line x1="12" y1="16" x2="12.01" y2="16"/>
</svg>
```

### clock

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>
```

### rocket

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
  <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>
  <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>
  <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
</svg>
```

### file

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
  <polyline points="13 2 13 9 20 9"/>
</svg>
```

### circle-check (check-circle)

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
  <polyline points="22 4 12 14.01 9 11.01"/>
</svg>
```

### zap

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
</svg>
```

---

## 5. Brand Logos — Simple Icons

Simple Icons CDN rewrites any icon in a single hex color. No JS required.

```html
<!-- GitHub, cream on dark -->
<img src="https://cdn.simpleicons.org/github/F3EEE4" class="icon" alt="GitHub">

<!-- GitHub, orange accent -->
<img src="https://cdn.simpleicons.org/github/ff8c42" class="icon" alt="GitHub">

<!-- Other examples -->
<img src="https://cdn.simpleicons.org/cloudflare/ff8c42" class="icon" alt="Cloudflare">
<img src="https://cdn.simpleicons.org/python/F3EEE4"    class="icon" alt="Python">
<img src="https://cdn.simpleicons.org/typescript/F3EEE4" class="icon" alt="TypeScript">
<img src="https://cdn.simpleicons.org/docker/F3EEE4"    class="icon" alt="Docker">
```

Slug = lowercase brand name, no spaces. Find slugs at [simpleicons.org](https://simpleicons.org).

**Inline alternative** — download the SVG from Simple Icons, strip `fill` attributes,
add `fill="currentColor"`, embed inline. Use when offline portability matters.

---

## 6. Usage Guidelines

- **One accent icon per section header** — place it before the heading text, inline.
- **Hero icon** — use `.icon-lg` (2em), color `#ff8c42` (orange) via explicit `color:` or `stroke:`.
- **Body icons** — use `.icon` (1.1em), `stroke="currentColor"` so they inherit paragraph color.
- **Pair pattern:**

```html
<h2>
  <svg class="icon-lg" style="color:#ff8c42" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
  </svg>
  Highlights
</h2>

<li>
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
  Deploy pipeline green
</li>
```

- `currentColor` cascades — set `color` on a parent container and all
  `.icon` children adopt it automatically.
- Keep icon count low: one per logical item max. Visual noise defeats scannability
  on a small mobile screen.
