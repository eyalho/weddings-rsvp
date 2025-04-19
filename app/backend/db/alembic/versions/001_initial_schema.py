"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2023-08-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_responses table
    op.create_table(
        'user_responses',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('phone_number', sa.String(20), nullable=False, index=True),
        sa.Column('question_key', sa.String(50), nullable=False, index=True),
        sa.Column('response_text', sa.Text(), nullable=True),
        sa.Column('response_value', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), 
                 onupdate=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create rsvp_guests table
    op.create_table(
        'rsvp_guests',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_response_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('attending', sa.Boolean(), nullable=False),
        sa.Column('dietary_restrictions', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), 
                 onupdate=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_response_id'], ['user_responses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create button_responses view
    op.execute("""
    CREATE VIEW button_responses AS
    SELECT 
        ur.id,
        ur.question_key,
        ur.response_value,
        COUNT(*) as count
    FROM 
        user_responses ur
    WHERE 
        ur.question_key = 'button_response'
    GROUP BY 
        ur.id, ur.question_key, ur.response_value
    """)
    
    # Create numeric_responses view
    op.execute("""
    CREATE VIEW numeric_responses AS
    SELECT 
        ur.question_key,
        MIN(CAST(ur.response_value AS NUMERIC)) as min_value,
        MAX(CAST(ur.response_value AS NUMERIC)) as max_value,
        AVG(CAST(ur.response_value AS NUMERIC)) as avg_value,
        COUNT(*) as count
    FROM 
        user_responses ur
    WHERE 
        ur.question_key = 'numeric_response'
        AND ur.response_value ~ '^[0-9]+$'
    GROUP BY 
        ur.question_key
    """)
    
    # Create rsvp_statistics view
    op.execute("""
    CREATE VIEW rsvp_statistics AS
    SELECT
        COUNT(DISTINCT rg.id) as total_guests,
        SUM(CASE WHEN rg.attending = TRUE THEN 1 ELSE 0 END) as attending_count,
        SUM(CASE WHEN rg.attending = FALSE THEN 1 ELSE 0 END) as not_attending_count,
        COUNT(DISTINCT rg.id) as total_responses,
        SUM(CASE WHEN rg.attending = TRUE THEN 1 ELSE 0 END) as attending_guests,
        SUM(CASE WHEN rg.attending = FALSE THEN 1 ELSE 0 END) as not_attending_guests
    FROM
        rsvp_guests rg
    """)
    

def downgrade() -> None:
    # Drop views
    op.execute("DROP VIEW IF EXISTS rsvp_statistics")
    op.execute("DROP VIEW IF EXISTS numeric_responses")
    op.execute("DROP VIEW IF EXISTS button_responses")
    
    # Drop tables
    op.drop_table('rsvp_guests')
    op.drop_table('user_responses') 