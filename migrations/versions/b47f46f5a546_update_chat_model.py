"""update chat model

Revision ID: b47f46f5a546
Revises: 40c8520b3109
Create Date: 2025-03-28 15:05:27.502659

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b47f46f5a546'
down_revision = '40c8520b3109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.alter_column('graph',
                              existing_type=sa.TEXT(),  # Change to the actual current type
                              type_=sa.LargeBinary(),  # Change to the target type
                              postgresql_using="graph::bytea")
        batch_op.alter_column('memory',
                              existing_type=sa.TEXT(), # Change to the actual current type
                              type_=sa.LargeBinary(),  # Change to the target type
                              postgresql_using="memory::bytea")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.alter_column('memory',
               existing_type=sa.LargeBinary(),
               type_=mysql.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('graph',
               existing_type=sa.LargeBinary(),
               type_=mysql.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
