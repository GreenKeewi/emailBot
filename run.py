#!/usr/bin/env python3
"""
Main CLI entry point for the email outreach bot.
Usage: python run.py --province=Ontario --category=plumber [--limit=50]
"""

import sys
import argparse
from orchestrator import Orchestrator


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Email Outreach Bot - Systematically contact businesses across a province'
    )
    parser.add_argument(
        '--province',
        required=True,
        help='Province name (e.g., Ontario, Quebec, British Columbia, Alberta)'
    )
    parser.add_argument(
        '--category',
        required=True,
        help='Business category (e.g., plumber, electrician, restaurant)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Optional limit on number of emails to send in this run'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connections without running the bot'
    )
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator()
        
        if args.test:
            print("Running connection tests...\n")
            success = orchestrator.test_connection()
            sys.exit(0 if success else 1)
        
        # Run the bot
        stats = orchestrator.run(
            province=args.province,
            category=args.category,
            limit=args.limit
        )
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nBot stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
