import secrets
import base64
import uvicorn
import pyotp
import random
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlmodel import create_engine, Session, SQLModel, select
from typing import Annotated
from model import MOTD, MOTDBase

# Inisialisasi database SQLite
sqlite_file_name = "motd.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# FastAPI setup
app = FastAPI(docs_url=None, redoc_url=None)
security = HTTPBasic()

# Template setup
templates = Jinja2Templates(directory=".")

# User dan shared secret
users = {
    "sister": "ii2210_sister_astro123",
    "naila": "ii2210_cosmic456"
}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/motd", response_class=HTMLResponse)
async def get_motd(request: Request, session: SessionDep):
    result = session.exec(select(MOTD)).all()
    motd_message = random.choice(result).motd if result else "Belum ada MOTD"
    return templates.TemplateResponse("motd.html", {"request": request, "motd": motd_message})

@app.post("/motd")
async def post_motd(message: MOTDBase, session: SessionDep, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_password_bytes = credentials.password.encode("utf8")
    valid_username, valid_password = False, False

    try:
        if credentials.username in users:
            valid_username = True
            s = base64.b32encode(users.get(credentials.username).encode("utf-8")).decode("utf-8")
            totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
            valid_password = secrets.compare_digest(current_password_bytes, totp.now().encode("utf8"))

            if valid_password and valid_username:
                new_motd = MOTD(motd=message.motd, creator=credentials.username)
                session.add(new_motd)
                session.commit()
                session.refresh(new_motd)
                return {"id": new_motd.id, "text": new_motd.motd}
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid userid or password.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid userid or password.")

    except HTTPException as e:
        raise e

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=17787, reload=True)
