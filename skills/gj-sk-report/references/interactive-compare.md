# Interactive compare — tab contract

Use only with `templates/comparison-interactive.html`.

## Markup

```html
<nav class="compare-nav" role="tablist" aria-label="compare">
  <button type="button" class="compare-tab is-active" data-compare="both" role="tab" aria-selected="true">both</button>
  <button type="button" class="compare-tab" data-compare="a" role="tab" aria-selected="false">a</button>
  <button type="button" class="compare-tab" data-compare="b" role="tab" aria-selected="false">b</button>
  <button type="button" class="compare-tab" data-compare="contrast" role="tab" aria-selected="false">contrast</button>
</nav>

<section data-compare-panel="both">…</section>
<section data-compare-panel="a" hidden>…</section>
<section data-compare-panel="b" hidden>…</section>
<section data-compare-panel="contrast" hidden>
  <div class="compare-row">
    <div class="compare-col compare-col--a"><span class="compare-col-label">a</span>…</div>
    <div class="compare-col compare-col--b"><span class="compare-col-label">b</span>…</div>
  </div>
</section>
```

## Script (paste once, inline IIFE — no React)

```html
<script>
(function () {
  var tabs = document.querySelectorAll(".compare-tab");
  var panels = document.querySelectorAll("[data-compare-panel]");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var key = tab.getAttribute("data-compare");
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.forEach(function (p) {
        var show = p.getAttribute("data-compare-panel") === key;
        if (show) p.removeAttribute("hidden");
        else p.setAttribute("hidden", "");
      });
    });
  });
})();
</script>
```

Replace labels `a` / `b` with the real option names. Keep 44px tap targets.
