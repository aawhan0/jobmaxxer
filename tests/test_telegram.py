from src.jobmaxxer.telegram import TelegramConfig, send_message


def test_config_requires_both_environment_values(monkeypatch):
    monkeypatch.delenv("JOBMAXXER_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("JOBMAXXER_TELEGRAM_CHAT_ID", raising=False)
    assert TelegramConfig.from_env() is None


def test_send_message_posts_expected_payload(monkeypatch):
    calls = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"ok": True}

    def fake_post(url, **kwargs):
        calls["url"] = url
        calls["kwargs"] = kwargs
        return Response()

    monkeypatch.setattr("src.jobmaxxer.telegram.requests.post", fake_post)
    send_message("hello", TelegramConfig("token", "123"))
    assert calls["url"].endswith("/bottoken/sendMessage")
    assert calls["kwargs"]["json"] == {"chat_id": "123", "text": "hello"}


def test_empty_message_is_not_sent(monkeypatch):
    monkeypatch.setattr("src.jobmaxxer.telegram.requests.post", lambda *a, **k: (_ for _ in ()).throw(AssertionError()))
    send_message("   ", TelegramConfig("token", "123"))
