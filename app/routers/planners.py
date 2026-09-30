import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.database import get_db
from app.deps import current_user
from app.models import HomeRequest, PartyRequest
from app.services.ai import ai_service
from app.config import settings

router = APIRouter(prefix="/api", tags=["planners"])

def save(user_id, planner, payload, result):
    with get_db() as db:
        cur = db.execute("INSERT INTO recommendations(user_id,planner,request_json,response_json) VALUES(?,?,?,?)", (user_id, planner, json.dumps(payload), json.dumps(result)))
        return cur.lastrowid

def final(planner, budget, result, source, hid):
    result["planner"] = planner; result["budget"] = budget; result["source"] = source; result["history_id"] = hid
    return result

@router.post("/generate-home")
def home(payload: HomeRequest, user=Depends(current_user)):
    data = payload.model_dump(); result, source = ai_service.generate("home", data); hid=save(user["id"],"home",data,result); return final("home",payload.budget,result,source,hid)

@router.post("/generate-party")
def party(payload: PartyRequest, user=Depends(current_user)):
    data = payload.model_dump(); result, source = ai_service.generate("party", data); hid=save(user["id"],"party",data,result); return final("party",payload.budget,result,source,hid)

@router.post("/generate-jewelry")
async def jewelry(budget: float = Form(...), occasion: str = Form("special occasion"), style: str = Form("classic"), notes: str = Form(""), outfit: UploadFile | None = File(None), user=Depends(current_user)):
    if budget <= 0: raise HTTPException(422, "Budget must be greater than zero")
    image_bytes=None; mime=None
    if outfit:
        if outfit.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(400,"Use JPG, PNG, or WEBP")
        image_bytes=await outfit.read()
        if len(image_bytes) > settings.max_image_mb*1024*1024: raise HTTPException(413,"Image is too large")
        mime=outfit.content_type
    data={"budget":budget,"occasion":occasion,"style":style,"notes":notes}; result, source=ai_service.generate("jewelry",data,image_bytes,mime); hid=save(user["id"],"jewelry",data,result); return final("jewelry",budget,result,source,hid)

@router.get("/history")
def history(user=Depends(current_user)):
    with get_db() as db: rows=db.execute("SELECT id,planner,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 30",(user["id"],)).fetchall()
    return [{"id":r["id"],"planner":r["planner"],"request":json.loads(r["request_json"]),"response":json.loads(r["response_json"]),"created_at":r["created_at"]} for r in rows]

@router.get("/session-info")
def session_info(user=Depends(current_user)): return {"authenticated":True,"user":user}
