"""Initial migration

Revision ID: 1
Revises: 
Create Date: 2024-04-21 19:45:14.948114

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_cities_id"), "cities", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_cities_id"), table_name="cities")
    op.drop_table("cities")
    # ### end Alembic commands ###
