from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.session import init_db
from core.config import settings
from routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    await init_db()
    yield
    # Run at shutdown


app = FastAPI(title="Mini E-Commerce API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(products.router, prefix=settings.API_PREFIX)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)