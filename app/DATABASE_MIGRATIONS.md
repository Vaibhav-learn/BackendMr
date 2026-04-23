# Alembic Configuration for Database Migrations

## Initial Setup

1. Initialize Alembic (already done if alembic/ directory exists):
   alembic init alembic

2. Update alembic/env.py to use SQLAlchemy models

3. Create first migration:
   alembic revision --autogenerate -m "Initial migration"

4. Apply migration:
   alembic upgrade head

## Common Commands

# Create new migration
alembic revision --autogenerate -m "Add new table"

# View migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Upgrade to specific version
alembic upgrade ae1027a6acf

# Current database version
alembic current

## PostgreSQL Commands

# Connect to PostgreSQL (PHARMA database)
psql -U postgres -h localhost -p 54321

# Using existing database
\c Vaibhav

# List tables
\dt

# Describe table
\d table_name

# Backup database
pg_dump -U postgres -h localhost -p 54321 Vaibhav > backup.sql

# Restore database
psql -U postgres -h localhost -p 54321 Vaibhav < backup.sql
