import fastapi
import uvicorn
import views
from fastapi.staticfiles import StaticFiles

# Creating an instance of FastAPI application
app = fastapi.FastAPI()

# Managing static files 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Adding each APIRouter to the main FastAPI application
def configure():
    app.include_router(views.router)

configure()
