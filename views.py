import fastapi
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from werkzeug.security import generate_password_hash, check_password_hash
from markets import get_trend





templates = Jinja2Templates('templates')


router = fastapi.APIRouter()


security = HTTPBasic()


users = {'email': [], 'pass_hash': []}

trend = get_trend()



@router.get("/")
def index_get(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@router.post("/")
def index_post(request: Request, email: str = Form(...), password: str = Form(...)):


    if email not in users['email']:

        try:

            pass_hash = generate_password_hash(password)
            users['pass_hash'].append(pass_hash)
            users['email'].append(email)
            return templates.TemplateResponse('index.html', context={'request': request, 'pass_hash': pass_hash, 'email': email.upper()})

        except KeyError:
            msg = 'WROND PASSWORD!'
            return templates.TemplateResponse('index.html', context={'request': request, 'msg': msg})
    else:
        msg = 'SORRY, THAT EMAIL ALREADY EXISTS IN OUR DATABASE!'
        return templates.TemplateResponse('index.html', context={'request': request, 'msg': msg})
    

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):


    usr_email = credentials.username
    usr_pass = credentials.password


    if usr_email in users['email']:
        x = users['email'].index(usr_email)
        pass_hash = users['pass_hash'][x]


        result = check_password_hash(pass_hash, usr_pass)
        if result == True:
            return credentials.username


        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},)


    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},)

@router.get("/signals")
def read_current_user(request: Request, username: str = Depends(get_current_username)):
    nums = range(6)
    msg = 'CONNECTION ERROR. PLEASE TRY AGAIN LATER.'
    try:
        return templates.TemplateResponse('signals.html', context={'request': request, 'trend': trend, 'nums': nums})
    except:
        len(trend) < 6
        return templates.TemplateResponse("index.html", {'request': request, 'msg': msg})

@router.get("/about")
def about_get(request: Request):
    return templates.TemplateResponse('about.html', context={'request': request})

