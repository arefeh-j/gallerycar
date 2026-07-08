from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.brand import Brand

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")
@router.get("/landing", response_class=HTMLResponse)
async def brands_landing(
    request: Request,
    db: Session = Depends(get_db)
):

    brands = db.query(Brand).all()

    return templates.TemplateResponse(
        request=request,
        name="brands/brands_landing.html",
        context={
            "request": request,
            "brands": brands
        }
    )