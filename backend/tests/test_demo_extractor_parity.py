from pathlib import Path


def test_demo_and_backend_claim_extractors_are_identical():
    """The Space is standalone, so it carries a mirror; CI prevents silent drift."""
    repo = Path(__file__).resolve().parents[2]
    backend = repo / "backend/app/services/claim_extractor.py"
    demo = repo / "demo/claim_extractor.py"

    assert backend.read_text(encoding="utf-8") == demo.read_text(encoding="utf-8"), (
        "demo/claim_extractor.py diverged from the backend canonical extractor. "
        "Copy backend/app/services/claim_extractor.py to demo/claim_extractor.py."
    )



def test_demo_and_backend_decision_policies_are_identical():
    """The frozen operating point must not drift between backend and Space."""
    repo = Path(__file__).resolve().parents[2]
    backend = repo / "backend/app/services/decision_policy.py"
    demo = repo / "demo/decision_policy.py"

    assert backend.read_text(encoding="utf-8") == demo.read_text(encoding="utf-8"), (
        "demo/decision_policy.py diverged from the backend policy. "
        "Copy backend/app/services/decision_policy.py to demo/decision_policy.py."
    )
