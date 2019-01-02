from datasette_json_html import render_cell
import jinja2
import json
import pytest


@pytest.mark.parametrize(
    "input,expected",
    (
        # Ignore unrecognized JSON structure:
        ({"blah": "blah"}, None),
        # Basic link:
        (
            {"href": "http://example.com/", "label": "Example"},
            '<a href="http://example.com/">Example</a>',
        ),
        # Evil links should not be rendered:
        ({"href": "javascript:alert('evil')", "label": "Evil"}, None),
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
                {"href": "http://blah.com/", "label": "Blah"},
            ],
            '<a href="http://example.com/">Example</a>, '
            '<a href="http://blah.com/">Blah</a>',
        ),
        # <pre> with string contents
        (
            {"pre": "Hello\n  two step indent\nBack again"},
            '<pre>Hello\n  two step indent\nBack again</pre>'
        ),
        # <pre> with JSON object contents
        (
            {"pre": {"this": {"is": "nested"}}},
            '<pre>{\n  &#34;this&#34;: {\n    &#34;is&#34;: &#34;nested&#34;\n  }\n}</pre>'
        ),
    ),
)
def test_render_cell(input, expected):
    actual = render_cell(json.dumps(input))
    assert expected == actual
    assert actual is None or isinstance(actual, jinja2.Markup)
