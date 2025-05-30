from fastapi import FastAPI
from routers.contacts import router

app = FastAPI(title="Contacts API", description="REST API for managing contacts")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
