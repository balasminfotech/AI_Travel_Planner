from pathlib import Path


def test_master_agent_logs_exception_details():

    source = Path(
        "agents/master_travel_agent.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "error_type=%s | message=%s"
        in source
    )

    assert "str(exc)[:500]" in source


def test_app_uses_new_streamlit_width_api():

    source = Path(
        "app.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "use_container_width=True"
        not in source
    )

    assert (
        "use_container_width=False"
        not in source
    )
