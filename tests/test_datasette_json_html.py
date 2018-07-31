from datasette_json_html import render_cell
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
    ),
)
def test_render_cell(input, expected):
    assert expected == render_cell(json.dumps(input))
