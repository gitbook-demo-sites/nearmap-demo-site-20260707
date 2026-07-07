import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://api.gitbook.com/v1"
ORG_ID = "CnKiKmimJyVAnHLQcyf1"
REPO = "nearmap-demo-site-20260707"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"
OPENAPI_SLUG = "nearmap-ai-feature-api-demo"
OPENAPI_FILE = ROOT / "openapi/nearmap-ai-feature-api.yaml"

SPACES = [
    {
        "key": "HOME",
        "sentinel": "XSPACE_HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "Demo framing, source notes, and review checklist.",
    },
    {
        "key": "PRODUCT",
        "sentinel": "XSPACE_PRODUCT",
        "folder": "product-docs",
        "title": "Product Documentation",
        "emoji": "1f5fa",
        "icon": "map-location-dot",
        "path": "product-documentation",
        "description": "Representative help-center content for MapBrowser, Roof Assessment, Betterview, admin, and support.",
    },
    {
        "key": "API",
        "sentinel": "XSPACE_API",
        "folder": "developer-api",
        "title": "Developer & API",
        "emoji": "1f4bb",
        "icon": "code",
        "path": "developer-api",
        "description": "API chooser, authentication, standards, AI Feature API guide, and generated reference pages.",
    },
]


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def git_commit_push(message: str):
    subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def replace_sentinels(space_ids: dict[str, str]):
    replacements = {item["sentinel"]: space_ids[item["key"]] for item in SPACES}
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")


def ensure_openapi_spec(org_id: str) -> dict:
    source_text = OPENAPI_FILE.read_text(encoding="utf-8")
    payload = {"slug": OPENAPI_SLUG, "source": {"text": source_text}}
    try:
        _, spec = api("POST", f"/orgs/{org_id}/openapi", payload)
        return {"created": True, "slug": OPENAPI_SLUG, "spec": spec}
    except RuntimeError as exc:
        if "400" not in str(exc) and "409" not in str(exc):
            raise
        _, specs = api("GET", f"/orgs/{org_id}/openapi")
        items = specs.get("items") or specs.get("results") or (specs if isinstance(specs, list) else [])
        for item in items:
            if item.get("slug") == OPENAPI_SLUG:
                return {"created": False, "slug": OPENAPI_SLUG, "spec": item, "note": "slug already existed"}
        return {"created": False, "slug": OPENAPI_SLUG, "error": str(exc)}


def create_site(org_id: str, openapi_result: dict) -> dict:
    _, site = api(
        "POST",
        f"/orgs/{org_id}/sites",
        {"type": "ultimate", "title": "Nearmap Documentation Hub", "visibility": "share-link"},
    )
    site_id = site["id"]
    api(
        "PATCH",
        f"/orgs/{org_id}/sites/{site_id}",
        {"title": "Nearmap Documentation Hub", "visibility": "share-link", "basename": "nearmap-documentation-hub"},
    )

    created = {"org": org_id, "site": site_id, "spaces": {}, "sections": {}, "site_spaces": {}, "site_object": site, "openapi": openapi_result}
    for item in SPACES:
        _, space = api(
            "POST",
            f"/orgs/{org_id}/spaces",
            {"title": item["title"], "emoji": item["emoji"], "empty": True, "editMode": "live"},
        )
        space_id = space["id"]
        created["spaces"][item["key"]] = space_id
        _, section = api(
            "POST",
            f"/orgs/{org_id}/sites/{site_id}/sections",
            {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
        )
        section_id = section["id"]
        site_space_id = section["siteSpaces"][0]["id"]
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id
        api(
            "PATCH",
            f"/orgs/{org_id}/sites/{site_id}/sections/{section_id}",
            {"path": item["path"], "description": item["description"], "draft": False, "defaultSiteSpace": site_space_id},
        )

    api(
        "PATCH",
        f"/orgs/{org_id}/sites/{site_id}",
        {"defaultSiteSection": created["sections"]["HOME"], "defaultSiteSpace": created["site_spaces"]["HOME"]},
    )
    return created


def import_spaces(created: dict):
    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    (ROOT / "gitbook-import-results.json").write_text(json.dumps(imports, indent=2) + "\n", encoding="utf-8")


def apply_customization(org_id: str, site_id: str, created: dict):
    logo = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/nearmap-wordmark.svg"
    cover = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/nearmap-cover.svg"
    favicon = "https://files.readme.io/22933f1-small-Blue.png"
    customization = {
        "title": "Nearmap Documentation Hub",
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#3448FF", "dark": "#7B8CFF"},
            "infoColor": {"light": "#3448FF", "dark": "#7B8CFF"},
            "successColor": {"light": "#0B8F6A", "dark": "#48D6A5"},
            "warningColor": {"light": "#F59E0B", "dark": "#FBBF24"},
            "dangerColor": {"light": "#D92D20", "dark": "#F97066"},
            "tint": {"color": {"light": "#F7F9FC", "dark": "#08112E"}},
            "corners": "rounded",
            "depth": "flat",
            "links": "accent",
            "font": "Inter",
            "monospaceFont": "IBMPlexMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {"icon": {"light": favicon, "dark": favicon}},
        "header": {
            "preset": "default",
            "logo": {"light": logo, "dark": logo},
            "links": [
                {"title": "Product docs", "to": {"kind": "space", "space": created["spaces"]["PRODUCT"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Developer & API", "to": {"kind": "space", "space": created["spaces"]["API"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Nearmap", "to": {"kind": "url", "url": "https://www.nearmap.com/"}, "style": "button-secondary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo, "dark": logo},
            "groups": [
                {
                    "title": "Demo sections",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "localizedTitle": {}},
                        {"title": "Product Documentation", "to": {"kind": "space", "space": created["spaces"]["PRODUCT"]}, "localizedTitle": {}},
                        {"title": "Developer & API", "to": {"kind": "space", "space": created["spaces"]["API"]}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                        {"title": "Nearmap", "to": {"kind": "url", "url": "https://www.nearmap.com/"}, "localizedTitle": {}},
                        {"title": "Help Center", "to": {"kind": "url", "url": "https://help.nearmap.com/"}, "localizedTitle": {}},
                        {"title": "API Hub", "to": {"kind": "url", "url": "https://developer.nearmap.com/"}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Nearmap Documentation Hub demo - built for review in GitBook.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "How do I get started with MapBrowser?",
                "Which Nearmap API should I use?",
                "How does API key authentication work?",
                "What does the AI Feature API return?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "self"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://www.nearmap.com/privacy-policy"},
        "socialPreview": {"url": cover},
        "socialAccounts": [{"platform": "linkedin", "handle": "company/nearmap-com", "display": {"footer": True, "header": False}}],
        "insights": {"trackingCookie": True},
    }
    _, customized = api("PUT", f"/orgs/{org_id}/sites/{site_id}/customization", customization)
    (ROOT / "gitbook-customization-result.json").write_text(json.dumps(customized, indent=2) + "\n", encoding="utf-8")


def main():
    org_id = sys.argv[1] if len(sys.argv) > 1 else ORG_ID
    openapi_result = ensure_openapi_spec(org_id)
    created_path = ROOT / "gitbook-created.json"
    if created_path.exists():
        created = json.loads(created_path.read_text(encoding="utf-8"))
        site_id = created["site"]
    else:
        created = create_site(org_id, openapi_result)
        site_id = created["site"]
        replace_sentinels(created["spaces"])
        created_path.write_text(json.dumps(created, indent=2) + "\n", encoding="utf-8")
        git_commit_push("Resolve Nearmap GitBook space links")

    import_spaces(created)
    apply_customization(org_id, site_id, created)

    publish_status, publish = api("POST", f"/orgs/{org_id}/sites/{site_id}/publish")
    share_status, share = api("POST", f"/orgs/{org_id}/sites/{site_id}/share-links", {"name": "Nearmap demo review"})
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "share_status": share_status,
        "share": share,
        "published_url": share["urls"]["published"],
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
        "openapi": openapi_result,
    }
    (ROOT / "gitbook-publish-share.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Add Nearmap GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
