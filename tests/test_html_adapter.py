from src.jobmaxxer.html_adapter import _Links


def test_html_link_parser_collects_job_links():
    parser = _Links()
    parser.feed('<a href="/jobs/1">AI Engineer</a><a href="/about">About</a>')
    assert parser.links == [("AI Engineer", "/jobs/1"), ("About", "/about")]
