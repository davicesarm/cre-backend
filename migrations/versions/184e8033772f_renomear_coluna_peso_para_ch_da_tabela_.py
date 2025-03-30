"""Renomear coluna peso para ch da tabela cursoMateria

Revision ID: 184e8033772f
Revises: 
Create Date: 2025-03-29 19:03:16.244477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '184e8033772f'
down_revision = None
branch_labels = None
depends_on = None

table_name = "cursoMateria"
old_column_name = "peso" 
new_column_name = "ch" 
column_type = sa.Integer() 

def upgrade():
    op.alter_column(table_name, old_column_name, new_column_name=new_column_name, existing_type=column_type)

def downgrade():
    op.alter_column(table_name, new_column_name, new_column_name=old_column_name, existing_type=column_type)