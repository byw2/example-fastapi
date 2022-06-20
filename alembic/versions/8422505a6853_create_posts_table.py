"""create posts table

Revision ID: 8422505a6853
Revises: 
Create Date: 2022-06-15 21:50:39.563080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8422505a6853'
down_revision = None
branch_labels = None
depends_on = None

# make changes
def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass

# rollback
def downgrade() -> None:
    op.drop_table("posts")
    pass
