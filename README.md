# datasette-json-html

[![PyPI](https://img.shields.io/pypi/v/datasette-json-html.svg)](https://pypi.org/project/datasette-json-html/)
[![Travis CI](https://travis-ci.com/simonw/datasette-json-html.svg?branch=master)](https://travis-ci.com/simonw/datasette-json-html)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-json-html/blob/master/LICENSE)

Datasette plugin for rendering HTML based on JSON values, using the [render_cell plugin hook](https://datasette.readthedocs.io/en/latest/plugins.html#plugin-hook-render-cell).

This plugin looks for cell values that match a very specific JSON format and converts them into HTML when they are rendered by the Datasette interface.

See [russian-ira-facebook-ads-datasette](https://github.com/simonw/russian-ira-facebook-ads-datasette) for an example of this plugin in action.

## Links

    {
        "href": "https://simonwillison.net/",
        "label": "Simon Willison"
    }

Will be rendered as an `<a href="">` link:

    <a href="https://simonwillison.net/">Simon Willison</a>

## List of links

    [
        {
            "href": "https://simonwillison.net/",
            "label": "Simon Willison"
        },
        {
            "href": "https://github.com/simonw/datasette",
            "label": "Datasette"
        }
    ]

Will be rendered as a comma-separated list of `<a href="">` links:

    <a href="https://simonwillison.net/">Simon Willison</a>,
    <a href="https://github.com/simonw/datasette">Datasette</a>

The `href` property must begin with `https://` or `http://` or `/`, to avoid potential XSS injection attacks (for example URLs that begin with `javascript:`).

## Images

The image tag is more complex. The most basic version looks like this:

    {
        "img_src": "https://placekitten.com/200/300"
    }

This will render as:

    <img src="https://placekitten.com/200/300">

But you can also include one or more of `alt`, `caption`, `width` and `href`.

If you include width or alt, they will be added as attributes:

    {
        "img_src": "https://placekitten.com/200/300",
        "alt": "Kitten",
        "width": 200
    }

Produces:

    <img src="https://placekitten.com/200/300"
        alt="Kitten" width="200">

The `href` key will cause the image to be wrapped in a link:

    {
        "img_src": "https://placekitten.com/200/300",
        "href": "http://www.example.com"
    }

Produces:

    <a href="http://www.example.com">
        <img src="https://placekitten.com/200/300">
    </a>

The `caption` key wraps everything in a fancy figure/figcaption block:

    {
        "img_src": "https://placekitten.com/200/300",
        "caption": "Kitten caption"
    }

Produces:

    <figure>
        <img src="https://placekitten.com/200/300"></a>
        <figcaption>Kitten caption</figcaption>
    </figure>

## Preformatted text

You can use `{"pre": "text"}` to render text in a `<pre>` HTML tag:

    {
        "pre": "This\nhas\nnewlines"
    }

Produces:

    <pre>This
    has
    newlines</pre>

If the value attached to the `"pre"` key is itself a JSON object, that JSON will be pretty-printed:

    {
        "pre": {
            "this": {
                "object": ["is", "nested"]
            }
        }
    }

Produces:

    <pre>{
      &#34;this&#34;: {
        &#34;object&#34;: [
          &#34;is&#34;,
          &#34;nested&#34;
        ]
      }
    }</pre>

## Using these with SQLite JSON functions

The most powerful way to make use of this plugin is in conjunction with SQLite's [JSON functions](https://www.sqlite.org/json1.html). For example:

    select json_object(
        "href", "https://simonwillison.net/",
        "label", "Simon Willison"
    );

You can use these functions to construct JSON objects that work with the plugin from data in a table:

    select id, json_object(
        "href", url, "label", text
    ) from mytable;

## The `urllib_quote_plus()` SQL function

Since this plugin is designed to be used with SQL that constructs the underlying JSON structure, it is likely you will need to construct dynamic URLs from results returned by a SQL query.

This plugin registers a custom SQLite function called `urllib_quote_plus()` to help you do that. It lets you use Python's [urllib.parse.quote\_plus() function](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus) from within a SQL query.

Here's an example of how you might use it:

    select id, json_object(
        "href",
        "/mydatabase/other_table?_search=" || urllib_quote_plus(text),
        "label", text
    ) from mytable;
