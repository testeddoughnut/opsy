"""This is the initial schema for Opsy.

Revision ID: 22d14acc37df
Revises: 
Create Date: 2019-10-03 16:21:51.396397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22d14acc37df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('ldap_group', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_ldap_group'), 'roles', ['ldap_group'], unique=False)
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('full_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('session_token', sa.String(length=255), nullable=True),
    sa.Column('session_token_expires_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_token', name='sess_uc')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_index(op.f('ix_users_session_token'), 'users', ['session_token'], unique=False)
    op.create_table('zones',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('vars', sa.JSON(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_zones_name'), 'zones', ['name'], unique=True)
    op.create_table('groups',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('parent_id', sa.String(length=36), nullable=True),
    sa.Column('zone_id', sa.String(length=36), nullable=True),
    sa.Column('default_priority', sa.BigInteger(), nullable=True),
    sa.Column('vars', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'zone_id'),
    sa.UniqueConstraint('name', 'zone_id')
    )
    op.create_index('groups_name_zone_id_key_not_null', 'groups', ['name', 'zone_id'], unique=True, postgresql_where=sa.text('zone_id IS NOT NULL'), sqlite_where=sa.text('zone_id IS NOT NULL'))
    op.create_index('groups_name_zone_id_key_null', 'groups', ['name'], unique=True, postgresql_where=sa.text('zone_id IS NULL'), sqlite_where=sa.text('zone_id IS NULL'))
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=False)
    op.create_index(op.f('ix_groups_parent_id'), 'groups', ['parent_id'], unique=False)
    op.create_index(op.f('ix_groups_zone_id'), 'groups', ['zone_id'], unique=False)
    op.create_table('hosts',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('zone_id', sa.String(length=36), nullable=False),
    sa.Column('vars', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hosts_name'), 'hosts', ['name'], unique=True)
    op.create_index(op.f('ix_hosts_zone_id'), 'hosts', ['zone_id'], unique=False)
    op.create_table('permissions',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('role_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role_id', 'name')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=False)
    op.create_index(op.f('ix_permissions_role_id'), 'permissions', ['role_id'], unique=False)
    op.create_table('role_mappings',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('role_id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_mappings_role_id'), 'role_mappings', ['role_id'], unique=False)
    op.create_index(op.f('ix_role_mappings_user_id'), 'role_mappings', ['user_id'], unique=False)
    op.create_table('host_group_mappings',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('host_id', sa.String(length=36), nullable=False),
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.Column('priority', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_host_group_mappings_group_id'), 'host_group_mappings', ['group_id'], unique=False)
    op.create_index(op.f('ix_host_group_mappings_host_id'), 'host_group_mappings', ['host_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_host_group_mappings_host_id'), table_name='host_group_mappings')
    op.drop_index(op.f('ix_host_group_mappings_group_id'), table_name='host_group_mappings')
    op.drop_table('host_group_mappings')
    op.drop_index(op.f('ix_role_mappings_user_id'), table_name='role_mappings')
    op.drop_index(op.f('ix_role_mappings_role_id'), table_name='role_mappings')
    op.drop_table('role_mappings')
    op.drop_index(op.f('ix_permissions_role_id'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_hosts_zone_id'), table_name='hosts')
    op.drop_index(op.f('ix_hosts_name'), table_name='hosts')
    op.drop_table('hosts')
    op.drop_index(op.f('ix_groups_zone_id'), table_name='groups')
    op.drop_index(op.f('ix_groups_parent_id'), table_name='groups')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_index('groups_name_zone_id_key_null', table_name='groups')
    op.drop_index('groups_name_zone_id_key_not_null', table_name='groups')
    op.drop_table('groups')
    op.drop_index(op.f('ix_zones_name'), table_name='zones')
    op.drop_table('zones')
    op.drop_index(op.f('ix_users_session_token'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_index(op.f('ix_roles_ldap_group'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
