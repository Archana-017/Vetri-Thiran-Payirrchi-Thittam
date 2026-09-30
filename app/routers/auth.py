from fastapi import APIRouter, HTTPException, Response
from app.database import get_db
from app.models import RegisterRequest, LoginRequest
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

def user_dict(row): return {"id": row["id"], "name": row["name"], "email": row["email"]}

@router.post("/register")
def register(payload: RegisterRequest, response: Response):
    with get_db() as db:
        if db.execute("SELECT id FROM users WHERE email=?", (payload.email,)).fetchone():
            raise HTTPException(409, "Email already registered")
        cur = db.execute("INSERT INTO users(email,name,password_hash) VALUES(?,?,?)", (payload.email, payload.name, hash_password(payload.password)))
        uid = cur.lastrowid
        row = db.execute("SELECT id,name,email FROM users WHERE id=?", (uid,)).fetchone()
    token = create_access_token(uid); response.set_cookie("access_token", token, httponly=True, samesite="lax")
    return {"access_token": token, "token_type": "bearer", "user": user_dict(row)}

@router.post("/login")
def login(payload: LoginRequest, response: Response):
    with get_db() as db: row = db.execute("SELECT * FROM users WHERE email=?", (payload.email,)).fetchone()
    if not row or not verify_password(payload.password, row["password_hash"]): raise HTTPException(401, "Invalid email or password")
    token = create_access_token(row["id"]); response.set_cookie("access_token", token, httponly=True, samesite="lax")
    return {"access_token": token, "token_type": "bearer", "user": user_dict(row)}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
