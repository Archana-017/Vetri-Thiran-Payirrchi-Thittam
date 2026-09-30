from fastapi import Depends, HTTPException, Request
from app.database import get_db
from app.security import decode_access_token

def current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            token = auth[7:]
    user_id = decode_access_token(token) if token else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    with get_db() as db:
        row = db.execute("SELECT id,email,name FROM users WHERE id=?", (user_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(row)
