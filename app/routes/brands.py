from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.brand import Brand

from fastapi import Form, status, HTTPException
from fastapi.responses import RedirectResponse

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
@router.get("/add", response_class=HTMLResponse)
async def add_brand_form(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="brands/brand_form.html",
        context={
            "editing": False,
            "brand": None
        }
    )


@router.post("/")
async def create_brand(

    request: Request,

    db: Session = Depends(get_db),

    name: str = Form(...)

):

    old_brand = db.query(Brand).filter(
        Brand.name == name
    ).first()

    if old_brand:

        return templates.TemplateResponse(
            request=request,
            name="brands/brand_form.html",
            context={
                "editing": False,
                "brand": None,
                "error": "This brand already exists."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    brand = Brand(name=name)

    db.add(brand)

    db.commit()

    return RedirectResponse(
        "/brands/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
# ==========================
# Edit Brand
# ==========================

@router.get("/edit/{brand_id}", response_class=HTMLResponse)
async def edit_brand_form(
    request: Request,
    brand_id: int,
    db: Session = Depends(get_db)
):

    brand = db.query(Brand).filter(
        Brand.id == brand_id
    ).first()

    if brand is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="brands/brand_form.html",
        context={
            "editing": True,
            "brand": brand
        }
    )

@router.post("/{brand_id}")
async def update_brand(

    brand_id: int,

    db: Session = Depends(get_db),

    name: str = Form(...)

):

    brand = db.query(Brand).filter(
        Brand.id == brand_id
    ).first()

    if brand is None:

        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    brand.name = name

    db.commit()

    return RedirectResponse(
        "/brands/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )
@router.get("/delete/{brand_id}", response_class=HTMLResponse)
async def confirm_delete_brand(

    request: Request,

    brand_id: int,

    db: Session = Depends(get_db)

):

    brand = db.query(Brand).filter(
        Brand.id == brand_id
    ).first()

    if brand is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="brands/brand_delete.html",
        context={
            "brand": brand
        }
    )
@router.post("/delete/{brand_id}")
async def delete_brand(

    brand_id: int,

    db: Session = Depends(get_db)

):

    brand = db.query(Brand).filter(
        Brand.id == brand_id
    ).first()

    if brand is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    db.delete(brand)

    db.commit()

    return RedirectResponse(
        "/brands/landing",
        status_code=status.HTTP_303_SEE_OTHER
    )