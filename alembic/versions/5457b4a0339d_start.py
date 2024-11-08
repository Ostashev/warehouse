"""start

Revision ID: 5457b4a0339d
Revises: 
Create Date: 2024-11-05 20:35:00.176590

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5457b4a0339d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    product_table = op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('current_status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productionbatch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('warehouse', sa.Boolean(), nullable=True),
    sa.CheckConstraint("status IN ('start', 'end')", name='status_check'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='fk_product_id'),
    sa.PrimaryKeyConstraint('id')
    )
    inventory_table = op.create_table('warehouseinventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.CheckConstraint('quantity >= 0', name='quantity_non_negative'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='fk_product_id_warehouse_inventory'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    op.bulk_insert(
        product_table,
        [
            {
                'id': 1,
                'model': 'Model A',
                'current_status': 'OUT_OF_STOCK'
            },
            {
                'id': 2,
                'model': 'Model B',
                'current_status': 'OUT_OF_STOCK'
            },
            {
                'id': 3,
                'model': 'Model C',
                'current_status': 'OUT_OF_STOCK'
            },
        ]
    )

    op.bulk_insert(
        inventory_table,
        [
            {
                'id': 1,
                'product_id': 1,
                'quantity': 0,
                'location': 'A1',
            },
            {
                'id': 2,
                'product_id': 2,
                'quantity': 0,
                'location': 'B1',
            },
            {
                'id': 3,
                'product_id': 3,
                'quantity': 0,
                'location': 'C1',
            },
        ]
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warehouseinventory')
    op.drop_table('productionbatch')
    op.drop_table('product')
    # ### end Alembic commands ###
