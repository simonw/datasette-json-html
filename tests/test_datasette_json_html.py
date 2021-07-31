from datasette_json_html import render_cell
import markupsafe
import json
import pytest


@pytest.mark.parametrize(
    "input,expected",
    (
        # Ignore unrecognized JSON structure:
        ({"blah": "blah"}, None),
        # Ignore empty list
        ([], None),
        # Basic link:
        (
            {"href": "http://example.com/", "label": "Example"},
            '<a href="http://example.com/">Example</a>',
        ),
        # Evil links should not be rendered:
        ({"href": "javascript:alert('evil')", "label": "Evil"}, None),
        # Link with a tooltip:
        (
            {"href": "http://example.com/", "label": "Example", "title": "Tooltip"},
            '<a href="http://example.com/" title="Tooltip">Example</a>',
        ),
        # Image tests:
        (
            {"img_src": "https://placekitten.com/200/300"},
            '<img src="https://placekitten.com/200/300">',
        ),
        (
            {
                "img_src": "https://placekitten.com/200/300",
                "alt": "Kitten",
                "width": 200,
            },
            '<img src="https://placekitten.com/200/300" alt="Kitten" width="200">',
        ),
        (
            {
                "img_src": "https://placekitten.com/200/300",
                "href": "http://www.example.com",
            },
            '<a href="http://www.example.com"><img src="https://placekitten.com/200/300"></a>',
        ),
        (
            {"img_src": "https://placekitten.com/200/300", "caption": "Kitten caption"},
            '<figure><img src="https://placekitten.com/200/300">'
            "<figcaption>Kitten caption</figcaption></figure>",
        ),
        # List of links:
        (
            [
                {"href": "http://example.com/", "label": "Example"},
                {
                    "href": "http://blah.com/",
                    "label": "Blah",
                    "title": "Tooltip & change",
                },
            ],
            '<a href="http://example.com/">Example</a>, '
            '<a href="http://blah.com/" title="Tooltip &amp; change">Blah</a>',
        ),
        # Link with description
        (
            {
                "href": "http://example.com/",
                "label": "Example",
                "description": "Hello there\nwith a break",
            },
            '<strong><a href="http://example.com/">Example</a></strong><br>'
            "Hello there<br>with a break",
        ),
        # <pre> with string contents
        (
            {"pre": "Hello\n  two step indent\nBack again"},
            "<pre>Hello\n  two step indent\nBack again</pre>",
        ),
        # <pre> with JSON object contents
        (
            {"pre": {"this": {"is": "nested"}}},
            "<pre>{\n  &#34;this&#34;: {\n    &#34;is&#34;: &#34;nested&#34;\n  }\n}</pre>",
        ),
    ),
)
def test_render_cell(input, expected):
    actual = render_cell(json.dumps(input))
    assert expected == actual
    assert actual is None or isinstance(actual, markupsafe.Markup)
