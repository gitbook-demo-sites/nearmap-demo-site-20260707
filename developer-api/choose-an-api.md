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
