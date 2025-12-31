#!/usr/bin/env python3
"""
Migration Script: Add Slide IDs and Parent Ownership

This script migrates existing presentations to the new UUID-based architecture:
1. Adds slide_id to each slide that doesn't have one
2. Adds parent_slide_id to all elements (textboxes, images, charts, etc.)
3. Optionally regenerates UUID-based element IDs for legacy index-based IDs

Usage:
    # Dry run (no changes saved)
    python add_slide_ids.py --dry-run

    # Migrate all presentations
    python add_slide_ids.py

    # Migrate specific presentation
    python add_slide_ids.py --presentation-id abc123

    # Also regenerate element IDs (optional, more disruptive)
    python add_slide_ids.py --regenerate-ids

v7.5.1 Ghost Elements Fix
"""

import asyncio
import argparse
import json
import uuid
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import storage modules
try:
    from storage import PresentationStorage
    from storage_supabase import SupabasePresentationStorage
except ImportError as e:
    print(f"Error importing storage modules: {e}")
    print("Make sure you're running from the v7.5-main directory")
    sys.exit(1)


def generate_slide_id():
    """Generate a new UUID-based slide ID."""
    return f"slide_{uuid.uuid4().hex[:12]}"


def generate_element_id(slide_id: str, element_type: str):
    """Generate a new UUID-based element ID."""
    return f"{slide_id}_{element_type}_{uuid.uuid4().hex[:8]}"


def is_legacy_id(element_id: str) -> bool:
    """Check if an element ID is in the legacy index-based format."""
    if not element_id:
        return False
    # Legacy format: slide-{N}-{slotName} or slide-{N}-slot-{slotName}-element
    return element_id.startswith('slide-') and '-' in element_id[6:]


def migrate_elements(elements: list, slide_id: str, element_type: str, regenerate_ids: bool = False):
    """
    Migrate a list of elements to add parent_slide_id.

    Args:
        elements: List of element dictionaries
        slide_id: The parent slide's slide_id
        element_type: Type of element (textbox, image, chart, etc.)
        regenerate_ids: Whether to regenerate IDs for legacy elements

    Returns:
        Tuple of (migrated_elements, stats_dict)
    """
    stats = {
        'total': len(elements),
        'added_parent_id': 0,
        'regenerated_ids': 0
    }

    for element in elements:
        # Add parent_slide_id if missing
        if not element.get('parent_slide_id'):
            element['parent_slide_id'] = slide_id
            stats['added_parent_id'] += 1

        # Optionally regenerate legacy IDs
        if regenerate_ids and is_legacy_id(element.get('id', '')):
            old_id = element['id']
            element['id'] = generate_element_id(slide_id, element_type)
            element['_migrated_from'] = old_id  # Keep reference for debugging
            stats['regenerated_ids'] += 1

    return elements, stats


def migrate_presentation(presentation: dict, regenerate_ids: bool = False):
    """
    Migrate a single presentation to add slide_ids and parent ownership.

    Args:
        presentation: The presentation dictionary
        regenerate_ids: Whether to regenerate legacy element IDs

    Returns:
        Tuple of (migrated_presentation, migration_stats)
    """
    stats = {
        'slides_processed': 0,
        'slides_added_id': 0,
        'elements': {
            'text_boxes': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0},
            'images': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0},
            'charts': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0},
            'infographics': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0},
            'diagrams': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0},
            'contents': {'total': 0, 'added_parent_id': 0, 'regenerated_ids': 0}
        }
    }

    slides = presentation.get('slides', [])

    for slide in slides:
        stats['slides_processed'] += 1

        # Add slide_id if missing
        if not slide.get('slide_id'):
            slide['slide_id'] = generate_slide_id()
            stats['slides_added_id'] += 1

        slide_id = slide['slide_id']

        # Migrate text_boxes
        if 'text_boxes' in slide:
            slide['text_boxes'], elem_stats = migrate_elements(
                slide['text_boxes'], slide_id, 'textbox', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['text_boxes'][key] += elem_stats[key]

        # Migrate images
        if 'images' in slide:
            slide['images'], elem_stats = migrate_elements(
                slide['images'], slide_id, 'image', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['images'][key] += elem_stats[key]

        # Migrate charts
        if 'charts' in slide:
            slide['charts'], elem_stats = migrate_elements(
                slide['charts'], slide_id, 'chart', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['charts'][key] += elem_stats[key]

        # Migrate infographics
        if 'infographics' in slide:
            slide['infographics'], elem_stats = migrate_elements(
                slide['infographics'], slide_id, 'infographic', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['infographics'][key] += elem_stats[key]

        # Migrate diagrams
        if 'diagrams' in slide:
            slide['diagrams'], elem_stats = migrate_elements(
                slide['diagrams'], slide_id, 'diagram', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['diagrams'][key] += elem_stats[key]

        # Migrate contents (L-series)
        if 'contents' in slide:
            slide['contents'], elem_stats = migrate_elements(
                slide['contents'], slide_id, 'content', regenerate_ids
            )
            for key in ['total', 'added_parent_id', 'regenerated_ids']:
                stats['elements']['contents'][key] += elem_stats[key]

    # Add migration metadata
    presentation['_migration'] = {
        'version': '7.5.1',
        'migrated_at': datetime.utcnow().isoformat(),
        'stats': stats
    }

    return presentation, stats


async def run_migration(args):
    """Run the migration process."""
    # Initialize storage
    use_supabase = os.environ.get('USE_SUPABASE', 'false').lower() == 'true'

    if use_supabase:
        print("Using Supabase storage")
        storage = SupabasePresentationStorage()
    else:
        print("Using local file storage")
        storage = PresentationStorage()

    # Get presentations to migrate
    if args.presentation_id:
        # Migrate single presentation
        presentation = await storage.load(args.presentation_id)
        if not presentation:
            print(f"Error: Presentation '{args.presentation_id}' not found")
            return
        presentations = [(args.presentation_id, presentation)]
    else:
        # Migrate all presentations
        print("Loading all presentations...")
        presentation_ids = await storage.list_all()
        presentations = []
        for pid in presentation_ids:
            pres = await storage.load(pid)
            if pres:
                presentations.append((pid, pres))
        print(f"Found {len(presentations)} presentations")

    # Run migration
    total_stats = {
        'presentations_processed': 0,
        'slides_processed': 0,
        'slides_added_id': 0,
        'elements_updated': 0
    }

    for pres_id, presentation in presentations:
        print(f"\nMigrating presentation: {pres_id}")

        migrated, stats = migrate_presentation(presentation, args.regenerate_ids)

        total_stats['presentations_processed'] += 1
        total_stats['slides_processed'] += stats['slides_processed']
        total_stats['slides_added_id'] += stats['slides_added_id']

        # Count total elements updated
        for elem_type, elem_stats in stats['elements'].items():
            total_stats['elements_updated'] += elem_stats['added_parent_id']
            total_stats['elements_updated'] += elem_stats['regenerated_ids']

        # Print per-presentation stats
        print(f"  Slides: {stats['slides_processed']} processed, {stats['slides_added_id']} added slide_id")
        for elem_type, elem_stats in stats['elements'].items():
            if elem_stats['total'] > 0:
                print(f"  {elem_type}: {elem_stats['total']} total, "
                      f"{elem_stats['added_parent_id']} added parent_id, "
                      f"{elem_stats['regenerated_ids']} regenerated IDs")

        # Save unless dry run
        if not args.dry_run:
            await storage.update(pres_id, migrated)
            print(f"  Saved successfully")
        else:
            print(f"  [DRY RUN] Would save changes")

    # Print summary
    print("\n" + "=" * 50)
    print("MIGRATION SUMMARY")
    print("=" * 50)
    print(f"Presentations processed: {total_stats['presentations_processed']}")
    print(f"Slides processed: {total_stats['slides_processed']}")
    print(f"Slides with new slide_id: {total_stats['slides_added_id']}")
    print(f"Elements updated: {total_stats['elements_updated']}")

    if args.dry_run:
        print("\n[DRY RUN] No changes were saved. Run without --dry-run to apply changes.")


def main():
    parser = argparse.ArgumentParser(
        description='Migrate presentations to UUID-based architecture'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without saving'
    )
    parser.add_argument(
        '--presentation-id',
        type=str,
        help='Migrate only a specific presentation'
    )
    parser.add_argument(
        '--regenerate-ids',
        action='store_true',
        help='Regenerate UUID-based IDs for legacy index-based element IDs'
    )

    args = parser.parse_args()

    print("=" * 50)
    print("Ghost Elements Fix - Migration Script v7.5.1")
    print("=" * 50)
    print(f"Dry run: {args.dry_run}")
    print(f"Regenerate IDs: {args.regenerate_ids}")
    if args.presentation_id:
        print(f"Target presentation: {args.presentation_id}")
    print()

    asyncio.run(run_migration(args))


if __name__ == '__main__':
    main()
