#!/usr/bin/env python3
"""
Simple validation script to test imports and basic functionality.
Run this to ensure all modules are properly structured.
"""

import sys


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...\n")
    
    modules = [
        'history_store',
        'location_manager',
        'scraper',
        'site_analyzer',
        'ai_writer',
        'mailer',
        'orchestrator'
    ]
    
    failed = []
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name}")
        except Exception as e:
            print(f"✗ {module_name}: {e}")
            failed.append(module_name)
    
    return len(failed) == 0


def test_history_store():
    """Test basic HistoryStore functionality."""
    print("\n\nTesting HistoryStore...\n")
    
    try:
        from history_store import HistoryStore
        
        # Create instance with test database
        store = HistoryStore(db_path="test_bot.db")
        print("✓ HistoryStore initialized")
        
        # Test creating a run
        run_id = store.create_run("Ontario", "test")
        print(f"✓ Created run with ID: {run_id}")
        
        # Test adding a search
        search_id = store.add_search("Ontario", "Toronto", "test", 43.6532, -79.3832, 5000)
        print(f"✓ Added search with ID: {search_id}")
        
        # Test adding a business
        business_id = store.add_business(
            name="Test Business",
            city="Toronto",
            province="Ontario",
            category="test",
            email="test@example.com"
        )
        print(f"✓ Added business with ID: {business_id}")
        
        # Clean up
        import os
        if os.path.exists("test_bot.db"):
            os.remove("test_bot.db")
            print("✓ Cleaned up test database")
        
        return True
        
    except Exception as e:
        print(f"✗ HistoryStore test failed: {e}")
        return False


def test_location_manager():
    """Test basic LocationManager functionality."""
    print("\n\nTesting LocationManager...\n")
    
    try:
        from location_manager import LocationManager
        
        manager = LocationManager()
        print("✓ LocationManager initialized")
        
        # Test getting province cities
        cities = manager.get_province_cities("Ontario")
        print(f"✓ Found {len(cities)} cities in Ontario")
        
        if cities:
            # Test generating grids
            grids = manager.generate_search_grids(cities[0])
            print(f"✓ Generated {len(grids)} search grids for {cities[0]['city']}")
            
            # Test getting all locations
            locations = manager.get_all_search_locations("Ontario", "test")
            print(f"✓ Generated {len(locations)} total search locations")
        
        return True
        
    except Exception as e:
        print(f"✗ LocationManager test failed: {e}")
        return False


def test_environment_check():
    """Check for .env file."""
    print("\n\nChecking environment setup...\n")
    
    import os
    from pathlib import Path
    
    if Path(".env").exists():
        print("✓ .env file found")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'GOOGLE_MAPS_API_KEY',
            'GEMINI_API_KEY',
            'GMAIL_ADDRESS',
            'GMAIL_APP_PASSWORD'
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"⚠ Missing environment variables: {', '.join(missing)}")
            print("  Configure these in .env before running the bot")
            return False
        else:
            print("✓ All required environment variables set")
            return True
    else:
        print("⚠ .env file not found")
        print("  Copy .env.example to .env and configure your API keys")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Email Outreach Bot - Validation Script")
    print("="*60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test HistoryStore
    results.append(("HistoryStore", test_history_store()))
    
    # Test LocationManager
    results.append(("LocationManager", test_location_manager()))
    
    # Check environment
    results.append(("Environment", test_environment_check()))
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All validation tests passed!")
        print("\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Test connections: python run.py --test")
        print("3. Run the bot: python run.py --province=Ontario --category=plumber")
        return 0
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
