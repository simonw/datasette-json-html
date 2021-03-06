from datasette import hookimpl
import jinja2
import json
import urllib

valid_link_keys = (
    {"href", "label"},
    {"href", "label", "title"},
    {"href", "label", "title", "description"},
    {"href", "label", "description"},
)
valid_link_keys_no_description = ({"href", "label"}, {"href", "label", "title"})

# Add urllib_quote_plus SQLite function`
@hookimpl
def prepare_connection(conn):
    conn.create_function("urllib_quote_plus", 1, urllib.parse.quote_plus)


@hookimpl
def render_cell(value):
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not (
        (stripped.startswith("{") and stripped.endswith("}"))
        or (stripped.startswith("[") and stripped.endswith("]"))
    ):
        return None
    try:
        data = json.loads(value)
    except ValueError:
        return None
    if isinstance(data, list):
        # Handle list-of-links
        if len(data) == 0:
            return None
        if all(
            isinstance(item, dict)
            and set(item.keys()) in valid_link_keys_no_description
            and is_sensible_href(item["href"])
            for item in data
        ):
            bits = [build_link(item) for item in data]
            return jinja2.Markup(", ".join(bits))
        else:
            return None
    keys = set(data.keys())
    if keys in valid_link_keys:
        # Render {"href": "...", "label": "..."} as link
        href = data["href"]
        if not is_sensible_href(href):
            return None
        return jinja2.Markup(build_link(data))
    elif keys == {"pre"}:
        value = data["pre"]
        if isinstance(value, str):
            pre = value
        else:
            pre = json.dumps(value, indent=2)
        return jinja2.Markup("<pre>{pre}</pre>".format(pre=jinja2.escape(pre)))
    elif "img_src" in keys and keys.issubset(
        {"img_src", "alt", "href", "caption", "width"}
    ):
        # Render <img src="">, optionally with alt, wrapping link and/or caption
        html = '<img src="{img_src}"{optional_alt}{optional_width}>'.format(
            img_src=jinja2.escape(data["img_src"]),
            optional_alt=' alt="{}"'.format(jinja2.escape(data["alt"]))
            if data.get("alt")
            else "",
            optional_width=' width="{}"'.format(jinja2.escape(data["width"]))
            if data.get("width")
            else "",
        )
        if data.get("href") and is_sensible_href(data["href"]):
            html = '<a href="{href}">{html}</a>'.format(
                href=jinja2.escape(data["href"]), html=html
            )
        if data.get("caption"):
            html = "<figure>{html}<figcaption>{caption}</figcaption></figure>".format(
                caption=jinja2.escape(data["caption"]), html=html
            )
        return jinja2.Markup(html)


def is_sensible_href(href):
    return (
        href.startswith("/")
        or href.startswith("http://")
        or href.startswith("https://")
    )


def build_link(item):
    html = '<a href="{href}"{title}>{label}</a>'.format(
        href=jinja2.escape(item["href"]),
        label=jinja2.escape(item["label"] or "") or "&nbsp;",
        title=' title="{}"'.format(jinja2.escape(item["title"]))
        if item.get("title")
        else "",
    )
    if item.get("description"):
        description = (
            jinja2.escape(item["description"])
            .replace("\r\n", "\n")
            .replace("\n", jinja2.Markup("<br>"))
        )
        html = "<strong>{}</strong><br>{}".format(html, description)
    return html
