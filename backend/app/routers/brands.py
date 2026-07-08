from fastapi import APIRouter


router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)


@router.get("/")
def test_brand():

    return {
        "message": "brands router works"
    }