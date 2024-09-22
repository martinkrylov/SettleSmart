import pytest
from app.database import get_database_connection  # Adjust the import based on your project structure

def test_database_connection():
    db = get_database_connection()
    # Check 1: Ensure the connection is not None
    assert db is not None, "Database connection should not be None"
    # Check 2: Verify resources database exists
    assert db.resources.name == "resources"

    print(db)
    # Additional check: Ensure we can perform a simple query
    result = db.resources.command("ping")
    assert result["ok"] == 1, "Failed to ping the database"

    print("All database checks passed successfully")

def test_collection_names():
    db = get_database_connection()
    collections = list(db.resources.list_collection_names())
    print("collections:", collections)
    # Check: Ensure the expected collection is present
    expected_collections = ["cities", "conditions", "healthcare_professionals", "healthcare_taxonomy_codes"]  # Replace with your expected collection names
    for collection in expected_collections:
        assert collection in collections, f"Collection '{collection}' not found in the database"
    
    print("All expected collections are present")