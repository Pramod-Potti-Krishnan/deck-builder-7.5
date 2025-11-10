"""
Pytest configuration and fixtures for download endpoints testing.
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_presentation_data():
    """Sample presentation data for testing."""
    return {
        "title": "Test Presentation",
        "slides": [
            {
                "layout": "L29",
                "content": {
                    "hero_content": """
                        <div style="display: flex; flex-direction: column; justify-content: center;
                                    align-items: center; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                            <h1 style="color: white; font-size: 72px; margin: 0;">Test Presentation</h1>
                            <p style="color: white; font-size: 32px; margin-top: 20px;">Sample Hero Slide</p>
                        </div>
                    """
                }
            },
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Key Points",
                    "subtitle": "Overview of main topics",
                    "rich_content": """
                        <div style="padding: 20px;">
                            <ul style="font-size: 28px; line-height: 1.8;">
                                <li>First key point with important information</li>
                                <li>Second key point with critical details</li>
                                <li>Third key point with valuable insights</li>
                            </ul>
                        </div>
                    """
                }
            },
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Conclusion",
                    "subtitle": "Summary",
                    "rich_content": """
                        <div style="padding: 20px; text-align: center;">
                            <h2 style="font-size: 48px; color: #667eea;">Thank You</h2>
                            <p style="font-size: 24px; margin-top: 20px;">Questions?</p>
                        </div>
                    """
                }
            }
        ]
    }


@pytest.fixture
def base_url():
    """Base URL for the test server."""
    return "http://localhost:8504"


@pytest.fixture
def output_dir(tmp_path):
    """Temporary directory for test outputs."""
    output = tmp_path / "test_outputs"
    output.mkdir()
    return output
