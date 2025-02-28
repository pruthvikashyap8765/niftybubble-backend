from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import models
from database import engine
from routers import user, authentication, stockdata

app = FastAPI()

# origins = [
#     "http://localhost:5173",
# ]

# origins = [
#     "https://niftybubbles.vercel.app/",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") != "https":
        https_url = request.url.replace(scheme="https")
        return RedirectResponse(https_url)
    return await call_next(request)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(stockdata.router)