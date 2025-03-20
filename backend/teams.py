# teams.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.firebase_config import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Add Team Form (GET)
@router.get("/teams/add", response_class=HTMLResponse)
def add_team_form(request: Request):
    return templates.TemplateResponse("add_team.html", {"request": request})


# Handle Add Team (POST)
@router.post("/teams/add")
def add_team(
    name: str = Form(...),
    founded: int = Form(...),
    poles: int = Form(...),
    wins: int = Form(...),
    titles: int = Form(...),
    position: int = Form(...)
):
    db.collection('teams').document(name).set({
        "Year Founded": founded,
        "Total Pole Positions": poles,
        "Total Race Wins": wins,
        "Total Constructor Titles": titles,
        "Last Season Position": position
    })
    return RedirectResponse(url="/teams/list", status_code=303)


# List All Teams (GET)
@router.get("/teams/list", response_class=HTMLResponse)
def list_teams(request: Request):
    teams = [{"name": doc.id, **doc.to_dict()} for doc in db.collection('teams').stream()]
    return templates.TemplateResponse("list_teams.html", {"request": request, "teams": teams})


# View Team Details (GET)
@router.get("/teams/{name}", response_class=HTMLResponse)
def view_team(request: Request, name: str):
    doc = db.collection('teams').document(name).get()
    if doc.exists:
        return templates.TemplateResponse("view_team.html", {"request": request, "team": doc.to_dict(), "name": name})
    return RedirectResponse(url="/teams/list", status_code=303)


# Edit Team Form (GET)
@router.get("/teams/edit/{name}", response_class=HTMLResponse)
def edit_team_form(request: Request, name: str):
    doc = db.collection('teams').document(name).get()
    if doc.exists:
        return templates.TemplateResponse("edit_team.html", {"request": request, "team": doc.to_dict(), "name": name})
    return RedirectResponse(url="/teams/list", status_code=303)


# Handle Edit Team (POST)
@router.post("/teams/edit/{name}")
def edit_team(
    name: str,
    founded: int = Form(...),
    poles: int = Form(...),
    wins: int = Form(...),
    titles: int = Form(...),
    position: int = Form(...)
):
    db.collection('teams').document(name).update({
        "Year Founded": founded,
        "Total Pole Positions": poles,
        "Total Race Wins": wins,
        "Total Constructor Titles": titles,
        "Last Season Position": position
    })
    return RedirectResponse(url=f"/teams/{name}", status_code=303)


# Delete Team (GET)
@router.get("/teams/delete/{name}")
def delete_team(name: str):
    db.collection('teams').document(name).delete()
    return RedirectResponse(url="/teams/list", status_code=303)


# QUERY Teams - Show Form (GET)
@router.get("/teams/query", response_class=HTMLResponse)
def query_teams_form(request: Request):
    return templates.TemplateResponse("query_teams.html", {"request": request, "results": None})


# QUERY Teams - Handle Query (POST)
@router.post("/teams/query", response_class=HTMLResponse)
def query_teams(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: int = Form(...)
):
    results = []
    all_teams = db.collection('teams').stream()

    for doc in all_teams:
        team = doc.to_dict()
        team_name = doc.id
        team_value = team.get(attribute)

        # Skip if attribute not present or not numeric
        if team_value is None or not isinstance(team_value, (int, float)):
            continue

        # Apply comparison
        if (comparison == "greater" and team_value > value) or \
           (comparison == "less" and team_value < value) or \
           (comparison == "equal" and team_value == value):
            results.append({"name": team_name, **team})

    return templates.TemplateResponse("query_teams.html", {"request": request, "results": results})


# ✅ COMPARE Teams - Show Form and Compare via GET
@router.get("/teams/compare", response_class=HTMLResponse)
def compare_teams_form(request: Request, team1: str = None, team2: str = None):
    team1_data = None
    team2_data = None

    # Fetch team1 details if provided
    if team1:
        doc1 = db.collection('teams').document(team1).get()
        if doc1.exists:
            team1_data = doc1.to_dict()
            team1_data["name"] = team1  # Include team name

    # Fetch team2 details if provided
    if team2:
        doc2 = db.collection('teams').document(team2).get()
        if doc2.exists:
            team2_data = doc2.to_dict()
            team2_data["name"] = team2  # Include team name

    return templates.TemplateResponse("compare_teams.html", {
        "request": request,
        "team1": team1_data,
        "team2": team2_data
    })
