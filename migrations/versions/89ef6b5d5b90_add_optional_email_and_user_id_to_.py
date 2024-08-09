"""Add optional email and user_id to AuditLog

Revision ID: 89ef6b5d5b90
Revises: f31aa6e4debe
Create Date: 2024-08-09 16:39:40.346745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89ef6b5d5b90'
down_revision = 'f31aa6e4debe'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('audit_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('audit_logs', schema=None) as batch_op:
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def upgrade_wms():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_wms():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

