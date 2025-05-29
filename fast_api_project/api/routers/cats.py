from fastapi import APIRouter

# localhost:8000/owners/<int:owner_id>

router=APIRouter(prefix="/owners", tags=["owners"])

@router.post("/", name="Create owner")