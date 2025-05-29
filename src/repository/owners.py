from api.databases.models import Owner


async def create_owner(body, db):
    owner = Owner(**body.model_dump())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner
