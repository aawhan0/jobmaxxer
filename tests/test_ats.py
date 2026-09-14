from jobmaxxer.ats import detect_ats, normalize_job_url


def test_detect_common_ats_hosts():
    assert detect_ats('https://boards.greenhouse.io/acme') == 'greenhouse'
    assert detect_ats('https://jobs.lever.co/acme') == 'lever'
    assert detect_ats('https://jobs.ashbyhq.com/acme') == 'ashby'
    assert detect_ats('https://acme.myworkdayjobs.com/en-US/jobs') == 'workday'


def test_unknown_urls_use_html_fallback():
    assert detect_ats('https://example.com/careers') == 'html'


def test_normalize_job_url_removes_fragment_and_trailing_slash():
    assert normalize_job_url('https://example.com/job/123/#apply') == 'https://example.com/job/123'
