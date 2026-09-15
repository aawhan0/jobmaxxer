from src.jobmaxxer.providers import parse_remoteok_payload


def test_parse_remoteok_payload_uses_position_and_url():
    jobs = parse_remoteok_payload(
        "Remote OK",
        [
            {
                "position": "AI Engineer",
                "location": "Remote",
                "url": "https://remoteok.com/remote-jobs/ai-engineer-123",
                "id": "123",
            },
            {"company": "metadata"},
        ],
    )

    assert len(jobs) == 1
    assert jobs[0].title == "AI Engineer"
    assert jobs[0].location == "Remote"
    assert jobs[0].source == "remoteok"
    assert jobs[0].url == "https://remoteok.com/remote-jobs/ai-engineer-123"


def test_parse_remoteok_payload_preserves_description_fields():
    jobs = parse_remoteok_payload(
        "Remote OK",
        [
            {
                "position": "Backend Engineer",
                "description": "Build Python services.",
                "apply_url": "https://example.com/apply",
            }
        ],
    )

    assert jobs[0].description == "Build Python services."
    assert jobs[0].url == "https://example.com/apply"
