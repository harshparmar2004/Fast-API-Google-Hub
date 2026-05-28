from fastapi import APIRouter, Depends
from auth import get_people_service
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class CreateContactRequest(BaseModel):
    given_name: str
    family_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

@router.get("/")
def list_contacts(service = Depends(get_people_service), pageSize: int = 100):
    """List out contacts."""
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=pageSize,
        personFields='names,emailAddresses,phoneNumbers'
    ).execute()
    return results.get('connections', [])

@router.post("/create")
def create_contact(req: CreateContactRequest, service = Depends(get_people_service)):
    """Create a new contact."""
    contact_body = {
        "names": [
            {
                "givenName": req.given_name,
                "familyName": req.family_name or ""
            }
        ]
    }
    if req.email:
         contact_body["emailAddresses"] = [{"value": req.email}]
    if req.phone_number:
         contact_body["phoneNumbers"] = [{"value": req.phone_number}]
    
    result = service.people().createContact(body=contact_body).execute()
    return result

@router.delete("/{resource_name:path}")
def delete_contact(resource_name: str, service = Depends(get_people_service)):
    """Delete a contact (resource_name e.g. people/c123456)."""
    service.people().deleteContact(resourceName=resource_name).execute()
    return {"status": "deleted"}
