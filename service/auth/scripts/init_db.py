import sys
import os
import asyncio
from sqlalchemy import text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db.db import engine, Base
from core.db.models.user import User
from core.db.models.token import Token

async def create_tables():
    try:
        print("🔗 Connecting to database...")
        async with engine.begin() as conn:
            print("📦 Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

async def main():
    success = await create_tables()
    if success:
        print("🎉 Database initialization completed!")
    else:
        print("💥 Database initialization failed!")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    asyncio.run(main())