"""Evolving database schema

Revision ID: 7
Revises: 6
Create Date: 2024-04-28 12:53:58.530573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7"
down_revision = "6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "earthquake_searches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("closest_earthquake_date", sa.DateTime(), nullable=True),
        sa.Column("closest_earthquake_magnitude", sa.Float(), nullable=True),
        sa.Column("closest_earthquake_distance", sa.Float(), nullable=True),
        sa.Column("closest_earthquake_location", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_earthquake_searches_id"), "earthquake_searches", ["id"], unique=False)
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_earthquake_searches_id"), table_name="earthquake_searches")
    op.drop_table("earthquake_searches")
    # ### end Alembic commands ###
