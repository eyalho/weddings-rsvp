#!/usr/bin/env python3
"""
Database migration script for RSVP system.

This script runs PostgreSQL migrations in the correct order.
"""
import os
import sys
import argparse
import logging
import psycopg2
from psycopg2 import sql

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("db_migrations")

# Default migration directory
MIGRATIONS_DIR = os.path.dirname(os.path.abspath(__file__))

# Default connection parameters
DEFAULT_HOST = "dpg-d01p48buibrs73b1ht40-a"
DEFAULT_USER = "eyalh"
DEFAULT_PASSWORD = "ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4"
DEFAULT_DATABASE = "rsvp_4sgh"

# External host
EXTERNAL_HOST = "dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com"

# Default connection string (internal connection)
DEFAULT_DB_URI = f"postgresql://{DEFAULT_USER}:{DEFAULT_PASSWORD}@{DEFAULT_HOST}/{DEFAULT_DATABASE}"

# External connection
EXTERNAL_DB_URI = f"postgresql://{DEFAULT_USER}:{DEFAULT_PASSWORD}@{EXTERNAL_HOST}/{DEFAULT_DATABASE}"


def get_connection(db_uri=None, host=None, user=None, password=None, database=None):
    """
    Get a database connection using either URI or direct parameters.
    
    Args:
        db_uri: Database URI string
        host: Database host
        user: Database user
        password: Database password
        database: Database name
        
    Returns:
        Database connection
    """
    if db_uri:
        return psycopg2.connect(db_uri)
    else:
        return psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )


def run_migration_file(conn, file_path):
    """Run a single migration file."""
    logger.info(f"Running migration: {os.path.basename(file_path)}")
    
    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        # Execute the SQL script
        with conn.cursor() as cur:
            cur.execute(sql_content)
        
        logger.info(f"Migration {os.path.basename(file_path)} completed successfully")
        return True
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False


def setup_migrations_table(conn):
    """Set up the migrations table if it doesn't exist."""
    logger.info("Setting up migrations tracking table")
    
    try:
        with conn.cursor() as cur:
            # Create the migrations table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(255) UNIQUE NOT NULL,
                    applied_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
            """)
        logger.info("Migrations table ready")
        return True
    except Exception as e:
        logger.error(f"Failed to set up migrations table: {str(e)}")
        return False


def get_applied_migrations(conn):
    """Get list of already applied migrations."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT migration_name FROM schema_migrations ORDER BY id;")
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to get applied migrations: {str(e)}")
        return []


def mark_migration_as_applied(conn, migration_name):
    """Mark a migration as applied in the tracking table."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO schema_migrations (migration_name) VALUES (%s);",
                (migration_name,)
            )
        return True
    except Exception as e:
        logger.error(f"Failed to mark migration as applied: {str(e)}")
        return False


def run_migrations(conn, migrations_dir=MIGRATIONS_DIR, force=False):
    """
    Run all migrations in the specified directory.
    
    Args:
        conn: Database connection
        migrations_dir: Directory containing migration files
        force: Whether to force run all migrations
        
    Returns:
        True if all migrations succeeded, False otherwise
    """
    logger.info(f"Running migrations from directory: {migrations_dir}")
    
    # Get sorted list of migration files
    migration_files = sorted([
        f for f in os.listdir(migrations_dir) 
        if f.endswith('.sql') and not f.startswith('.')
    ])
    
    if not migration_files:
        logger.warning("No migration files found!")
        return True
    
    try:
        # Set auto-commit
        conn.autocommit = True
        
        # Set up the migrations table
        if not setup_migrations_table(conn):
            return False
        
        # Get already applied migrations
        applied_migrations = get_applied_migrations(conn) if not force else []
        
        # Run migrations that haven't been applied yet
        success = True
        for migration_file in migration_files:
            if migration_file in applied_migrations and not force:
                logger.info(f"Skipping already applied migration: {migration_file}")
                continue
                
            file_path = os.path.join(migrations_dir, migration_file)
            if run_migration_file(conn, file_path):
                mark_migration_as_applied(conn, migration_file)
            else:
                success = False
                break
        
        return success
        
    except Exception as e:
        logger.error(f"Error during migrations: {str(e)}")
        return False


def main():
    """Main function to run migrations."""
    parser = argparse.ArgumentParser(description="Run database migrations")
    
    # Connection mode group
    conn_group = parser.add_mutually_exclusive_group()
    conn_group.add_argument(
        "--uri", 
        default=os.environ.get("DATABASE_URL", DEFAULT_DB_URI),
        help="Database connection URI"
    )
    conn_group.add_argument(
        "--direct", 
        action="store_true",
        help="Use direct connection parameters instead of URI"
    )
    
    # Connection parameters
    parser.add_argument(
        "--host", 
        default=os.environ.get("PGHOST", DEFAULT_HOST),
        help="Database host"
    )
    parser.add_argument(
        "--external", 
        action="store_true",
        help="Use external database connection"
    )
    parser.add_argument(
        "--user", 
        default=os.environ.get("PGUSER", DEFAULT_USER),
        help="Database user"
    )
    parser.add_argument(
        "--password", 
        default=os.environ.get("PGPASSWORD", DEFAULT_PASSWORD),
        help="Database password"
    )
    parser.add_argument(
        "--database", 
        default=os.environ.get("PGDATABASE", DEFAULT_DATABASE),
        help="Database name"
    )
    
    # Other options
    parser.add_argument(
        "--dir", 
        default=MIGRATIONS_DIR,
        help="Directory containing migration files"
    )
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force run all migrations, even if already applied"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("Starting migrations")
        
        # Determine how to connect
        if args.direct:
            # Use direct connection parameters
            host = EXTERNAL_HOST if args.external else args.host
            conn = get_connection(
                host=host,
                user=args.user,
                password=args.password,
                database=args.database
            )
            logger.info(f"Connected to database using direct parameters (host: {host})")
        else:
            # Use connection URI
            db_uri = EXTERNAL_DB_URI if args.external else args.uri
            conn = get_connection(db_uri=db_uri)
            logger.info(f"Connected to database using URI")
        
        # Run migrations
        success = run_migrations(conn, args.dir, args.force)
        
        # Close connection
        conn.close()
        
        if success:
            logger.info("All migrations completed successfully")
            sys.exit(0)
        else:
            logger.error("Migrations failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Migration process failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 