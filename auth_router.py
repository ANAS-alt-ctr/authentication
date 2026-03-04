import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreateAuth, Token
from models import User
from security import fake_users_db, hash_password, verify_password, create_access_token

router = APIRouter()
USERS_JSON_FILE = "users.json"

def load_json():
    try:
        with open(USERS_JSON_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"registered_users": [], "auth_history": []}

def save_json(data):
    with open(USERS_JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def record_auth_event(username: str, event_type: str):
    data = load_json()
    if "auth_history" not in data:
        data["auth_history"] = []
    data["auth_history"].append({
        "username": username,
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat()
    })
    save_json(data)

@router.post("/register")
def register(user_in: UserCreateAuth):
    data = load_json()
    registered_users = data.get("registered_users", [])

    if any(u["username"] == user_in.username for u in registered_users):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user_in.password)
    user_model = User(username=user_in.username, hashed_password=hashed_pwd)
    fake_users_db[user_in.username] = user_model
                                                                        
    user_data = {
        "id": len(registered_users) + 1,
        "username": user_in.username,
        "hashed_password": hashed_pwd,
        "name": user_in.name if hasattr(user_in, 'name') else user_in.username,
        "age": getattr(user_in, 'age', 0),
        "city": getattr(user_in, 'city', "Unknown"),
        "email": getattr(user_in, 'email', ""),
        "review": getattr(user_in, 'review', ""),
        "timestamp": datetime.utcnow().isoformat(),
        "analyses": []
    }

    if "registered_users" not in data:
        data["registered_users"] = []
    data["registered_users"].append(user_data)
    save_json(data)

    record_auth_event(user_in.username, "register")

    return {"message": f"User '{user_in.username}' registered successfully", 
            "user_data": user_data}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data = load_json()
    user_dict = next((u for u in data.get("registered_users", []) if u["username"] == form_data.username), None)
    
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    user_model = User(username=user_dict["username"], hashed_password=user_dict["hashed_password"])
    fake_users_db[user_dict["username"]] = user_model
    
    access_token = create_access_token(data={"sub": user_dict["username"]})
    
    record_auth_event(user_dict["username"], "login")
    
    return {"access_token": access_token, "token_type": "bearer"}
