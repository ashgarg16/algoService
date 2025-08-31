import os
from fastapi import FastAPI, Depends, Form, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from database import SessionLocal, engine
from models.user import Base, User
from services.auth_service import AuthService
from services.auth_service import verify_password
from dependencies.auth import get_current_user, require_role
from database import get_db
from fastapi import Form


# ------------------ CONFIG ------------------
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="CHANGE_ME_TO_A_RANDOM_SECRET")  # store in env in prod
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



# ------------------ Bootstrap Initial Admin ------------------
@app.on_event("startup")
def create_initial_admin():
    db = SessionLocal()
    auth = AuthService(db)
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if not existing_admin:
        auth.register_user(ADMIN_EMAIL, ADMIN_PASSWORD, role="admin")
        print(f"✅ Initial admin created: {ADMIN_EMAIL}")
    db.close()

# ------------------ ROUTES ------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if request.session.get("user_email"):
        # print("Redirecting to dashboard")
        return RedirectResponse("/dashboard")
    # print("Rendering login page")
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "message": ""})

@app.post("/register")
def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    if auth_service.register_user(email, password):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "message": "Email already exists"})

@app.post("/login")
def login(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid credentials"
        })
    if not user.is_active:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Account is deactivated. Contact admin."
        })
    request.session["user_email"] = user.email
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse("/")
    user = db.query(User).filter(User.email == user_email).first()
    is_admin = user.role == "admin" if user else False
    users = db.query(User).all() if is_admin else []
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_email": user_email,
        "is_admin": is_admin,
        "users": users
    })

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")

# ------------------ TOKEN REFRESH ------------------
@app.post("/refresh-token")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.session.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    auth_service = AuthService(db)
    new_access = auth_service.refresh_access_token(refresh_token)
    if not new_access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    request.session["access_token"] = new_access
    return {"access_token": new_access}

# ------------------ PASSWORD RESET ------------------
@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_form(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request, "message": ""})

@app.post("/forgot-password")
def forgot_password(email: str = Form(...), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token = auth_service.generate_reset_token(email)
    if not token:
        return {"message": "Email not found"}
    # In production, send token via email. For now, return it for testing.
    return {"reset_token": token}

@app.get("/reset-password", response_class=HTMLResponse)
def reset_password_form(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request, "message": ""})

@app.post("/reset-password")
def reset_password(token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    if auth_service.reset_password(token, new_password):
        return {"message": "Password reset successful"}
    return {"message": "Invalid or expired token"}

# ------------------ ADMIN DELETE USER ------------------
@app.post("/admin/delete-user")
def admin_delete_user(
    request: Request,
    target_email: str = Form(...),
    db: Session = Depends(get_db)
):
    current_email = request.session.get("user_email")
    if not current_email:
        raise HTTPException(status_code=401, detail="Not logged in")

    user = db.query(User).filter(User.email == current_email).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    auth_service = AuthService(db)
    if auth_service.delete_user(current_email, target_email):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/admin/user/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = True
        db.commit()
    return RedirectResponse("/dashboard", status_code=303)

@app.post("/admin/user/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = False
        db.commit()
    return RedirectResponse("/dashboard", status_code=303)

