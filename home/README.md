---
description: "A consolidated Nearmap documentation experience for product users, administrators, and developers."
icon: house
cover: "https://raw.githubusercontent.com/gitbook-demo-sites/nearmap-demo-site-20260707/main/assets/nearmap-cover.svg"
coverY: 0
layout:
  width: wide
  cover:
    visible: true
    size: hero
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: false
  outline:
    visible: false
  pagination:
    visible: true
---

# Welcome to Nearmap

{% columns %}
{% column width="50%" %}
Bring product documentation, help content, API guidance, and generated reference pages into one searchable GitBook site. This first draft focuses on a representative slice of Nearmap's public help center and one API surface rather than a full migration.

<button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">Ask the Nearmap docs</button>

<button type="button" class="button secondary" data-action="ask" data-query="How do I get started with MapBrowser?" data-icon="map">MapBrowser</button> <button type="button" class="button secondary" data-action="ask" data-query="Which API should I use for AI property features?" data-icon="code">APIs</button>
{% endcolumn %}

{% column width="50%" %}
{% hint style="success" icon="gitbook" %}
**A note from GitBook**

This demo follows the Evolve example pattern: a strong homepage, visible product paths, developer entry points, support content, and a generated OpenAPI reference. It is intentionally scoped to a first-draft consolidation story for Nearmap.
{% endhint %}
{% endcolumn %}
{% endcolumns %}

## Choose your path

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><h4><i class="fa-map-location-dot" style="color:$primary;"></i></h4></td><td><h4><strong>Product documentation</strong></h4></td><td>MapBrowser, Roof Assessment, Betterview, admin tasks, and support workflows.</td><td><a href="https://app.gitbook.com/s/XSPACE_PRODUCT/">Product documentation</a></td></tr>
<tr><td><h4><i class="fa-code" style="color:$primary;"></i></h4></td><td><h4><strong>Developer and API</strong></h4></td><td>API chooser, authentication, standards, and generated AI Feature API reference.</td><td><a href="https://app.gitbook.com/s/XSPACE_API/">Developer and API</a></td></tr>
<tr><td><h4><i class="fa-route" style="color:$primary;"></i></h4></td><td><h4><strong>Demo map</strong></h4></td><td>What was consolidated, what was left out, and where feedback is most useful.</td><td><a href="demo-map.md">Demo map</a></td></tr>
</tbody></table>

## Product, APIs, and answers in one place

{% columns %}
{% column width="66%" %}
<details open>
<summary><i class="fa-map" style="color:$primary;"></i> <strong>Product help</strong></summary>

The public Help Center already organizes MapBrowser, Roof Assessment, Betterview, Nearmap Content, Integrations, APIs, and account management. GitBook keeps that reader model, then adds clearer landing pages and reusable review workflows.

<a href="https://app.gitbook.com/s/XSPACE_PRODUCT/" class="button secondary">Open product docs</a>
</details>

<details open>
<summary><i class="fa-code" style="color:$primary;"></i> <strong>Developer docs</strong></summary>

The API Hub explains how to choose between Tile, Coverage, AI Feature, Roof Age, WMS, DSM/True Ortho, Transactional Content, and Betterview APIs. This demo narrows the generated reference to AI Feature API.

<a href="https://app.gitbook.com/s/XSPACE_API/" class="button secondary">Open developer docs</a>
</details>
{% endcolumn %}

{% column width="34%" %}
#### What is in scope

<table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody>
<tr><td><strong>Product docs</strong></td><td>Representative MapBrowser, Roof Assessment, Betterview, admin, and support pages.</td><td></td></tr>
<tr><td><strong>API docs</strong></td><td>One generated AI Feature API spec plus surrounding developer handbook pages.</td><td></td></tr>
<tr><td><strong>Design</strong></td><td>Nearmap navy/blue styling, prominent search, AI Assistant, and source links.</td><td></td></tr>
</tbody></table>
{% endcolumn %}
{% endcolumns %}
