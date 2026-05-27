from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.url_scanner import scan_url, explain_threat
from app.auth.router import get_current_user

router = APIRouter()

class URLScanRequest(BaseModel):
    url: str

@router.post("/url")
async def scan_url_endpoint(
    req: URLScanRequest,
    user_id: str = Depends(get_current_user)
):
    result = await scan_url(req.url)

    # Add LLM explanation for medium/high risk
    if result.get('risk_score', 0) > 40:
        result['ai_explanation'] = await explain_threat(result)
    else:
        result['ai_explanation'] = "This site appears safe based on our analysis."

    return result