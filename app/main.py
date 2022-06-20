from fastapi import FastAPI
from database import engine
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
import models

# list of origins that we are allowing to make requests to our
# app
origins = ["https://www.google.com"]

# create all our models defined in models class
# and using engine to connect to Postgres database
# with Alembic, this is unnecessary
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# decorator makes method a route
# get request using the route "/"
# invokes the function once request is recieved

# Route: '/'
@app.get("/")
def root():
    return {'content': 'Hello World!'}

# add each APIRouter to the main FastAPI application
# include all the routes from that router as part of it
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




