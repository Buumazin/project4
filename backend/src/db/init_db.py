#!/usr/bin/env python3
"""
Database initialization script for FinAlly
Creates tables and seeds initial data if database is empty
"""

from db.schema import init_database
from db.seed import seed_database
from db.init import SessionLocal
import os

def initialize_database():
    """Initialize database with tables and seed data"""
    print("Initializing FinAlly database...")

    # Create tables
    engine = init_database()

    # Check if database is empty (no users)
    session = SessionLocal()

    try:
        from .models import UserProfile
        user_count = session.query(UserProfile).count()

        if user_count == 0:
            print("Database is empty, seeding with initial data...")
            seed_database()
        else:
            print(f"Database already has {user_count} user(s), skipping seed")

    finally:
        session.close()

    print("Database initialization complete!")

if __name__ == "__main__":
    initialize_database()