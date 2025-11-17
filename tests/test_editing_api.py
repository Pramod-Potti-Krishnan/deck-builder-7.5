"""
Test script for content editing API endpoints

Tests:
1. Create a presentation
2. Update presentation metadata
3. Update slide content
4. Get version history
5. Restore a version
"""

import requests
import json
import time

# API base URL (adjust port if needed)
BASE_URL = "http://localhost:8504/api"

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_create_presentation():
    """Test: Create a sample presentation"""
    print_section("TEST 1: Create Presentation")

    presentation_data = {
        "title": "Content Editing Test Presentation",
        "slides": [
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Original Title",
                    "subtitle": "Original Subtitle",
                    "rich_content": "<div>Original Content</div>",
                    "presentation_name": "Test Presentation"
                }
            },
            {
                "layout": "L29",
                "content": {
                    "hero_content": "<div style='background: #3b82f6; color: white; padding: 40px;'>Original Hero Slide</div>"
                }
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/presentations", json=presentation_data)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Presentation created successfully")
        print(f"   ID: {data['id']}")
        print(f"   URL: {data['url']}")
        return data['id']
    else:
        print(f"❌ Failed to create presentation: {response.status_code}")
        print(f"   {response.text}")
        return None

def test_update_metadata(presentation_id):
    """Test: Update presentation title"""
    print_section("TEST 2: Update Presentation Metadata")

    update_data = {
        "title": "UPDATED: Content Editing Test"
    }

    response = requests.put(
        f"{BASE_URL}/presentations/{presentation_id}?created_by=test_user&change_summary=Updated title",
        json=update_data
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Metadata updated successfully")
        print(f"   New title: {data['presentation']['title']}")
        print(f"   Updated at: {data['presentation'].get('updated_at', 'N/A')}")
        return True
    else:
        print(f"❌ Failed to update metadata: {response.status_code}")
        print(f"   {response.text}")
        return False

def test_update_slide(presentation_id, slide_index=0):
    """Test: Update slide content"""
    print_section(f"TEST 3: Update Slide {slide_index + 1} Content")

    update_data = {
        "slide_title": "EDITED Title",
        "subtitle": "EDITED Subtitle",
        "rich_content": "<div style='color: red;'><h2>EDITED Content</h2><p>This content was updated via API!</p></div>"
    }

    response = requests.put(
        f"{BASE_URL}/presentations/{presentation_id}/slides/{slide_index}?created_by=test_user&change_summary=Updated slide 1 content",
        json=update_data
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Slide content updated successfully")
        print(f"   Slide title: {data['slide']['content'].get('slide_title', 'N/A')}")
        print(f"   Subtitle: {data['slide']['content'].get('subtitle', 'N/A')}")
        return True
    else:
        print(f"❌ Failed to update slide: {response.status_code}")
        print(f"   {response.text}")
        return False

def test_get_version_history(presentation_id):
    """Test: Get version history"""
    print_section("TEST 4: Get Version History")

    response = requests.get(f"{BASE_URL}/presentations/{presentation_id}/versions")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Version history retrieved successfully")
        print(f"   Presentation ID: {data['presentation_id']}")
        print(f"   Current version: {data['current_version_id']}")
        print(f"   Total versions: {len(data['versions'])}")

        if data['versions']:
            print(f"\n   Version History:")
            for i, version in enumerate(data['versions'], 1):
                print(f"   {i}. Version: {version['version_id']}")
                print(f"      Created: {version['created_at']}")
                print(f"      By: {version['created_by']}")
                print(f"      Summary: {version.get('change_summary', 'N/A')}")
                print()

        return data.get('versions', [])
    else:
        print(f"❌ Failed to get version history: {response.status_code}")
        print(f"   {response.text}")
        return []

def test_restore_version(presentation_id, version_id):
    """Test: Restore a specific version"""
    print_section(f"TEST 5: Restore Version {version_id}")

    restore_data = {
        "create_backup": True
    }

    response = requests.post(
        f"{BASE_URL}/presentations/{presentation_id}/restore/{version_id}",
        json=restore_data
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Version restored successfully")
        print(f"   Restored from: {data['presentation'].get('restored_from', 'N/A')}")
        print(f"   Updated at: {data['presentation'].get('updated_at', 'N/A')}")
        return True
    else:
        print(f"❌ Failed to restore version: {response.status_code}")
        print(f"   {response.text}")
        return False

def test_view_presentation(presentation_id):
    """Test: Get final presentation data"""
    print_section("FINAL: View Presentation Data")

    response = requests.get(f"{BASE_URL}/presentations/{presentation_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Presentation data retrieved")
        print(f"   Title: {data['title']}")
        print(f"   Slides: {len(data['slides'])}")
        print(f"   Slide 1 Title: {data['slides'][0]['content'].get('slide_title', 'N/A')}")
        return data
    else:
        print(f"❌ Failed to get presentation: {response.status_code}")
        return None

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("  CONTENT EDITING API TEST SUITE")
    print("="*60)

    # Test 1: Create presentation
    presentation_id = test_create_presentation()
    if not presentation_id:
        print("\n❌ Test suite aborted: Could not create presentation")
        return

    time.sleep(0.5)

    # Test 2: Update metadata
    test_update_metadata(presentation_id)
    time.sleep(0.5)

    # Test 3: Update slide content
    test_update_slide(presentation_id, slide_index=0)
    time.sleep(0.5)

    # Test 4: Get version history
    versions = test_get_version_history(presentation_id)
    time.sleep(0.5)

    # Test 5: Restore version (if versions exist)
    if versions:
        # Restore the first version (original state)
        first_version = versions[0]['version_id']
        test_restore_version(presentation_id, first_version)
        time.sleep(0.5)

    # Final: View presentation
    test_view_presentation(presentation_id)

    # Summary
    print_section("TEST SUMMARY")
    print(f"✅ All tests completed!")
    print(f"   Presentation ID: {presentation_id}")
    print(f"   View at: http://localhost:8504/p/{presentation_id}")
    print(f"   API Docs: http://localhost:8504/docs")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("   Make sure the server is running: python3 server.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
