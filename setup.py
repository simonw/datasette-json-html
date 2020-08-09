from setuptools import setup
import os

VERSION = "0.6.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-json-html",
    description="Datasette plugin for rendering HTML based on JSON values",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-json-html",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-json-html/issues",
        "CI": "https://github.com/simonw/datasette-json-html/actions",
        "Changelog": "https://github.com/simonw/datasette-json-html/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_json_html"],
    entry_points={"datasette": ["json_html = datasette_json_html"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx"]},
    tests_require=["datasette-json-html[test]"],
)
