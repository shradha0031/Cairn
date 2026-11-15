"""HTTP entry point for the Cairn API."""

from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import ASSUMPTIONS
from .briefing import create_briefing
from .models import AssumptionsResponse, BriefingRequest, BriefingResponse, HealthResponse, LayersResponse, RouteRequest, RouteResponse, RoutesResponse, SafetyRequest, SafetyResponse, StopResponse, StopsResponse
from .routing import generate_candidate_routes
from .safety import assess_safety
from .stops import ALL_STOPS

app = FastAPI(
    title="Cairn API",
    description="Safe-route planning for Mars crews.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Confirm that the API is running and identify the active site."""

    return HealthResponse(status="ok", site=ASSUMPTIONS.site_name)


@app.get("/layers", response_model=LayersResponse)
def layers() -> LayersResponse:
    """Return the layers available in the initial synthetic fixture."""

    return LayersResponse(
        layers=["base imagery", "elevation", "slope", "terrain units"],
        synthetic_data=True,
        real_layers=["base imagery"],
        synthetic_layers=["elevation", "slope", "terrain units"],
    )


@app.get("/assumptions", response_model=AssumptionsResponse)
def assumptions() -> AssumptionsResponse:
    """Expose adjustable demo assumptions to the frontend."""

    return AssumptionsResponse(assumptions=ASSUMPTIONS)


@app.post("/routes", response_model=RoutesResponse)
def routes(request: RouteRequest) -> RoutesResponse:
    """Return route candidates computed from the current terrain grid."""

    try:
        candidates = generate_candidate_routes(request.start, request.end)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return RoutesResponse(
        routes=[RouteResponse.model_validate(asdict(candidate)) for candidate in candidates],
        synthetic_data=True,
    )


@app.post("/safety", response_model=SafetyResponse)
def safety(request: SafetyRequest) -> SafetyResponse:
    """Return the selected route's current return-safety assessment."""

    assessment = assess_safety(request.route_id, request.progress, request.available_minutes)
    return SafetyResponse.model_validate(asdict(assessment))


@app.get("/stops", response_model=StopsResponse)
def stops() -> StopsResponse:
    """Return synthetic science and emergency stops for the demo site."""

    return StopsResponse(
        stops=[StopResponse.model_validate(asdict(stop)) for stop in ALL_STOPS],
        synthetic_data=True,
    )


@app.post("/briefing", response_model=BriefingResponse)
def briefing(request: BriefingRequest) -> BriefingResponse:
    """Explain computed facts without allowing an LLM to change them."""

    result = create_briefing(request.facts)
    return BriefingResponse(summary=result.summary, source=result.source)
