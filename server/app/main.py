from fastapi import FastAPI
from app.routes.base_routes import router as base_router
from app.routes.articles import router as articles_router


app = FastAPI(title="Crypto News AI Backend", version="1.0.0")

app.include_router(base_router)
app.include_router(articles_router, prefix="/articles", tags=["Articles"])
