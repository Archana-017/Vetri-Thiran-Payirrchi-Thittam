from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_register_login_and_home():
    email='test@example.com'
    client.post('/api/auth/register',json={'name':'Test User','email':email,'password':'secret123'})
    r=client.post('/api/auth/login',json={'email':email,'password':'secret123'}); assert r.status_code==200
    r=client.post('/api/generate-home',json={'budget':10000,'rooms':['Living Room'],'style':'modern','notes':''})
    assert r.status_code==200 and r.json()['planner']=='home'
