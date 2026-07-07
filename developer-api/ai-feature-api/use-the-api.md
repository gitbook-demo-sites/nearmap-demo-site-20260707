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
