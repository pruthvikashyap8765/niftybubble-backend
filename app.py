from fastapi import FastAPI
import models
from database import engine
from routers import user, authentication, stockdata
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

# origins = [
#     "http://localhost:5173",  
# ]

origins = [
    "https://niftybubbles.vercel.app/",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(stockdata.router)

