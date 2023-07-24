from fastapi import FastAPI

# sqlalchemy
from sqlalchemy import text

# assuming that the users directory is within the modules directory,
# and the models.py file is within the users directory.
from .db.dbconnect import engine, Base, SessionLocal
from .modules.users import routes as user_routes
from .modules.todos import routes as todo_routes

# This will create all the tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes for each group of endpoints
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(todo_routes.router, prefix="/todos", tags=["todos"])


# Check if database is functional
@app.on_event("startup")
async def startup_event():
    # create a new database session for the startup event
    session = SessionLocal()

    # Test database connection
    try:
        # execute a query to check if the connection is successful
        session.execute(text("SELECT 1"))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # close the session
        session.close()


@app.get("/")
def app_root():
    return {"Hello": "World"}
