from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request

# Import routers (drivers, teams, auth)
from backend import drivers, teams, auth

# Initialize FastAPI app
app = FastAPI()

# Mount static directory for CSS, JS, Images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(drivers.router)  # Drivers functionality
app.include_router(teams.router)    # Teams functionality
app.include_router(auth.router)     # Authentication routes (login/logout)

# Home route
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ping route for server testing
@app.get("/ping")
def ping():
    return {"status": "Server is running", "firebase": "Connected"}
