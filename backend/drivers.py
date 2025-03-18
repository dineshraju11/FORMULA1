from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.firebase_config import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ✅ Add Driver Form
@router.get("/drivers/add", response_class=HTMLResponse)
def add_driver_form(request: Request):
    return templates.TemplateResponse("add_driver.html", {"request": request})


# ✅ Handle Add Driver POST
@router.post("/drivers/add")
def add_driver(
    name: str = Form(...),
    age: int = Form(...),
    poles: int = Form(...),
    wins: int = Form(...),
    points: int = Form(...),
    titles: int = Form(...),
    fastest_laps: int = Form(...),
    team: str = Form(...)
):
    db.collection('drivers').document(name).set({
        "Age": age,
        "Total Pole Positions": poles,
        "Total Race Wins": wins,
        "Total Points Scored": points,
        "Total World Titles": titles,
        "Total Fastest Laps": fastest_laps,
        "Team": team
    })
    return RedirectResponse(url="/drivers/list", status_code=303)


# ✅ View Driver Details
@router.get("/drivers/view/{name}", response_class=HTMLResponse)
def view_driver(request: Request, name: str):
    doc = db.collection('drivers').document(name).get()
    if doc.exists:
        return templates.TemplateResponse("view_driver.html", {"request": request, "driver": doc.to_dict(), "name": name})
    return RedirectResponse(url="/drivers/list", status_code=303)


# ✅ Edit Driver Form (Pre-fill form with existing data)
@router.get("/drivers/edit/{name}", response_class=HTMLResponse)
def edit_driver_form(request: Request, name: str):
    doc = db.collection('drivers').document(name).get()
    if doc.exists:
        return templates.TemplateResponse("edit_driver.html", {"request": request, "driver": doc.to_dict(), "name": name})
    return RedirectResponse(url="/drivers/list", status_code=303)


# ✅ Handle Edit Driver POST (Update Driver in Firestore)
@router.post("/drivers/edit/{name}")
def edit_driver(
    name: str,
    age: int = Form(...),
    poles: int = Form(...),
    wins: int = Form(...),
    points: int = Form(...),
    titles: int = Form(...),
    fastest_laps: int = Form(...),
    team: str = Form(...)
):
    db.collection('drivers').document(name).update({
        "Age": age,
        "Total Pole Positions": poles,
        "Total Race Wins": wins,
        "Total Points Scored": points,
        "Total World Titles": titles,
        "Total Fastest Laps": fastest_laps,
        "Team": team
    })
    return RedirectResponse(url=f"/drivers/view/{name}", status_code=303)


# ✅ Delete Driver
@router.get("/drivers/delete/{name}")
def delete_driver(name: str):
    db.collection('drivers').document(name).delete()
    return RedirectResponse(url="/drivers/list", status_code=303)


# ✅ List all drivers
@router.get("/drivers/list", response_class=HTMLResponse)
def list_drivers(request: Request):
    drivers = [{"name": doc.id, **doc.to_dict()} for doc in db.collection('drivers').stream()]
    return templates.TemplateResponse("list_drivers.html", {"request": request, "drivers": drivers})


# ✅ Query Drivers Form (GET route to show form)
@router.get("/drivers/query", response_class=HTMLResponse)
def query_drivers_form(request: Request):
    return templates.TemplateResponse("query_drivers.html", {"request": request, "results": None})


# ✅ Handle Query Form Submission (POST route to filter and display drivers)
@router.post("/drivers/query", response_class=HTMLResponse)
def query_drivers(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: int = Form(...)
):
    all_drivers = db.collection('drivers').stream()
    matching_drivers = []

    for doc in all_drivers:
        driver = doc.to_dict()
        driver_name = doc.id
        driver_value = driver.get(attribute)

        # Ensure value exists and is numeric
        if driver_value is None or not isinstance(driver_value, (int, float)):
            continue

        # Apply selected comparison logic
        if (comparison == "greater" and driver_value > value) or \
           (comparison == "less" and driver_value < value) or \
           (comparison == "equal" and driver_value == value):
            matching_drivers.append({"name": driver_name, **driver})

    # Render form again with filtered results
    return templates.TemplateResponse("query_drivers.html", {
        "request": request,
        "results": matching_drivers
    })
# Compare Drivers Form (GET)
@router.get("/drivers/compare", response_class=HTMLResponse)
def compare_drivers_form(request: Request):
    drivers = [doc.id for doc in db.collection('drivers').stream()]
    return templates.TemplateResponse("compare_drivers.html", {"request": request, "drivers": drivers})


# Handle Compare Drivers (POST)
@router.post("/drivers/compare", response_class=HTMLResponse)
def compare_drivers(
    request: Request,
    driver1: str = Form(...),
    driver2: str = Form(...)
):
    # Fetch driver 1 data
    doc1 = db.collection('drivers').document(driver1).get()
    driver1_data = doc1.to_dict() if doc1.exists else None

    # Fetch driver 2 data
    doc2 = db.collection('drivers').document(driver2).get()
    driver2_data = doc2.to_dict() if doc2.exists else None

    if not driver1_data or not driver2_data:
        # Handle missing drivers gracefully
        return templates.TemplateResponse("compare_drivers.html", {
            "request": request,
            "drivers": [doc.id for doc in db.collection('drivers').stream()],
            "driver1": None,
            "driver2": None
        })

    return templates.TemplateResponse("compare_drivers.html", {
        "request": request,
        "drivers": [doc.id for doc in db.collection('drivers').stream()],
        "driver1": driver1_data,
        "driver2": driver2_data,
        "name1": driver1,
        "name2": driver2
    })
