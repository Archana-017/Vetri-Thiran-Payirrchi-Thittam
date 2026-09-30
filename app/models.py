from typing import Literal
from pydantic import BaseModel, Field, EmailStr

Planner = Literal["home", "party", "jewelry"]

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = "modern"
    notes: str = ""

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = "birthday"
    venue: str = "home"
    city: str = ""
    notes: str = ""

class RecommendationItem(BaseModel):
    category: str
    name: str
    estimated_price: float
    platform: str
    url: str
    reason: str

class RecommendationResponse(BaseModel):
    planner: Planner
    budget: float
    allocated_total: float
    summary: str
    items: list[RecommendationItem]
    tips: list[str] = []
    source: str
    history_id: int | None = None
