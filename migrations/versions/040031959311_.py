"""empty message

Revision ID: 040031959311
Revises: 
Create Date: 2022-12-15 07:02:19.007119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '040031959311'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orcid_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_token', sa.String(), nullable=True),
    sa.Column('orcid_id', sa.String(), nullable=True),
    sa.Column('orcid_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orcid_user')
    # ### end Alembic commands ###
