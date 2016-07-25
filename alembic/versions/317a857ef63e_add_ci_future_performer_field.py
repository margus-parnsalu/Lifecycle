"""add CI_Future_performer_field

Revision ID: 317a857ef63e
Revises: 
Create Date: 2016-07-25 11:09:26.560151

"""

# revision identifiers, used by Alembic.
revision = '317a857ef63e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('sd_ci', sa.Column('performer_new', sa.String(length=30), nullable=True))


def downgrade():
    op.drop_column('sd_ci', 'performer_new')
