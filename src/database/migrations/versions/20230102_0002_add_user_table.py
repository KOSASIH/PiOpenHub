# 20230102_0002_add_user_table.py
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20230102_0002_add_user_table'
down_revision = '20230101_0001_initial'
branch_labels = None
depends_on = None

def upgrade():
    # Add additional columns or tables here
    pass

def downgrade():
    # Reverse the changes made in the upgrade
    pass
