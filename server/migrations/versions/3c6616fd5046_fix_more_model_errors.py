"""Fix more model errors

Revision ID: 3c6616fd5046
Revises: 44668e30d67c
Create Date: 2024-09-04 15:02:54.359553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c6616fd5046'
down_revision = '44668e30d67c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('near_misses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_date', sa.DateTime(), nullable=False),
    sa.Column('report_time', sa.DateTime(), nullable=False),
    sa.Column('near_miss_date', sa.DateTime(), nullable=False),
    sa.Column('near_miss_time', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=260), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('near_misses')
    # ### end Alembic commands ###