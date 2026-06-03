<<<<<<< HEAD
from fastapi import APIRouter, Depends, Request
=======
from fastapi import APIRouter, Depends
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
from pydantic import BaseModel
from auth import get_people_service
from utils import format_response

router = APIRouter()

<<<<<<< HEAD
@router.get("/groups")
def groups(request: Request, service=Depends(get_people_service)):
    res = service.contactGroups().list().execute()
    return format_response(request, "groups", res.get('contactGroups', []))

@router.post("/group/create")
def create_group(name: str, request: Request, service=Depends(get_people_service)):
    res = service.contactGroups().create(body={'contactGroup': {'name': name}}).execute()
    return format_response(request, "create_group", res)

@router.post("/{id}/group/add")
def add_to_group(id: str, group_id: str, request: Request, service=Depends(get_people_service)):
    return format_response(request, "add_to_group", {"msg": "Added"})

@router.get("/recent")
def recent(request: Request, service=Depends(get_people_service)):
    return format_response(request, "recent", [])

@router.get("/starred")
def starred(request: Request, service=Depends(get_people_service)):
    return format_response(request, "starred", [])

@router.post("/import")
def import_csv(request: Request, service=Depends(get_people_service)):
    return format_response(request, "import", {})

=======
class ContactReq(BaseModel):
    given_name: str
    family_name: str
    email: str
    phone: str = ""

@router.get("/list")
def list_contacts(service=Depends(get_people_service)):
    # 41. List all contacts
    res = service.people().connections().list(
        resourceName='people/me',
        pageSize=50,
        personFields='names,emailAddresses,phoneNumbers'
    ).execute()
    return format_response(res.get('connections', []))

@router.get("/search")
def search_contacts(q: str, service=Depends(get_people_service)):
    # 42. Search contact by name
    res = service.people().searchContacts(
        query=q,
        readMask='names,emailAddresses,phoneNumbers'
    ).execute()
    return format_response(res.get('results', []))

@router.post("/create")
def create_contact(req: ContactReq, service=Depends(get_people_service)):
    # 43. Create new contact
    contact = {
        "names": [{"givenName": req.given_name, "familyName": req.family_name}],
        "emailAddresses": [{"value": req.email}]
    }
    if req.phone:
        contact["phoneNumbers"] = [{"value": req.phone}]
        
    res = service.people().createContact(body=contact).execute()
    return format_response(res)

@router.put("/{resource_name:path}")
def update_contact(resource_name: str, req: ContactReq, service=Depends(get_people_service)):
    # 44. Update contact details
    # Must retrieve etag first
    person = service.people().get(resourceName=resource_name, personFields='names,emailAddresses,phoneNumbers').execute()
    
    person['names'] = [{"givenName": req.given_name, "familyName": req.family_name}]
    person['emailAddresses'] = [{"value": req.email}]
    if req.phone:
        person['phoneNumbers'] = [{"value": req.phone}]
        
    res = service.people().updateContact(
        resourceName=resource_name,
        updatePersonFields='names,emailAddresses,phoneNumbers',
        body=person
    ).execute()
    return format_response(res)
>>>>>>> 35566e39ffc8bcd207f42827b910bfa0d39a0585
