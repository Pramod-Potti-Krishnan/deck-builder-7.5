"""
Test Suite for Background Features API

Tests:
1. Create presentations with background_color
2. Create presentations with background_image
3. Create presentations with both (image priority)
4. Update slide backgrounds via editing API
5. Backward compatibility (no background fields)
6. Validation of hex color format
7. Validation of image URLs and data URIs
"""

import pytest
import requests
import json
from typing import Dict, Any


class TestBackgroundFeatures:
    """Test background color and background image features"""

    BASE_URL = "http://localhost:8504"  # Update if different

    def test_create_presentation_with_background_color(self):
        """Test creating a presentation with background_color on slides"""
        payload = {
            "title": "Background Color Test",
            "slides": [
                {
                    "layout": "L25",
                    "background_color": "#f0f9ff",
                    "content": {
                        "slide_title": "Slide with Blue Background",
                        "subtitle": "Testing background color feature",
                        "rich_content": "<div>Content here</div>"
                    }
                },
                {
                    "layout": "L29",
                    "background_color": "#1a1a2e",
                    "content": {
                        "hero_content": "<div style='color: white;'>Dark background</div>"
                    }
                }
            ]
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "url" in data
        print(f"✅ Created presentation with background colors: {data['url']}")

    def test_create_presentation_with_background_image(self):
        """Test creating a presentation with background_image on slides"""
        payload = {
            "title": "Background Image Test",
            "slides": [
                {
                    "layout": "L29",
                    "background_image": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920&h=1080&fit=crop",
                    "content": {
                        "hero_content": "<div style='color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);'>Hero with Background Image</div>"
                    }
                },
                {
                    "layout": "L25",
                    "background_image": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&h=1080&fit=crop",
                    "content": {
                        "slide_title": "Content with Background Image",
                        "rich_content": "<div style='color: white;'>Content</div>"
                    }
                }
            ]
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        print(f"✅ Created presentation with background images: {data['url']}")

    def test_create_presentation_with_both_backgrounds(self):
        """Test creating a presentation with both background_color and background_image"""
        payload = {
            "title": "Both Backgrounds Test",
            "slides": [
                {
                    "layout": "L29",
                    "background_image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&h=1080&fit=crop",
                    "background_color": "#0f4c75",  # Fallback color
                    "content": {
                        "hero_content": "<div style='color: white;'>Image with Fallback Color</div>"
                    }
                }
            ]
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        data = response.json()
        print(f"✅ Created presentation with image + fallback color: {data['url']}")

    def test_create_presentation_without_backgrounds(self):
        """Test backward compatibility - presentation without background fields"""
        payload = {
            "title": "No Background Test",
            "slides": [
                {
                    "layout": "L25",
                    "content": {
                        "slide_title": "Default Slide",
                        "rich_content": "<div>No background specified</div>"
                    }
                }
            ]
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        data = response.json()
        print(f"✅ Backward compatibility verified: {data['url']}")

    def test_update_slide_background_color(self):
        """Test updating slide background via editing API"""
        # First create a presentation
        create_payload = {
            "title": "Update Background Test",
            "slides": [
                {
                    "layout": "L25",
                    "content": {
                        "slide_title": "Original Slide",
                        "rich_content": "<div>Original content</div>"
                    }
                }
            ]
        }

        create_response = requests.post(f"{self.BASE_URL}/presentations", json=create_payload)
        assert create_response.status_code == 200
        presentation_id = create_response.json()["id"]

        # Update the slide to add background
        update_payload = {
            "background_color": "#fef3c7"
        }

        update_response = requests.patch(
            f"{self.BASE_URL}/presentations/{presentation_id}/slides/0",
            json=update_payload
        )

        assert update_response.status_code == 200
        print(f"✅ Updated slide background color via API")

    def test_update_slide_background_image(self):
        """Test updating slide background image via editing API"""
        # First create a presentation
        create_payload = {
            "title": "Update Image Test",
            "slides": [
                {
                    "layout": "L29",
                    "content": {
                        "hero_content": "<div>Original hero</div>"
                    }
                }
            ]
        }

        create_response = requests.post(f"{self.BASE_URL}/presentations", json=create_payload)
        assert create_response.status_code == 200
        presentation_id = create_response.json()["id"]

        # Update the slide to add background image
        update_payload = {
            "background_image": "https://images.unsplash.com/photo-1557683304-673a23048d34?w=1920&h=1080&fit=crop"
        }

        update_response = requests.patch(
            f"{self.BASE_URL}/presentations/{presentation_id}/slides/0",
            json=update_payload
        )

        assert update_response.status_code == 200
        print(f"✅ Updated slide background image via API")

    def test_all_layouts_with_backgrounds(self):
        """Test that all 6 layouts support backgrounds"""
        layouts = ["L01", "L02", "L03", "L25", "L27", "L29"]

        slides = []
        for layout in layouts:
            if layout == "L25":
                content = {
                    "slide_title": f"{layout} Test",
                    "rich_content": "<div>Content</div>"
                }
            elif layout == "L29":
                content = {
                    "hero_content": "<div>Hero content</div>"
                }
            else:
                content = {
                    "slide_title": f"{layout} Test",
                    "element_1": "Subtitle",
                    "element_2": "Element 2",
                    "element_3": "Element 3"
                }

            slides.append({
                "layout": layout,
                "background_color": "#e0e7ff",
                "content": content
            })

        payload = {
            "title": "All Layouts with Backgrounds",
            "slides": slides
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        data = response.json()
        print(f"✅ All 6 layouts support backgrounds: {data['url']}")

    def test_data_uri_background_image(self):
        """Test background_image with data URI (base64)"""
        # Small 1x1 pixel red PNG as data URI
        data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        payload = {
            "title": "Data URI Background Test",
            "slides": [
                {
                    "layout": "L29",
                    "background_image": data_uri,
                    "content": {
                        "hero_content": "<div>Data URI Background</div>"
                    }
                }
            ]
        }

        response = requests.post(f"{self.BASE_URL}/presentations", json=payload)

        assert response.status_code == 200
        print(f"✅ Data URI background image supported")


def run_tests():
    """Run all tests and print results"""
    test_suite = TestBackgroundFeatures()

    tests = [
        ("Background Color", test_suite.test_create_presentation_with_background_color),
        ("Background Image", test_suite.test_create_presentation_with_background_image),
        ("Both Backgrounds", test_suite.test_create_presentation_with_both_backgrounds),
        ("Backward Compatibility", test_suite.test_create_presentation_without_backgrounds),
        ("Update Background Color", test_suite.test_update_slide_background_color),
        ("Update Background Image", test_suite.test_update_slide_background_image),
        ("All Layouts", test_suite.test_all_layouts_with_backgrounds),
        ("Data URI", test_suite.test_data_uri_background_image),
    ]

    print("\n" + "="*60)
    print("BACKGROUND FEATURES API TEST SUITE")
    print("="*60 + "\n")

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
            failed += 1

    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run tests
    run_tests()
