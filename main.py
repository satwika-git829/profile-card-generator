from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional

app = FastAPI(title="User Profile Card Generator")

# --- Request & Response Schemas ---
class ProfileRequest(BaseModel):
    name: str
    bio: str
    image_url: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    website_or_linkedin: Optional[str] = None

class ProfileResponse(BaseModel):
    name: str
    bio: str
    image_url: Optional[str] = None
    initials: str
    role: Optional[str] = None
    location: Optional[str] = None
    website_or_linkedin: Optional[str] = None

# Helper function to generate initials if image URL is not provided
def get_initials(name: str) -> str:
    parts = name.strip().split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()

# --- POST Endpoint ---
@app.post("/api/generate-card", response_model=ProfileResponse)
def generate_profile_card(profile: ProfileRequest):
    if not profile.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if not profile.bio.strip():
        raise HTTPException(status_code=400, detail="Bio is required")

    initials = get_initials(profile.name)
    
    # Process & return formatted data back to UI
    return ProfileResponse(
        name=profile.name.strip(),
        bio=profile.bio.strip(),
        image_url=profile.image_url.strip() if profile.image_url and profile.image_url.strip() else None,
        initials=initials,
        role=profile.role.strip() if profile.role else None,
        location=profile.location.strip() if profile.location else None,
        website_or_linkedin=profile.website_or_linkedin.strip() if profile.website_or_linkedin else None,
    )

# Static Files Setup
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)