from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI(title="Elevator Pitch Refinement")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

WEBUI_ENABLED = True  # Set to use open-webui API
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcyYTNjNTgyLWYwNGYtNDExNS05ZTkwLTViOGY2NDA4NGRjOCJ9.U_5DMnbDzSki3I2IFfeibuWzheq7fNlzV3EaOtCjwdA"  # Replace with a valid API key
DEFAULT_MODEL = "gemma2:2b"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_pitch")
async def generate_pitch(
    startup_name: str = Form(...),
    business_model: str = Form(...),
    competitive_advantages: str = Form(...),
    tone: str = Form("persuasive"),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        prompt = f"""
        Generate a compelling elevator pitch for a startup named '{startup_name}'.
        - Business Model: {business_model}
        - Competitive Advantages: {competitive_advantages}
        - Tone: {tone}
        The pitch should be concise (under 75 words), engaging, and clearly convey the startup's value proposition.
        """

        if WEBUI_ENABLED:
            try:
                messages = [{"role": "user", "content": prompt}]
                request_payload = {"model": model, "messages": messages}
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=60.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        return {"elevator_pitch": generated_text}
            except Exception as e:
                print(f"API request failed: {str(e)}")

        raise HTTPException(status_code=500, detail="Failed to generate elevator pitch")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
