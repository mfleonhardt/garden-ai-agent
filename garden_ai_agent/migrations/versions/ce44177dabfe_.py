"""empty message

Revision ID: ce44177dabfe
Revises: e8175e4ff2b4
Create Date: 2024-11-14 16:07:19.308865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce44177dabfe'
down_revision = 'e8175e4ff2b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('observations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plant_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('observation_type', sa.Enum('HEIGHT', 'SPREAD', 'HEALTH', 'LEAF_COUNT', 'FLOWER_COUNT', 'FRUIT_COUNT', 'GROWTH_STAGE', 'PEST_DAMAGE', 'DISEASE_SEVERITY', name='observationtype'), nullable=False),
    sa.Column('numeric_value', sa.Float(), nullable=True),
    sa.Column('stage_value', sa.Enum('SEED', 'GERMINATION', 'SEEDLING', 'VEGETATIVE', 'FLOWERING', 'FRUITING', 'DORMANT', 'DEAD', name='growthstage'), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('image_data', sa.BLOB(), nullable=True),
    sa.Column('recorded_by', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], name='fk_observations_plant'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('observations')
    # ### end Alembic commands ###
