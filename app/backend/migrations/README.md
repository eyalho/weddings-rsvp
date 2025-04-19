# Database Migrations

This directory contains SQL migration files for the PostgreSQL database used by the RSVP system.

## Migration Files

The migrations are designed to be run in sequence:

1. `001_initial_schema.sql` - Initial schema setup with user responses table
2. `002_add_user_management.sql` - Adds user management and automated RSVP tracking
3. `003_rename_users_to_rsvp_guests.sql` - Renames users table to rsvp_guests to better reflect its purpose

## How to Run Migrations

### Using psql Command Line

You can run these migrations directly using the PostgreSQL `psql` command:

```bash
# Using connection string
# Internal connection
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a/rsvp_4sgh" -f 001_initial_schema.sql
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a/rsvp_4sgh" -f 002_add_user_management.sql
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a/rsvp_4sgh" -f 003_rename_users_to_rsvp_guests.sql

# External connection
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com/rsvp_4sgh" -f 001_initial_schema.sql
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com/rsvp_4sgh" -f 002_add_user_management.sql
psql "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com/rsvp_4sgh" -f 003_rename_users_to_rsvp_guests.sql
```

### Using Direct psql Connection

Alternatively, you can connect to the database first and then run the migrations:

```bash
# Direct connection to the external database
PGPASSWORD=ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4 psql -h dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com -U eyalh rsvp_4sgh

# Once connected, you can run the migrations using \i command:
\i 001_initial_schema.sql
\i 002_add_user_management.sql
\i 003_rename_users_to_rsvp_guests.sql
```

Or you can apply the migrations directly without connecting interactively:

```bash
# Apply migrations directly
PGPASSWORD=ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4 psql -h dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com -U eyalh rsvp_4sgh -f 001_initial_schema.sql
PGPASSWORD=ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4 psql -h dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com -U eyalh rsvp_4sgh -f 002_add_user_management.sql
PGPASSWORD=ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4 psql -h dpg-d01p48buibrs73b1ht40-a.virginia-postgres.render.com -U eyalh rsvp_4sgh -f 003_rename_users_to_rsvp_guests.sql
```

### Using Python

You can also run migrations programmatically with Python and psycopg2:

```python
import psycopg2
import os

# Database connection string
db_uri = "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a/rsvp_4sgh"

# Directory with migration files
migrations_dir = "app/backend/migrations"

def run_migration(file_path):
    with open(file_path, 'r') as f:
        sql = f.read()
    
    with psycopg2.connect(db_uri) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql)
    
    print(f"Migration {file_path} completed successfully")

# Run the migrations in order
run_migration(os.path.join(migrations_dir, "001_initial_schema.sql"))
run_migration(os.path.join(migrations_dir, "002_add_user_management.sql"))
run_migration(os.path.join(migrations_dir, "003_rename_users_to_rsvp_guests.sql"))
```

### Using the Provided Migration Script

For the most reliable migration experience, use the provided Python script:

```bash
# Run all pending migrations
python app/backend/migrations/run_migrations.py

# Use the external connection
python app/backend/migrations/run_migrations.py --external

# Force run all migrations (even if already applied)
python app/backend/migrations/run_migrations.py --force
```

## Best Practices

1. **Always backup the database before running migrations**
2. **Run migrations during low-traffic periods**
3. **Test migrations in a development environment first**
4. **Keep migrations idempotent when possible** (can be run multiple times without error)
5. **Use transaction blocks for safety**

## Database Schema Overview

After running all migrations, the database will have the following structure:

### Tables
- `user_responses`: Stores all interactions from users
- `rsvp_guests`: Stores consolidated guest information and RSVP status

### Views
- `button_responses`: Simplified view of button interactions
- `numeric_responses`: Simplified view of numeric responses 
- `rsvp_statistics`: Overall RSVP statistics

### Functions and Triggers
- `update_updated_at_column()`: Updates timestamps automatically
- `process_user_response()`: Automatically updates guest information based on responses 