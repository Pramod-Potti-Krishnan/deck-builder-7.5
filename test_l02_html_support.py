"""
Test L02 HTML Support - v7.5.1
Tests that L02 layout properly renders HTML in element_2 and element_3
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8504"


def test_l02_with_html():
    """Test L02 with HTML content in both element_2 and element_3."""
    print("\n" + "=" * 70)
    print("TEST: L02 with HTML Content (Analytics Format)")
    print("=" * 70)

    # Create presentation with L02 layout and HTML content
    presentation_data = {
        "title": "L02 HTML Support Test - v7.5.1",
        "slides": [{
            "layout": "L02",
            "content": {
                "slide_title": "Quarterly Revenue Growth",
                "element_1": "FY 2024 Performance Analytics",
                "element_3": """<div class='l02-chart-container' style='width: 1260px; height: 720px; background: #ffffff; display: flex; align-items: center; justify-content: center; border: 2px solid #e5e7eb; border-radius: 8px;'>
    <div style='text-align: center; color: #6b7280;'>
        <div style='font-size: 48px; margin-bottom: 16px;'>📊</div>
        <div style='font-size: 24px; font-weight: bold; color: #1f2937;'>Chart Placeholder</div>
        <div style='font-size: 16px; margin-top: 8px;'>(Chart.js would render here)</div>
    </div>
</div>""",
                "element_2": """<div style='padding: 32px; background: #f8f9fa; border-radius: 8px; height: 100%; box-sizing: border-box;'>
    <h3 style='font-size: 20px; font-weight: 600; margin: 0 0 16px 0; color: #1f2937;'>Key Insights</h3>
    <p style='font-size: 16px; line-height: 1.6; color: #374151; margin: 0 0 12px 0;'>
        The line chart illustrates quarterly revenue growth, with figures increasing from $125,000 in Q1 to $195,000 in Q4, representing a 56% year-over-year growth.
    </p>
    <p style='font-size: 16px; line-height: 1.6; color: #374151; margin: 0;'>
        This upward trend indicates robust business performance throughout 2024 and suggests continued market demand for our products.
    </p>
</div>""",
                "presentation_name": "Analytics Test",
                "company_logo": "🏢"
            }
        }]
    }

    # Create presentation
    response = requests.post(
        f"{BASE_URL}/api/presentations",
        json=presentation_data,
        timeout=10
    )

    if response.status_code not in [200, 201]:
        print(f"❌ Failed to create presentation: {response.status_code}")
        print(response.text[:500])
        return None

    result = response.json()
    pres_id = result.get("id") or result.get("presentation_id")

    print(f"\n✅ Presentation created: {pres_id}")

    # Verify saved content
    verify_response = requests.get(f"{BASE_URL}/api/presentations/{pres_id}")
    if verify_response.status_code == 200:
        saved_data = verify_response.json()
        saved_slide = saved_data["slides"][0]

        print(f"\n📋 Saved Presentation Data:")
        print(f"   Layout: {saved_slide.get('layout')}")
        print(f"   element_3 length: {len(saved_slide['content']['element_3'])} chars")
        print(f"   element_2 length: {len(saved_slide['content']['element_2'])} chars")

        # Check if HTML was preserved
        has_html_in_element2 = '<' in saved_slide['content']['element_2']
        has_html_in_element3 = '<' in saved_slide['content']['element_3']

        print(f"\n✅ HTML Preservation Check:")
        print(f"   element_3 contains HTML: {has_html_in_element3}")
        print(f"   element_2 contains HTML: {has_html_in_element2}")

    # Output URLs
    viewer_url = f"{BASE_URL}/p/{pres_id}"
    builder_url = f"{BASE_URL}/static/builder.html?id={pres_id}"

    print(f"\n" + "=" * 70)
    print(f"🎉 TEST COMPLETE")
    print(f"=" * 70)
    print(f"\n🔗 Viewer URL (for testing):")
    print(f"   {viewer_url}")
    print(f"\n🔗 Builder URL:")
    print(f"   {builder_url}")
    print(f"\n📝 Expected Result:")
    print(f"   - Chart placeholder visible on left (1260px wide)")
    print(f"   - Observations panel visible on right (540px wide)")
    print(f"   - NO BLANK SCREEN")
    print(f"   - HTML content properly rendered")

    return pres_id


def test_l02_with_plain_text():
    """Test L02 with plain text (backward compatibility)."""
    print("\n" + "=" * 70)
    print("TEST: L02 with Plain Text (Backward Compatibility)")
    print("=" * 70)

    presentation_data = {
        "title": "L02 Plain Text Test - v7.5.1",
        "slides": [{
            "layout": "L02",
            "content": {
                "slide_title": "System Architecture",
                "element_1": "Cloud Infrastructure Overview",
                "element_3": "<div style='width: 1260px; height: 720px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; border: 2px solid #e5e7eb; border-radius: 8px;'><div style='text-align: center; color: #6b7280; font-size: 24px;'>📐 Diagram Placeholder</div></div>",
                "element_2": "The architecture utilizes a microservices approach with API Gateway, Service Mesh, and distributed databases. Each service is independently deployable and scalable, ensuring system resilience and flexibility. This design supports horizontal scaling and fault tolerance.",
                "presentation_name": "Technical Docs",
                "company_logo": "⚙️"
            }
        }]
    }

    response = requests.post(
        f"{BASE_URL}/api/presentations",
        json=presentation_data,
        timeout=10
    )

    if response.status_code not in [200, 201]:
        print(f"❌ Failed to create presentation: {response.status_code}")
        return None

    result = response.json()
    pres_id = result.get("id") or result.get("presentation_id")

    print(f"\n✅ Presentation created: {pres_id}")

    viewer_url = f"{BASE_URL}/p/{pres_id}"

    print(f"\n🔗 Viewer URL:")
    print(f"   {viewer_url}")
    print(f"\n📝 Expected Result:")
    print(f"   - Diagram placeholder on left")
    print(f"   - Plain text on right with default styling")
    print(f"   - Text should be readable and properly formatted")

    return pres_id


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("L02 HTML SUPPORT TESTS - v7.5.1")
    print("=" * 70)

    try:
        # Test 1: HTML content (Analytics format)
        html_test_id = test_l02_with_html()

        # Test 2: Plain text (backward compatibility)
        text_test_id = test_l02_with_plain_text()

        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED")
        print("=" * 70)
        print("\nResults:")
        if html_test_id:
            print(f"✅ HTML Test: http://localhost:8504/p/{html_test_id}")
        if text_test_id:
            print(f"✅ Plain Text Test: http://localhost:8504/p/{text_test_id}")

        print("\nManual Verification:")
        print("  1. Open both URLs in browser")
        print("  2. Verify HTML test shows formatted observations panel")
        print("  3. Verify plain text test shows styled text")
        print("  4. Confirm NO blank screens")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Layout Builder server")
        print("   Make sure server is running on port 8504")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
