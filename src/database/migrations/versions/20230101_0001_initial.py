# 20230101_0001_initial.py
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20230101_0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    # Drop user table
    op.drop_table('users')
