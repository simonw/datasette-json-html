from datasette_json_html import prepare_connection
import sqlite3


def test_urllib_quote_plus():
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    result = conn.execute(
        """
        select urllib_quote_plus("/foo/bar?baz=bam")
    """
    ).fetchone()[0]
    assert "%2Ffoo%2Fbar%3Fbaz%3Dbam" == result
