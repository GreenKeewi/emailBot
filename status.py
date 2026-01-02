#!/usr/bin/env python3
"""
Status CLI for viewing progress.
Usage: python status.py --province=Ontario [--category=plumber]
"""

import argparse
from orchestrator import Orchestrator
from rich.console import Console
from rich.table import Table


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='View outreach bot progress and statistics'
    )
    parser.add_argument(
        '--province',
        required=True,
        help='Province name'
    )
    parser.add_argument(
        '--category',
        default=None,
        help='Optional category filter'
    )
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator()
        
        if not args.category:
            print(f"\n📊 Status for {args.province}")
            print("Specify --category for detailed information\n")
            return
        
        status = orchestrator.get_status(args.province, args.category)
        
        console = Console()
        
        # Create summary table
        table = Table(title=f"\n{args.province} - {args.category} Status", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        # Add rows
        table.add_row("Province Complete", "✅ Yes" if status['complete'] else "⏳ In Progress")
        table.add_row("Total Businesses Found", str(status['total_businesses']))
        table.add_row("Businesses with Email", str(status['businesses_with_email']))
        table.add_row("Emails Sent", str(status['businesses_emailed']))
        
        # Search status
        searches = status.get('searches', {})
        pending = searches.get('pending', 0)
        partial = searches.get('partial', 0)
        complete = searches.get('complete', 0)
        total_searches = pending + partial + complete
        
        table.add_row("Total Search Areas", str(total_searches))
        table.add_row("  - Completed", str(complete))
        table.add_row("  - Partial", str(partial))
        table.add_row("  - Pending", str(pending))
        
        console.print(table)
        
        # Completion percentage
        if total_searches > 0:
            completion_pct = (complete / total_searches) * 100
            print(f"\n📈 Progress: {completion_pct:.1f}% of search areas completed\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    main()
