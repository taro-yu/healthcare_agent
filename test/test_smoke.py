import os
import pytest

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_import():
    from health_agent.core.agent import HealthAgent
    agent = HealthAgent()
    assert agent is not None