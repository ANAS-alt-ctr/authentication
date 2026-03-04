from fastapi import APIRouter, Depends, HTTPException, Query, status
from security import get_current_user
import json

router = APIRouter()
USERS_JSON_FILE = "users.json"

def load_json():
    try:
        with open(USERS_JSON_FILE, "r") as f:
            return json.load(f)
    except:
        return {"registered_users": [], "auth_history": []}

def save_json(data):
    with open(USERS_JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

@router.get("/", tags=["users"])
def get_users(_: object = Depends(get_current_user)):
    data = load_json()
    return data.get("registered_users", [])

@router.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int, _: object = Depends(get_current_user)):
    data = load_json()
    registered_users = data.get("registered_users", [])
    user = next((u for u in registered_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    registered_users.remove(user)
    save_json(data)
    return {"message": "User deleted successfully"}

@router.get("/Analyze/{user_id}", tags=["users"])
def analyze_users(user_id: int, _: object = Depends(get_current_user)):
    data = load_json()
    user = next((u for u in data["registered_users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if "analyses" not in user:
        user["analyses"] = []

    analysis_id = len(user["analyses"]) + 1
    review_text = user.get("review", "")
    analysis_data = {
        "analysis_id": analysis_id,
        "word_count": len(review_text.split()),
        "uppercase_letters": sum(1 for l in review_text if l.isupper()),
        "special_characters": sum(1 for c in review_text if not c.isalnum() and not c.isspace())
    }

    user["analyses"].append(analysis_data)
    save_json(data)
    return {"user_id": user_id, **analysis_data}

@router.get("/analyses", tags=["users"])
def get_user_analyses(
    user_id: int,
    limit: int = Query(5, gt=0),
    offset: int = Query(0, ge=0),
    sort: str = Query("asc"),
    min_words: int = Query(None, ge=0),
    _: object = Depends(get_current_user)
):
    data = load_json()
    user = next((u for u in data["registered_users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    analyses_list = user.get("analyses", [])

    if min_words is not None:
        analyses_list = [a for a in analyses_list if a.get("word_count", 0) >= min_words]

    reverse = sort.lower() == "desc"
    analyses_list = sorted(analyses_list, key=lambda x: x.get("analysis_id", 0), reverse=reverse)

    return analyses_list[offset: offset + limit]