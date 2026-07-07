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
