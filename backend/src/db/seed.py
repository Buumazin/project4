from sqlalchemy.orm import Session
from db.models import UserProfile, Position, WatchlistItem
from db.init import SessionLocal

def seed_database():
    """Seed database with initial data for development/testing"""

    session = SessionLocal()

    try:
        # Create default user if not exists
        user = session.query(UserProfile).filter_by(id="default").first()
        if not user:
            user = UserProfile(
                id="default",
                cash_balance=10000.0
            )
            session.add(user)
            print("Created default user with $10,000 cash")

        # Create sample positions
        sample_positions = [
            {"ticker": "AAPL", "quantity": 10, "avg_cost": 180.0},
            {"ticker": "GOOGL", "quantity": 5, "avg_cost": 140.0},
            {"ticker": "MSFT", "quantity": 8, "avg_cost": 380.0},
            {"ticker": "TSLA", "quantity": 3, "avg_cost": 220.0},
        ]

        for pos_data in sample_positions:
            # Check if position already exists
            existing = session.query(Position).filter_by(
                user_id="default",
                ticker=pos_data["ticker"]
            ).first()

            if not existing:
                position = Position(
                    user_id="default",
                    ticker=pos_data["ticker"],
                    quantity=pos_data["quantity"],
                    avg_cost=pos_data["avg_cost"]
                )
                session.add(position)
                print(f"Created position: {pos_data['quantity']} {pos_data['ticker']} @ ${pos_data['avg_cost']}")

        # Create default watchlist
        default_watchlist = [
            "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN",
            "NFLX", "META", "NVDA", "JPM", "XOM"
        ]

        for ticker in default_watchlist:
            # Check if already in watchlist
            existing = session.query(WatchlistItem).filter_by(
                user_id="default",
                ticker=ticker
            ).first()

            if not existing:
                watchlist_item = WatchlistItem(
                    user_id="default",
                    ticker=ticker
                )
                session.add(watchlist_item)
                print(f"Added to watchlist: {ticker}")

        session.commit()
        print("Database seeded successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()