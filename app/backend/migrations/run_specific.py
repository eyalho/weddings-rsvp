#!/usr/bin/env python3
"""
Script to run a specific migration file directly.
"""
import sys
import os
import psycopg2
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("specific_migration")

# Default connection parameters - same as in run_migrations.py
DEFAULT_HOST = "dpg-d01p48buibrs73b1ht40-a"
DEFAULT_USER = "eyalh"
DEFAULT_PASSWORD = "ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4"
DEFAULT_DATABASE = "rsvp_4sgh"
EXTERNAL_HOST = "dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com"

def run_specific_migration(migration_file, external=True):
    """Run a specific migration file directly."""
    if not os.path.exists(migration_file):
        logger.error(f"Migration file not found: {migration_file}")
        return False
        
    # Determine connection parameters
    host = EXTERNAL_HOST if external else DEFAULT_HOST
    db_uri = f"postgresql://{DEFAULT_USER}:{DEFAULT_PASSWORD}@{host}/{DEFAULT_DATABASE}"
    
    try:
        # Connect to database
        logger.info(f"Connecting to database at {host}")
        conn = psycopg2.connect(db_uri)
        conn.autocommit = False  # We want transaction control
        
        # Read migration file
        with open(migration_file, 'r') as f:
            sql_content = f.read()
            
        # Execute the SQL
        logger.info(f"Running migration: {os.path.basename(migration_file)}")
        with conn.cursor() as cur:
            cur.execute(sql_content)
            
        # Commit the transaction
        conn.commit()
        logger.info(f"Migration {os.path.basename(migration_file)} completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        # Attempt to rollback
        try:
            conn.rollback()
        except:
            pass
        return False
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_specific.py <migration_file> [--local]")
        sys.exit(1)
        
    migration_file = sys.argv[1]
    external = True if len(sys.argv) < 3 or sys.argv[2] != "--local" else False
    
    if run_specific_migration(migration_file, external):
        sys.exit(0)
    else:
        sys.exit(1) 