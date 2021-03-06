"""empty message

Revision ID: ebaca45ba907
Revises: 4223eba9a854
Create Date: 2020-07-29 23:27:47.871633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebaca45ba907'
down_revision = '4223eba9a854'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reaccion', sa.Column('fecha', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reaccion', 'fecha')
    # ### end Alembic commands ###
