from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
REPO = "nearmap-demo-site-20260707"
RAW = f"https://raw.githubusercontent.com/gitbook-demo-sites/{REPO}/main"


def write(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def yaml(space: str) -> None:
    write(
        f"{space}/.gitbook.yaml",
        """
        root: ./
        structure:
          readme: README.md
          summary: SUMMARY.md
        """,
    )


def vars_file(space: str) -> None:
    write(
        f"{space}/.gitbook/vars.yaml",
        """
        company_name: Nearmap
        demo_name: Nearmap Documentation Hub
        review_stage: First-draft demo
        api_spec_slug: nearmap-ai-feature-api-demo
        help_center_url: https://help.nearmap.com/
        developer_url: https://developer.nearmap.com/
        marketing_url: https://www.nearmap.com/
        """,
    )


def summary(space: str, lines: list[str]) -> None:
    write(f"{space}/SUMMARY.md", "# Table of contents\n\n" + "\n".join(lines))


def card(icon: str, title: str, desc: str, href: str) -> str:
    return (
        f'<tr><td><h4><i class="fa-{icon}" style="color:$primary;"></i></h4></td>'
        f"<td><h4><strong>{title}</strong></h4></td><td>{desc}</td>"
        f'<td><a href="{href}">{title}</a></td></tr>'
    )


for slug in ["home", "product-docs", "developer-api"]:
    yaml(slug)
    vars_file(slug)

write(
    "README.md",
    """
    # Nearmap demo site

    First-draft GitBook demo content for Nearmap. Each top-level folder is imported as a separate GitBook space.
    """,
)

write(".gitignore", ".DS_Store\nThumbs.db\n*.swp\n*.swo\n.idea/\n.vscode/\n__pycache__/\n")

write(
    "assets/nearmap-cover.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520" role="img" aria-label="Nearmap Documentation Hub">
      <rect width="1600" height="520" fill="#F7F9FC"/>
      <rect x="0" y="0" width="1600" height="18" fill="#08112E"/>
      <rect x="1040" y="88" width="394" height="300" rx="10" fill="#FFFFFF" stroke="#D9E1F2"/>
      <rect x="1080" y="128" width="314" height="170" rx="6" fill="#EAF1FF"/>
      <path d="M1080 264 L1162 196 L1226 232 L1294 162 L1394 246 L1394 298 L1080 298 Z" fill="#3448FF" opacity=".18"/>
      <path d="M1080 232 L1146 184 L1200 208 L1268 140 L1394 222" fill="none" stroke="#3448FF" stroke-width="5"/>
      <rect x="1080" y="324" width="128" height="12" rx="6" fill="#08112E"/>
      <rect x="1228" y="324" width="166" height="12" rx="6" fill="#3448FF"/>
      <rect x="1080" y="352" width="314" height="10" rx="5" fill="#D9E1F2"/>
      <rect x="1080" y="376" width="236" height="10" rx="5" fill="#D9E1F2"/>
      <text x="96" y="184" font-family="Arial, Helvetica, sans-serif" font-size="86" font-weight="700" fill="#08112E" letter-spacing="0">Nearmap</text>
      <text x="100" y="250" font-family="Arial, Helvetica, sans-serif" font-size="31" fill="#3448FF">Documentation Hub</text>
      <text x="102" y="304" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="#26334D">Product guides, support content, and API reference in one governed experience.</text>
      <rect x="102" y="356" width="264" height="44" rx="6" fill="#3448FF"/>
      <text x="126" y="385" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">Property intelligence docs</text>
    </svg>
    """,
)

write(
    "assets/nearmap-wordmark.svg",
    """
    <svg xmlns="http://www.w3.org/2000/svg" width="500" height="120" viewBox="0 0 500 120" role="img" aria-label="Nearmap">
      <rect width="500" height="120" fill="#FFFFFF"/>
      <text x="24" y="76" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="700" fill="#08112E">Nearmap</text>
      <rect x="262" y="62" width="118" height="8" fill="#3448FF"/>
    </svg>
    """,
)

write(
    "openapi/nearmap-ai-feature-api.yaml",
    """
    openapi: 3.0.3
    info:
      title: Nearmap AI Feature API Demo
      version: "4.0"
      description: Representative OpenAPI spec for one Nearmap API surface, based on the public AI Feature API documentation.
    servers:
      - url: https://api.nearmap.com
    security:
      - apiKeyQuery: []
      - apiKeyHeader: []
    tags:
      - name: AI Features
      - name: Rollups
      - name: Metadata
    paths:
      /ai/features/v4/features.json:
        get:
          tags: [AI Features]
          summary: Return AI features for an AOI and date range
          parameters:
            - $ref: "#/components/parameters/Polygon"
            - $ref: "#/components/parameters/Since"
            - $ref: "#/components/parameters/Until"
            - $ref: "#/components/parameters/Packs"
            - $ref: "#/components/parameters/Classes"
          responses:
            "200":
              description: AI features returned as GeoJSON-like feature data.
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/FeatureResponse"
            "400":
              description: Invalid AOI, date range, class, or pack request.
            "401":
              description: Missing or invalid API key.
            "404":
              description: No matching survey resources found.
        post:
          tags: [AI Features]
          summary: Return AI features using an AOI in the request body
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/AoiRequest"
          responses:
            "200":
              description: AI features returned for the requested AOI.
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/FeatureResponse"
            "400":
              description: Invalid request body or unsupported query combination.
      /ai/features/v4/classes.json:
        get:
          tags: [Metadata]
          summary: List feature and attribute classes available to the caller
          responses:
            "200":
              description: Class metadata.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      classes:
                        type: array
                        items:
                          $ref: "#/components/schemas/Class"
      /ai/features/v4/packs.json:
        get:
          tags: [Metadata]
          summary: List AI packs available to the caller
          responses:
            "200":
              description: Pack metadata.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      packs:
                        type: array
                        items:
                          $ref: "#/components/schemas/Pack"
      /ai/features/v4/rollups.json:
        get:
          tags: [Rollups]
          summary: Return rolled-up AOI facts as JSON
          parameters:
            - $ref: "#/components/parameters/Polygon"
            - $ref: "#/components/parameters/Since"
            - $ref: "#/components/parameters/Until"
            - $ref: "#/components/parameters/Packs"
            - $ref: "#/components/parameters/Classes"
          responses:
            "200":
              description: Aggregated facts for the query AOI.
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/RollupResponse"
        post:
          tags: [Rollups]
          summary: Return rolled-up AOI facts using a request body
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/AoiRequest"
          responses:
            "200":
              description: Aggregated facts for the query AOI.
              content:
                application/json:
                  schema:
                    $ref: "#/components/schemas/RollupResponse"
    components:
      securitySchemes:
        apiKeyQuery:
          type: apiKey
          in: query
          name: apikey
        apiKeyHeader:
          type: apiKey
          in: header
          name: Authorization
      parameters:
        Polygon:
          name: polygon
          in: query
          schema:
            type: string
          description: Closed longitude/latitude polygon for the query AOI.
        Since:
          name: since
          in: query
          schema:
            type: string
            format: date
          description: Earliest capture date to consider.
        Until:
          name: until
          in: query
          schema:
            type: string
            format: date
          description: Latest capture date to consider.
        Packs:
          name: packs
          in: query
          schema:
            type: string
          description: Comma-separated AI pack IDs.
        Classes:
          name: classes
          in: query
          schema:
            type: string
          description: Comma-separated feature class IDs.
      schemas:
        AoiRequest:
          type: object
          properties:
            aoi:
              type: object
              description: GeoJSON Polygon with no interior rings.
            classes:
              type: array
              items:
                type: string
            packs:
              type: array
              items:
                type: string
        FeatureResponse:
          type: object
          properties:
            type:
              type: string
              example: FeatureCollection
            features:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  geometry:
                    type: object
                  properties:
                    type: object
        RollupResponse:
          type: object
          additionalProperties: true
          example:
            roof_count: 3
            total_roof_area_sqft: 4210
            largest_roof_material: tile
        Class:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            type:
              type: string
        Pack:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            classes:
              type: array
              items:
                type: string
    """,
)

write(
    "home/README.md",
    f"""
    ---
    description: "A consolidated Nearmap documentation experience for product users, administrators, and developers."
    icon: house
    cover: "{RAW}/assets/nearmap-cover.svg"
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

    {{% columns %}}
    {{% column width="50%" %}}
    Bring product documentation, help content, API guidance, and generated reference pages into one searchable GitBook site. This first draft focuses on a representative slice of Nearmap's public help center and one API surface rather than a full migration.

    <button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">Ask the Nearmap docs</button>

    <button type="button" class="button secondary" data-action="ask" data-query="How do I get started with MapBrowser?" data-icon="map">MapBrowser</button> <button type="button" class="button secondary" data-action="ask" data-query="Which API should I use for AI property features?" data-icon="code">APIs</button>
    {{% endcolumn %}}

    {{% column width="50%" %}}
    {{% hint style="success" icon="gitbook" %}}
    **A note from GitBook**

    This demo follows the Evolve example pattern: a strong homepage, visible product paths, developer entry points, support content, and a generated OpenAPI reference. It is intentionally scoped to a first-draft consolidation story for Nearmap.
    {{% endhint %}}
    {{% endcolumn %}}
    {{% endcolumns %}}

    ## Choose your path

    <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    {card("map-location-dot", "Product documentation", "MapBrowser, Roof Assessment, Betterview, admin tasks, and support workflows.", "https://app.gitbook.com/s/XSPACE_PRODUCT/")}
    {card("code", "Developer and API", "API chooser, authentication, standards, and generated AI Feature API reference.", "https://app.gitbook.com/s/XSPACE_API/")}
    {card("route", "Demo map", "What was consolidated, what was left out, and where feedback is most useful.", "demo-map.md")}
    </tbody></table>

    ## Product, APIs, and answers in one place

    {{% columns %}}
    {{% column width="66%" %}}
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
    {{% endcolumn %}}

    {{% column width="34%" %}}
    #### What is in scope

    <table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody>
    <tr><td><strong>Product docs</strong></td><td>Representative MapBrowser, Roof Assessment, Betterview, admin, and support pages.</td><td></td></tr>
    <tr><td><strong>API docs</strong></td><td>One generated AI Feature API spec plus surrounding developer handbook pages.</td><td></td></tr>
    <tr><td><strong>Design</strong></td><td>Nearmap navy/blue styling, prominent search, AI Assistant, and source links.</td><td></td></tr>
    </tbody></table>
    {{% endcolumn %}}
    {{% endcolumns %}}
    """,
)

summary(
    "home",
    [
        "* [Home](README.md)",
        "* [Demo map](demo-map.md)",
        "* [Source notes](source-notes.md)",
        "* [Review checklist](review-checklist.md)",
    ],
)

write(
    "home/demo-map.md",
    """
    ---
    description: "How the public Nearmap docs surfaces were consolidated for this demo."
    icon: route
    ---

    # Demo map

    Nearmap currently has a marketing site, a Help Center, and a ReadMe-powered API Hub. The demo does not try to migrate everything. It shows how the most important reader paths could live together in GitBook while still preserving the distinction between product users and developers.

    <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><h4><i class="fa-building" style="color:$primary;"></i></h4></td><td><h4><strong>Property intelligence positioning</strong></h4></td><td>Homepage language reflects Nearmap's AI-enabled property intelligence platform and high-resolution aerial imagery.</td><td><a href="source-notes.md">Source notes</a></td></tr>
    <tr><td><h4><i class="fa-map" style="color:$primary;"></i></h4></td><td><h4><strong>Product documentation</strong></h4></td><td>Selected help-center topics become a reader-friendly product space.</td><td><a href="https://app.gitbook.com/s/XSPACE_PRODUCT/">Product documentation</a></td></tr>
    <tr><td><h4><i class="fa-code" style="color:$primary;"></i></h4></td><td><h4><strong>API docs</strong></h4></td><td>The API Hub becomes a developer space with one generated OpenAPI spec.</td><td><a href="https://app.gitbook.com/s/XSPACE_API/">Developer and API</a></td></tr>
    </tbody></table>

    ## Suggested demo flow

    {% stepper %}
    {% step %}
    Open the homepage and show that product users and developers share one search and AI Assistant.
    {% endstep %}

    {% step %}
    Move into Product Documentation and show the product category cards, getting-started path, and support resources.
    {% endstep %}

    {% step %}
    Move into Developer and API, then show the API chooser and generated AI Feature API reference.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "home/source-notes.md",
    """
    ---
    description: "Public source material used to shape the first-draft Nearmap demo."
    icon: link
    ---

    # Source notes

    | Source | Used for |
    | --- | --- |
    | nearmap.com | Brand, product positioning, property intelligence story, and platform language |
    | help.nearmap.com | Product categories, popular article themes, FAQ, troubleshooting, and support model |
    | developer.nearmap.com | API Hub structure, API chooser, authentication model, and AI Feature API reference |
    | Evolve demo site | Homepage structure, card-first navigation, columns, AI Assistant buttons, and demo note pattern |

    {% hint style="info" %}
    This is not a complete content migration. It is a scoped sales demo that shows consolidation quality, GitBook-native blocks, and OpenAPI generation from one representative API surface.
    {% endhint %}
    """,
)

write(
    "home/review-checklist.md",
    """
    ---
    description: "Feedback prompts for the Nearmap demo site review."
    icon: clipboard-check
    ---

    # Review checklist

    | Area | Question |
    | --- | --- |
    | Scope | Is AI Feature API the best single API spec to show first, or should we swap to Tile or Transactional Content? |
    | Product docs | Are MapBrowser, Roof Assessment, Betterview, and Account Management the right representative product set? |
    | Branding | Does the dark navy and bright blue treatment feel close enough for a first review? |
    | Story | Should the consolidation story emphasize customer self-service, developer onboarding, or internal docs governance more strongly? |
    | Next pass | Do we need persona-specific content for administrators, insurance teams, government teams, and developers? |
    """,
)

summary(
    "product-docs",
    [
        "* [Product Documentation](README.md)",
        "* [Getting started](getting-started.md)",
        "",
        "## Core products",
        "* [MapBrowser quick start](core-products/mapbrowser-quick-start.md)",
        "* [Measuring and annotations](core-products/measuring-and-annotations.md)",
        "* [Roof Assessment](core-products/roof-assessment.md)",
        "* [Betterview overview](core-products/betterview-overview.md)",
        "",
        "## Administration",
        "* [Account and user management](administration/account-and-user-management.md)",
        "* [Data usage](administration/data-usage.md)",
        "",
        "## Support",
        "* [FAQ](support/faq.md)",
        "* [Troubleshooting](support/troubleshooting.md)",
        "* [Release notes model](support/release-notes.md)",
    ],
)

write(
    "product-docs/README.md",
    """
    ---
    description: "Representative product documentation consolidated from the public Nearmap Help Center."
    icon: map-location-dot
    layout:
      width: wide
      title:
        visible: true
      description:
        visible: true
      tableOfContents:
        visible: false
      outline:
        visible: false
    ---

    # Product Documentation

    The Help Center covers product docs, getting started guides, troubleshooting, FAQ, webinars, tutorials, technical blog posts, and community support. This space keeps that reader model but trims it to the most demo-worthy product documentation paths.

    <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><h4><i class="fa-map" style="color:$primary;"></i></h4></td><td><h4><strong>MapBrowser</strong></h4></td><td>Look up locations, navigate high-resolution aerial imagery, measure, annotate, and collaborate.</td><td><a href="core-products/mapbrowser-quick-start.md">MapBrowser quick start</a></td></tr>
    <tr><td><h4><i class="fa-house-chimney-crack" style="color:$primary;"></i></h4></td><td><h4><strong>Roof Assessment</strong></h4></td><td>Inspect properties, monitor roof condition, and generate Building Condition reports.</td><td><a href="core-products/roof-assessment.md">Roof Assessment</a></td></tr>
    <tr><td><h4><i class="fa-shield-halved" style="color:$primary;"></i></h4></td><td><h4><strong>Betterview</strong></h4></td><td>Insurance property intelligence for underwriting, renewals, claims, and portfolio risk.</td><td><a href="core-products/betterview-overview.md">Betterview overview</a></td></tr>
    <tr><td><h4><i class="fa-user-gear" style="color:$primary;"></i></h4></td><td><h4><strong>Administration</strong></h4></td><td>Invite users, manage access, set up API applications, and monitor account usage.</td><td><a href="administration/account-and-user-management.md">Account management</a></td></tr>
    </tbody></table>

    ## GitBook consolidation angle

    {% columns %}
    {% column %}
    **Readers get one path.** Product, admin, support, and API guidance no longer feel split across disconnected surfaces.
    {% endcolumn %}

    {% column %}
    **Editors get governance.** Ownership, review status, page feedback, Git Sync, and change requests can sit behind the public experience.
    {% endcolumn %}
    {% endcolumns %}
    """,
)

write(
    "product-docs/getting-started.md",
    """
    ---
    description: "A first-day path for new Nearmap users and administrators."
    icon: rocket
    ---

    # Getting started

    New Nearmap users usually need to understand the product, access their subscription, find imagery, and know where to get support. Administrators also need to invite users, configure applications, and monitor usage.

    {% stepper %}
    {% step %}
    **Sign in and confirm access**

    Confirm your subscription and product access in MyAccount. If you cannot see a product, ask your Nearmap administrator to confirm your permissions.
    {% endstep %}

    {% step %}
    **Open MapBrowser**

    Search for a location, inspect available imagery, and use projects to organize work with your team.
    {% endstep %}

    {% step %}
    **Invite your team**

    Administrators can invite users, assign permissions, and set up access to integrations or API applications.
    {% endstep %}

    {% step %}
    **Use support and community**

    Search help articles, troubleshoot common issues, and contact support when account-specific help is needed.
    {% endstep %}
    {% endstepper %}
    """,
)

write(
    "product-docs/core-products/mapbrowser-quick-start.md",
    """
    ---
    description: "Representative MapBrowser quick-start content."
    icon: map
    ---

    # MapBrowser quick start

    MapBrowser is the web-based mapping and measurement platform for exploring Nearmap high-resolution aerial imagery in 2D and 3D.

    ## Common jobs

    <table><thead><tr><th>Job</th><th>What the user needs</th></tr></thead><tbody>
    <tr><td>Look up a location</td><td>Search by address, place, or coordinate and confirm available imagery dates.</td></tr>
    <tr><td>Compare captures</td><td>Use imagery dates to inspect change over time.</td></tr>
    <tr><td>Organize work</td><td>Create projects so site research and markups can be shared with the team.</td></tr>
    <tr><td>Export evidence</td><td>Use screenshots, reports, or exports when findings need to move into another workflow.</td></tr>
    </tbody></table>

    {% hint style="info" %}
    In a full migration, this page would preserve the original help-center quick-start screenshots and replace long article chains with guided steppers.
    {% endhint %}
    """,
)

write(
    "product-docs/core-products/measuring-and-annotations.md",
    """
    ---
    description: "Measure, annotate, and share site analysis."
    icon: ruler-combined
    ---

    # Measuring and annotations

    Measurement and annotation tools help users turn imagery into evidence for site analysis, risk review, design work, and collaboration.

    {% columns %}
    {% column %}
    **Measure**

    Use line, area, and height measurements when assessing a site. The Help Center notes that measurement precision depends on imagery type, shadows, obstructions, and resolution.
    {% endcolumn %}

    {% column %}
    **Annotate**

    Add markup to call out observations, repairs, boundaries, or follow-up items. Projects keep those annotations organized for teams.
    {% endcolumn %}
    {% endcolumns %}

    ## Demo improvement

    GitBook can combine short product instructions with context, caveats, and related API links so users understand not just which button to click, but how the measurement should be interpreted.
    """,
)

write(
    "product-docs/core-products/roof-assessment.md",
    """
    ---
    description: "Representative Roof Assessment documentation for portfolio condition monitoring."
    icon: house-chimney-crack
    ---

    # Roof Assessment

    Roof Assessment helps facilities and property teams inspect properties, assess roof condition, export portfolios, and generate Building Condition reports.

    ## Workflow

    ```mermaid
    flowchart LR
        Upload[Upload property portfolio] --> Review[List and map views]
        Review --> Inspect[Inspect roof condition]
        Inspect --> Report[Generate Building Condition report]
        Report --> Prioritize[Prioritize repairs and maintenance]
    ```

    ## Key pages to migrate later

    * Roof Assessment quick start
    * View site detections
    * Generate a Building Condition Report
    * Export a portfolio
    """,
)

write(
    "product-docs/core-products/betterview-overview.md",
    """
    ---
    description: "Representative Betterview documentation for insurance workflows."
    icon: shield-halved
    ---

    # Betterview overview

    Betterview is Nearmap's property intelligence platform for insurance. The Help Center positions it around underwriting, quoting, renewals, claims, predictive risk insights, and portfolio health.

    <table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody>
    <tr><td><h4><i class="fa-magnifying-glass-chart" style="color:$primary;"></i></h4></td><td><h4><strong>Property intelligence</strong></h4></td><td>Understand risk exposure, agency performance, and portfolio health.</td></tr>
    <tr><td><h4><i class="fa-list-check" style="color:$primary;"></i></h4></td><td><h4><strong>Bulk ordering</strong></h4></td><td>Upload property portfolios and request analysis at scale.</td></tr>
    <tr><td><h4><i class="fa-cloud-rain" style="color:$primary;"></i></h4></td><td><h4><strong>Claims and risk</strong></h4></td><td>Use imagery and property attributes to accelerate decisions after weather and catastrophe events.</td></tr>
    </tbody></table>
    """,
)

write(
    "product-docs/administration/account-and-user-management.md",
    """
    ---
    description: "Invite users, manage permissions, and prepare API access."
    icon: user-gear
    ---

    # Account and user management

    Administrators manage user invitations, permissions, API applications, and account setup. This is also where API access starts: users need an API application before they can create or use API keys.

    {% hint style="warning" %}
    For API keys, the public developer docs say key creation is handled in MyAccount rather than via an API call.
    {% endhint %}

    ## Admin checklist

    * Invite users and assign appropriate product access.
    * Confirm whether the user needs MapBrowser, Roof Assessment, Betterview, content exports, or API access.
    * Create or confirm the API application that users will associate with API keys.
    * Review account usage and subscription limits regularly.
    """,
)

write(
    "product-docs/administration/data-usage.md",
    """
    ---
    description: "Monitor data usage and help teams understand consumption."
    icon: chart-simple
    ---

    # Data usage

    Nearmap account teams need a clear way to understand data usage, export consumption, and API consumption. A consolidated GitBook page can combine product usage guidance with administrator responsibilities and links into API credit models.

    | Usage area | Documentation need |
    | --- | --- |
    | Imagery and exports | What counts against the subscription and where users can see reports |
    | AI Feature API | AI credits, AI pack access, and user enablement |
    | Transactional Content API | Transactional Credits and co-registered content retrieval |
    | Support | How to investigate unexpected usage |
    """,
)

write(
    "product-docs/support/faq.md",
    """
    ---
    description: "Representative FAQ content from the public Help Center."
    icon: circle-question
    ---

    # FAQ

    ## Why do some survey areas appear incomplete?

    Flight operations depend on weather, air traffic clearance, and imagery quality. If conditions change during capture, a survey may be incomplete and may need to be flown again later.

    ## Why did I not receive a password reset email?

    Check junk mail first. If the user account has been disabled, the organization administrator needs to enable access again.

    ## Should I use Simple or Custom WMS?

    Simple WMS is best when users only need the latest imagery for their area. Custom WMS supports geofencing, configured regions, and time navigation.

    ## Will AI Feature API return raster data?

    No. AI Feature API returns vector datasets.
    """,
)

write(
    "product-docs/support/troubleshooting.md",
    """
    ---
    description: "Troubleshooting paths for common Nearmap product and API issues."
    icon: screwdriver-wrench
    ---

    # Troubleshooting

    The Help Center has a dedicated troubleshooting resource. In GitBook, troubleshooting can be organized by symptom, product, and likely owner.

    <table><thead><tr><th>Symptom</th><th>First check</th><th>Escalation</th></tr></thead><tbody>
    <tr><td>Images look darker than expected</td><td>Compare imagery type, date, and display settings.</td><td>Product support if the issue affects multiple surveys.</td></tr>
    <tr><td>Location search returns no result</td><td>Try alternate address formatting or coordinates.</td><td>Support if coverage should exist.</td></tr>
    <tr><td>Export image is pixelated</td><td>Confirm export size, source imagery, and zoom level.</td><td>Support if source resolution seems wrong.</td></tr>
    <tr><td>API key does not work</td><td>Confirm key validity, application association, and request format.</td><td>Administrator or support depending on account setup.</td></tr>
    </tbody></table>
    """,
)

write(
    "product-docs/support/release-notes.md",
    """
    ---
    description: "A GitBook Updates model for product news."
    icon: clock-rotate-left
    layout:
      width: wide
    ---

    # Release notes model

    This page demonstrates how Nearmap product news and release notes could move from article lists into GitBook's Updates block.

    {% updates format="full" %}
    {% update date="2026-07-07" tags="mapbrowser,docs" %}
    ## MapBrowser documentation refresh

    Restructured quick starts, measurement guidance, collaboration topics, and export notes into a single MapBrowser path.
    {% endupdate %}

    {% update date="2026-07-07" tags="api,ai" %}
    ## AI Feature API reference generated from OpenAPI

    Added a generated API reference for AI features, metadata, and rollups so endpoint pages stay aligned with the spec.
    {% endupdate %}
    {% endupdates %}
    """,
)

summary(
    "developer-api",
    [
        "* [Developer and API](README.md)",
        "* [Choose an API](choose-an-api.md)",
        "* [Authentication](authentication.md)",
        "* [Nearmap API standard](nearmap-api-standard.md)",
        "",
        "## AI Feature API",
        "* [Overview](ai-feature-api/README.md)",
        "* [Use the AI Feature API](ai-feature-api/use-the-api.md)",
        "* ```yaml",
        "  type: builtin:openapi",
        "  props:",
        "    models: true",
        "    downloadLink: true",
        "  dependencies:",
        "    spec:",
        "      ref:",
        "        kind: openapi",
        "        spec: nearmap-ai-feature-api-demo",
        "  ```",
    ],
)

write(
    "developer-api/README.md",
    """
    ---
    description: "Developer onboarding and one generated API reference for the Nearmap AI Feature API."
    icon: code
    layout:
      width: wide
      tableOfContents:
        visible: false
      outline:
        visible: false
    ---

    # Developer and API

    Nearmap's API Hub helps developers choose the right API for imagery, coverage, 3D content, AI property features, WMS integrations, and insurance workflows. This demo keeps the chooser and authentication guidance, then generates reference pages for one selected surface: AI Feature API.

    <table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
    <tr><td><h4><i class="fa-compass" style="color:$primary;"></i></h4></td><td><h4><strong>Choose an API</strong></h4></td><td>Find the right Nearmap API for tiles, coverage, AI data, WMS, or transactional content.</td><td><a href="choose-an-api.md">Choose an API</a></td></tr>
    <tr><td><h4><i class="fa-key" style="color:$primary;"></i></h4></td><td><h4><strong>Authentication</strong></h4></td><td>API key model, MyAccount setup, and request patterns.</td><td><a href="authentication.md">Authentication</a></td></tr>
    <tr><td><h4><i class="fa-brain" style="color:$primary;"></i></h4></td><td><h4><strong>AI Feature API</strong></h4></td><td>Retrieve vector AI features and rollups for property AOIs.</td><td><a href="ai-feature-api/README.md">AI Feature API</a></td></tr>
    </tbody></table>

    {% hint style="info" %}
    Demo scope: only the AI Feature API spec is generated. Tile, Coverage, WMS, Roof Age, DSM/True Ortho, Transactional Content, and Betterview can be added later as additional specs or sections.
    {% endhint %}
    """,
)

write(
    "developer-api/choose-an-api.md",
    """
    ---
    description: "A concise version of the Nearmap API chooser."
    icon: compass
    ---

    # Choose an API

    | API | What it does | Typical use case |
    | --- | --- | --- |
    | Tile API | Streams Vertical and Panorama imagery tiles using Web Mercator XYZ coordinates. | Custom map viewers and basemap integrations |
    | Coverage API | Returns survey metadata, dates, content types, and resolution for a location. | Date pickers, coverage checks, survey listing |
    | DSM and True Ortho API | Provides 3D content, Digital Surface Model, and True Ortho imagery. | Elevation analysis, solar assessment, small-area 3D visualization |
    | AI Feature API | Returns vector AI features and rollup summaries for an AOI. | Insurance underwriting, property assessment, damage detection |
    | Transactional Content API | Retrieves multiple co-registered content types per transaction. | Property workflows that need imagery and AI data aligned |
    | WMS API | OGC-compliant WMS for GIS and CAD tools. | ArcGIS, QGIS, AutoCAD, and non-tile-based applications |
    | Roof Age API | Estimates roof installation date using imagery, AI, and third-party data. | Insurance policy rating and claims |
    | Betterview API | Provides insurance-specific property and risk data. | Underwriting, claims, and portfolio analysis |

    ## Recommendation

    If you are building an interactive map, start with Tile API and Coverage API. If you need structured property data or AI-derived attributes for specific addresses, start with Transactional Content API or AI Feature API.
    """,
)

write(
    "developer-api/authentication.md",
    """
    ---
    description: "Nearmap API key authentication for integrations."
    icon: key
    ---

    # Authentication

    Nearmap APIs use API Key authentication so applications can consume Nearmap imagery and data without using a username and password in each request.

    ## Key management

    {% stepper %}
    {% step %}
    **Create or confirm an API application**

    If no application exists, ask a Nearmap administrator to create one in MyAccount.
    {% endstep %}

    {% step %}
    **Create an API key**

    Users create API keys in MyAccount and associate them with an application.
    {% endstep %}

    {% step %}
    **Send the key with every request**

    The public docs describe two supported patterns: the `apikey` URL parameter or an HTTP Authorization header.
    {% endstep %}

    {% step %}
    **Refresh before expiry**

    API keys are valid until deleted, but may need periodic refresh. Check the expiry date in MyAccount.
    {% endstep %}
    {% endstepper %}

    {% tabs %}
    {% tab title="Query parameter" %}
    ```bash
    curl "https://api.nearmap.com/ai/features/v4/classes.json?apikey=$NEARMAP_API_KEY"
    ```
    {% endtab %}

    {% tab title="Header" %}
    ```bash
    curl "https://api.nearmap.com/ai/features/v4/classes.json" \\
      -H "Authorization: Apikey $NEARMAP_API_KEY"
    ```
    {% endtab %}
    {% endtabs %}
    """,
)

write(
    "developer-api/nearmap-api-standard.md",
    """
    ---
    description: "Common Nearmap API design standards."
    icon: brackets-curly
    ---

    # Nearmap API standard

    The public API standard describes Nearmap APIs as HTTPS-only, globally routed, namespaced, versioned, hosted on `api.nearmap.com`, and rate limited.

    ## URL pattern

    ```text
    https://api.nearmap.com/{namespace}/{version}/{resource}?{query}
    ```

    ## Standard integration checklist

    * Confirm the API namespace and version.
    * Verify whether the endpoint expects path parameters, query parameters, or a request body.
    * Send the API key with every request.
    * Handle rate limit headers and retry behavior.
    * Log request IDs or external references when supported.
    """,
)

write(
    "developer-api/ai-feature-api/README.md",
    """
    ---
    description: "Retrieve AI-derived vector property features for a small area of interest."
    icon: brain
    ---

    # AI Feature API

    The AI Feature API retrieves vector AI content for a small Area of Interest (AOI). It is useful for property assessment workflows that need features such as roofs, trees, pools, solar panels, surfaces, and related attributes.

    ## When to use it

    <table data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody>
    <tr><td><h4><i class="fa-map-pin" style="color:$primary;"></i></h4></td><td><h4><strong>Distributed AOIs</strong></h4></td><td>Query many small property parcels across broad geographies.</td></tr>
    <tr><td><h4><i class="fa-database" style="color:$primary;"></i></h4></td><td><h4><strong>Large datasets</strong></h4></td><td>Use date queries to retrieve latest available features across regions.</td></tr>
    <tr><td><h4><i class="fa-rotate" style="color:$primary;"></i></h4></td><td><h4><strong>Regular updates</strong></h4></td><td>Automate recurring retrieval instead of relying on manual MapBrowser exports.</td></tr>
    <tr><td><h4><i class="fa-bolt" style="color:$primary;"></i></h4></td><td><h4><strong>Real-time access</strong></h4></td><td>Return pre-processed AI content quickly for customer-facing applications.</td></tr>
    </tbody></table>

    {% hint style="warning" %}
    Access requires AI credits, subscription to at least one AI Pack, and user enablement by an administrator.
    {% endhint %}
    """,
)

write(
    "developer-api/ai-feature-api/use-the-api.md",
    """
    ---
    description: "A representative AI Feature API workflow."
    icon: code-branch
    ---

    # Use the AI Feature API

    AI Feature API calls start with an AOI. That AOI can come from a parcel boundary, a geocoded address workflow, or a user-drawn polygon.

    ```mermaid
    sequenceDiagram
        participant App as Customer app
        participant Parcel as Parcel boundary source
        participant API as Nearmap AI Feature API
        App->>Parcel: Resolve address or parcel ID
        Parcel-->>App: GeoJSON polygon
        App->>API: GET or POST /ai/features/v4/features.json
        API-->>App: Vector features and attributes
        App->>API: Optional /rollups.json
        API-->>App: Aggregated property facts
    ```

    ## Request pattern

    {% tabs %}
    {% tab title="Features" %}
    ```bash
    curl "https://api.nearmap.com/ai/features/v4/features.json?polygon=$POLYGON&apikey=$NEARMAP_API_KEY"
    ```
    {% endtab %}

    {% tab title="Rollups" %}
    ```bash
    curl "https://api.nearmap.com/ai/features/v4/rollups.json?polygon=$POLYGON&apikey=$NEARMAP_API_KEY"
    ```
    {% endtab %}
    {% endtabs %}

    ## Handling AOI intersections

    The public docs explain that feature polygons intersecting the query polygon are generally returned in full rather than truncated. Vegetation and Surfaces are the exception because potentially unbounded features are cropped to the query AOI.
    """,
)

print(f"Built {ROOT}")
