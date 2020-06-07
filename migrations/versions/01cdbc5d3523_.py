"""empty message

Revision ID: 01cdbc5d3523
Revises: 
Create Date: 2020-06-07 14:24:52.588961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01cdbc5d3523'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('instructions', sa.String(length=5000), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quantity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.Column('measurement_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['measurement_id'], ['measurement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quantity')
    op.drop_table('recipe')
    op.drop_table('measurement')
    op.drop_table('ingredient')
    op.drop_table('category')
    # ### end Alembic commands ###
