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
curl "https://api.nearmap.com/ai/features/v4/classes.json" \
  -H "Authorization: Apikey $NEARMAP_API_KEY"
```
{% endtab %}
{% endtabs %}
