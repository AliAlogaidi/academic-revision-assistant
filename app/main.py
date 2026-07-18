from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.rewriter import ACADEMIC_INTEGRITY_NOTE, AcademicRewriter
from app.schemas import RewriteRequest, RewriteResponse

app = FastAPI(
    title="Academic Revision Assistant",
    description="An MVP for improving academic draft clarity, structure, and originality.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
rewriter = AcademicRewriter()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/rewrite", response_model=RewriteResponse)
async def rewrite(payload: RewriteRequest) -> RewriteResponse:
    result = await rewriter.rewrite(
        text=payload.text,
        tone=payload.tone.value,
        depth=payload.depth.value,
        include_citation_notes=payload.include_citation_notes,
    )
    return RewriteResponse(
        original=payload.text,
        revised=result.revised,
        provider=result.provider,
        quality_notes=[note.__dict__ for note in result.quality_notes],
        academic_integrity_note=ACADEMIC_INTEGRITY_NOTE,
    )
