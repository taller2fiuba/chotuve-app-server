"""empty message

Revision ID: 2940356ebeac
Revises: 6030eadd9681
Create Date: 2020-06-10 00:29:15.278535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2940356ebeac'
down_revision = '6030eadd9681'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comentario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('video', sa.String(length=32), nullable=True),
    sa.Column('usuario', sa.Integer(), nullable=True),
    sa.Column('comentario', sa.String(length=5000), nullable=True),
    sa.Column('fecha', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comentario')
    # ### end Alembic commands ###
