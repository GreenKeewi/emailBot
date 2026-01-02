#!/usr/bin/env python3
"""
Reset CLI for clearing data.
Usage: python reset.py --province=Ontario --category=plumber [--confirm]
"""

import argparse
from orchestrator import Orchestrator


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Reset outreach bot data for a province and category'
    )
    parser.add_argument(
        '--province',
        required=True,
        help='Province name'
    )
    parser.add_argument(
        '--category',
        required=True,
        help='Business category'
    )
    parser.add_argument(
        '--confirm',
        action='store_true',
        help='Confirm reset without prompting'
    )
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator()
        
        # Confirm reset
        if not args.confirm:
            print(f"\n⚠️  WARNING: This will delete all data for:")
            print(f"   Province: {args.province}")
            print(f"   Category: {args.category}")
            print()
            response = input("Are you sure? (yes/no): ")
            
            if response.lower() not in ['yes', 'y']:
                print("Reset cancelled.")
                return 0
        
        # Perform reset
        orchestrator.reset(args.province, args.category)
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    main()
