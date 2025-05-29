from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text

from api.databases.connect import get_db
from api.routers import cats, owners

app = FastAPI()


@app.get("/", name="API root")
def read_root():
    return {"message": "Welcome to fast_api_project"}


@app.get("/health", name="Service availability")
def get_health_status(db=Depends(get_db)):
    try:
        result = db.execute("SELECT 1+1").fetchone()
        print(result)
        if result is None:
            raise Exception
        return {"message": "Service is running"}
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    return {"status": "ok", "message": "Service is running"}


# general
# - root
# - health

# cats
# _create cat
# - delete cat
# - list cat
# - update cat

# owner
# _ create owner
# - delete owner
# - list owner
# - update owner
