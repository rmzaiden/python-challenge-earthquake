"""Add new fields to city and create country and state models

Revision ID: 2
Revises: 1
Create Date: 2024-04-21 21:02:33.716275

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2"
down_revision = "1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_countries_id"), "countries", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_countries_id"), table_name="countries")
    op.drop_table("countries")
    # ### end Alembic commands ###
