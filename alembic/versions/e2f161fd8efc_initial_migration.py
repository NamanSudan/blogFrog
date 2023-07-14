"""Initial migration

Revision ID: e2f161fd8efc
Revises: 
Create Date: 2023-07-14 16:22:48.013793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f161fd8efc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100)),
        sa.Column('content', sa.Text),
        sa.Column('date', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###