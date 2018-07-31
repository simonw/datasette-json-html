from datasette import hookimpl
import jinja2
import json


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
        if all(
            isinstance(item, dict)
            and set(item.keys()) == {"href", "label"}
            and is_sensible_href(item["href"])
            for item in data
        ):
            bits = [
                '<a href="{href}">{label}</a>'.format(
                    href=jinja2.escape(item["href"]),
                    label=jinja2.escape(item["label"] or "") or "&nbsp;",
                )
                for item in data
            ]
            return jinja2.Markup(", ".join(bits))
        else:
            return None
    keys = set(data.keys())
    if keys == {"href", "label"}:
        # Render {"href": "...", "label": "..."} as link
        href = data["href"]
        if not is_sensible_href(href):
            return None
        return jinja2.Markup(
            '<a href="{href}">{label}</a>'.format(
                href=jinja2.escape(data["href"]),
                label=jinja2.escape(data["label"] or "") or "&nbsp;",
            )
        )
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
