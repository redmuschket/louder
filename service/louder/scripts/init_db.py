import asyncpg
import aiomysql
import sys
import os
import asyncio
from sqlalchemy import text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from core.db.db import engine, Base
from core.db.models.user_files import UserFileModel
from core.db.models.file import FileModel
from core import config


async def test_connection():
    try:
        db_url = config.get("DATABASE_URL")
        print(f"🔗 Testing connection to: {db_url}")

        # Парсим URL для MySQL
        if "mysql+aiomysql://" in db_url:
            # Формат: mysql+aiomysql://user:password@host:port/database
            parts = db_url.replace("mysql+aiomysql://", "").split("@")
            user_pass = parts[0].split(":")
            host_db = parts[1].split("/")
            host_port = host_db[0].split(":")

            user = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ""
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else "3306"  # MySQL порт по умолчанию
            database = host_db[1]

            print(f"👤 User: {user}")
            print(f"🔐 Password: {'*' * len(password)}")
            print(f"🌐 Host: {host}:{port}")
            print(f"📊 Database: {database}")

            # Пробуем подключиться к MySQL
            conn = await aiomysql.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                db=database
            )

            # Проверяем существование базы данных
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT DATABASE()")
                current_db = await cursor.fetchone()
                print(f"📋 Current database: {current_db[0]}")

                # Проверяем существование таблиц
                await cursor.execute("SHOW TABLES")
                tables = await cursor.fetchall()
                if tables:
                    print(f"📦 Existing tables: {[table[0] for table in tables]}")
                else:
                    print("ℹ️ No tables in database")

            # Проверяем версию MySQL
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT VERSION()")
                version = await cursor.fetchone()
                print(f"📋 MySQL version: {version[0]}")

            conn.close()
            print("🎉 MySQL connection successful!")
            return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

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