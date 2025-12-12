from src.engines.data_miner import DataMiner
import os

DUMMY_DATA_FILE = "dummy_data_logic.py"

CODE = """
import sqlite3
from django.db import models

# Django Model
class UserProfile(models.Model):
    name = models.CharField(max_length=100)

def get_users():
    # Raw SQL
    query = "SELECT * FROM users WHERE active=1"
    conn.execute(query)

def update_db():
    # Raw SQL 2
    sql = "UPDATE settings SET value=1"
    
# Mongoose-like (inside python string? Unlikely but miner is language agnostic regex for now)
# But let's verify logic mainly.
"""

def test_data_miner():
    print(f"Creating {DUMMY_DATA_FILE}...")
    with open(DUMMY_DATA_FILE, "w") as f:
        f.write(CODE)

    print("Running DataMiner...")
    miner = DataMiner()
    artifacts = miner.mine(DUMMY_DATA_FILE)

    if not artifacts:
        print("FAIL: No artifacts found.")
        return

    print("ARTIFACTS FOUND:")
    found_types = []
    found_names = []
    
    for art in artifacts:
        print(f" - [{art['type']}] Line {art['lineno']}: {art.get('name', art.get('content'))}")
        found_types.append(art['type'])
        found_names.append(art.get('name'))

    # Validation
    if "ORM_DJANGO_MODEL" in found_types and "UserProfile" in found_names:
        print("✅ DJANGO MODEL DETECTED")
    else:
        print("❌ DJANGO MODEL FAILED")

    sql_count = found_types.count("SQL_RAW")
    if sql_count >= 2:
        print(f"✅ RAW SQL DETECTED ({sql_count} instances)")
    else:
        print(f"❌ RAW SQL FAILED (Found {sql_count})")

    # Cleanup
    os.remove(DUMMY_DATA_FILE)
    print("Cleanup complete.")

if __name__ == "__main__":
    test_data_miner()
