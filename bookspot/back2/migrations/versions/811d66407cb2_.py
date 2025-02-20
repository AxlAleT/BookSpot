"""empty message

Revision ID: 811d66407cb2
Revises: 
Create Date: 2024-07-01 18:58:03.211064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '811d66407cb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grupo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=False),
    sa.Column('direccion', sa.String(length=255), nullable=False),
    sa.Column('correo_electronico', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('id_grupo', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_grupo'], ['grupo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    op.drop_table('grupo')
    # ### end Alembic commands ###
