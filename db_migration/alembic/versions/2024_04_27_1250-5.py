"""Add new fields to state model

Revision ID: 5
Revises: 4
Create Date: 2024-04-27 12:50:13.925094

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5"
down_revision = "4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "states", sa.Column("state_abbreviation", sa.String(length=2), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("states", "state_abbreviation")
    # ### end Alembic commands ###