#!/usr/bin/env python3
"""
Manual test script for PDF and PPTX download endpoints.

This script creates a test presentation, downloads it as both PDF and PPTX,
and validates the outputs.

Usage:
    python3 test_downloads_manual.py

Requirements:
    - Server must be running on http://localhost:8504 (or set SERVER_URL env var)
    - requests library: pip install requests
"""

import requests
import time
import os
import sys
from pathlib import Path


# Configuration
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8504")
OUTPUT_DIR = Path("test_output")


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")


def create_test_presentation():
    """Create a test presentation and return its ID."""
    print_header("Step 1: Creating Test Presentation")

    presentation_data = {
        "title": "Download Test Presentation",
        "slides": [
            {
                "layout": "L29",
                "content": {
                    "hero_content": """
                        <div style="display: flex; flex-direction: column; justify-content: center;
                                    align-items: center; height: 100%;
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                            <h1 style="color: white; font-size: 72px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                                Download Test
                            </h1>
                            <p style="color: white; font-size: 32px; margin-top: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                                PDF & PPTX Export Validation
                            </p>
                        </div>
                    """
                }
            },
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Key Features",
                    "subtitle": "Testing download functionality",
                    "rich_content": """
                        <div style="padding: 40px;">
                            <ul style="font-size: 32px; line-height: 2;">
                                <li style="margin-bottom: 20px;">📄 PDF export with high fidelity</li>
                                <li style="margin-bottom: 20px;">📊 PowerPoint export support</li>
                                <li style="margin-bottom: 20px;">🎨 Preserves styling and gradients</li>
                                <li style="margin-bottom: 20px;">⚡ Fast conversion processing</li>
                            </ul>
                        </div>
                    """
                }
            },
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Technical Details",
                    "subtitle": "Implementation overview",
                    "rich_content": """
                        <div style="padding: 40px;">
                            <div style="background: #f0f4f8; border-left: 5px solid #667eea; padding: 20px; margin-bottom: 20px;">
                                <h3 style="margin: 0 0 10px 0; color: #667eea;">PDF Generation</h3>
                                <p style="margin: 0; font-size: 24px;">Uses Playwright for screenshot-based PDF creation</p>
                            </div>
                            <div style="background: #f0f4f8; border-left: 5px solid #764ba2; padding: 20px;">
                                <h3 style="margin: 0 0 10px 0; color: #764ba2;">PPTX Generation</h3>
                                <p style="margin: 0; font-size: 24px;">Combines Playwright + python-pptx for PowerPoint files</p>
                            </div>
                        </div>
                    """
                }
            },
            {
                "layout": "L29",
                "content": {
                    "hero_content": """
                        <div style="display: flex; flex-direction: column; justify-content: center;
                                    align-items: center; height: 100%;
                                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                            <h1 style="color: white; font-size: 64px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                                Thank You
                            </h1>
                            <p style="color: white; font-size: 28px; margin-top: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                                Download endpoints are working! ✨
                            </p>
                        </div>
                    """
                }
            }
        ]
    }

    try:
        response = requests.post(
            f"{SERVER_URL}/api/presentations",
            json=presentation_data,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        presentation_id = result["id"]

        print_success(f"Presentation created successfully")
        print_info(f"Presentation ID: {presentation_id}")
        print_info(f"Viewer URL: {SERVER_URL}/p/{presentation_id}")

        return presentation_id

    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running on {SERVER_URL}?")
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to create presentation: {e}")
        sys.exit(1)


def download_pdf(presentation_id):
    """Download presentation as PDF."""
    print_header("Step 2: Downloading PDF")

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    try:
        print_info("Requesting PDF download...")
        start_time = time.time()

        response = requests.get(
            f"{SERVER_URL}/api/presentations/{presentation_id}/download/pdf",
            params={
                "landscape": True,
                "print_background": True,
                "quality": "high"
            },
            timeout=120  # 2 minutes timeout
        )
        response.raise_for_status()

        elapsed = time.time() - start_time

        # Save PDF
        pdf_path = OUTPUT_DIR / "test_presentation.pdf"
        pdf_path.write_bytes(response.content)

        file_size = len(response.content)
        print_success(f"PDF downloaded successfully")
        print_info(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print_info(f"Download time: {elapsed:.2f} seconds")
        print_info(f"Saved to: {pdf_path}")

        # Validate PDF
        if response.content.startswith(b'%PDF'):
            print_success("PDF file format validated")
        else:
            print_error("Invalid PDF format")

        return pdf_path

    except requests.exceptions.Timeout:
        print_error("PDF download timed out (>2 minutes)")
        return None
    except Exception as e:
        print_error(f"PDF download failed: {e}")
        return None


def download_pptx(presentation_id):
    """Download presentation as PPTX."""
    print_header("Step 3: Downloading PPTX")

    try:
        print_info("Requesting PPTX download...")
        start_time = time.time()

        response = requests.get(
            f"{SERVER_URL}/api/presentations/{presentation_id}/download/pptx",
            params={
                "aspect_ratio": "16:9",
                "quality": "high"
            },
            timeout=180  # 3 minutes timeout
        )
        response.raise_for_status()

        elapsed = time.time() - start_time

        # Save PPTX
        pptx_path = OUTPUT_DIR / "test_presentation.pptx"
        pptx_path.write_bytes(response.content)

        file_size = len(response.content)
        print_success(f"PPTX downloaded successfully")
        print_info(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print_info(f"Download time: {elapsed:.2f} seconds")
        print_info(f"Saved to: {pptx_path}")

        # Validate PPTX (ZIP format)
        if response.content.startswith(b'PK'):
            print_success("PPTX file format validated (ZIP container)")
        else:
            print_error("Invalid PPTX format")

        return pptx_path

    except requests.exceptions.Timeout:
        print_error("PPTX download timed out (>3 minutes)")
        return None
    except Exception as e:
        print_error(f"PPTX download failed: {e}")
        return None


def test_error_handling():
    """Test error handling with invalid presentation ID."""
    print_header("Step 4: Testing Error Handling")

    try:
        # Test PDF with invalid ID
        print_info("Testing PDF download with invalid ID...")
        response = requests.get(
            f"{SERVER_URL}/api/presentations/invalid-id/download/pdf",
            timeout=10
        )

        if response.status_code == 404:
            print_success("PDF: Correctly returns 404 for invalid ID")
        else:
            print_error(f"PDF: Expected 404, got {response.status_code}")

        # Test PPTX with invalid ID
        print_info("Testing PPTX download with invalid ID...")
        response = requests.get(
            f"{SERVER_URL}/api/presentations/invalid-id/download/pptx",
            timeout=10
        )

        if response.status_code == 404:
            print_success("PPTX: Correctly returns 404 for invalid ID")
        else:
            print_error(f"PPTX: Expected 404, got {response.status_code}")

    except Exception as e:
        print_error(f"Error handling test failed: {e}")


def print_summary(pdf_path, pptx_path):
    """Print test summary."""
    print_header("Test Summary")

    if pdf_path and pdf_path.exists():
        print_success(f"PDF: {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
    else:
        print_error("PDF: Download failed")

    if pptx_path and pptx_path.exists():
        print_success(f"PPTX: {pptx_path} ({pptx_path.stat().st_size:,} bytes)")
    else:
        print_error("PPTX: Download failed")

    print("\n" + "=" * 70)
    print("  Next Steps:")
    print("=" * 70)
    print("1. Open the PDF file to verify visual quality")
    print("2. Open the PPTX file in PowerPoint/Keynote")
    print("3. Check that all slides are present and correctly rendered")
    print("4. Verify gradients, fonts, and styling are preserved")
    print("=" * 70 + "\n")


def main():
    """Run all tests."""
    print("\n" + "🧪" * 35)
    print("  PDF & PPTX Download Endpoints - Manual Test")
    print("🧪" * 35)

    print_info(f"Server URL: {SERVER_URL}")
    print_info(f"Output directory: {OUTPUT_DIR}")

    # Step 1: Create presentation
    presentation_id = create_test_presentation()

    # Wait a moment for server to be ready
    time.sleep(1)

    # Step 2: Download PDF
    pdf_path = download_pdf(presentation_id)

    # Step 3: Download PPTX
    pptx_path = download_pptx(presentation_id)

    # Step 4: Test error handling
    test_error_handling()

    # Print summary
    print_summary(pdf_path, pptx_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
