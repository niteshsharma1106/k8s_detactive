#app.py
from fastapi import FastAPI
from api.ingest import router as ingest_router
from api.approval import router as approval_router
from api.incidents import router as incidents_router
from api.argo_ingest import router as argo_router




app = FastAPI()


app.include_router(ingest_router)
app.include_router(approval_router)
app.include_router(incidents_router)
app.include_router(argo_router)


@app.get("/health")
def health():
    return {"status": "ok"}
