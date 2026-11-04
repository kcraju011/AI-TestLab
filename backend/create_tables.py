from app.database.session import create_tables, engine


try:
    with engine.connect():
        print("PostgreSQL connection successful.")

    create_tables()
    print("Database tables created successfully.")

except Exception as error:
    print(f"Database setup failed: {error}")
    raise
