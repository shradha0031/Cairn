"""Plain-language mission briefings with a safe template fallback."""

import os
from typing import Any

import httpx


class BriefingResult:
    """The explanation and how it was produced."""

    def __init__(self, summary: str, source: str) -> None:
        self.summary = summary
        self.source = source


def template_briefing(facts: dict[str, Any]) -> str:
    """Turn already-computed facts into a short crew briefing."""

    route_name = facts.get("route_name", "selected route")
    alert = str(facts.get("alert_level", "GREEN")).upper()
    progress = round(float(facts.get("progress", 0)) * 100)
    return_need = float(facts.get("return_need_minutes", 0))
    remaining = float(facts.get("remaining_resources_minutes", 0))
    turn_back = round(float(facts.get("turn_back_progress", 1)) * 100)
    emergency_stop = facts.get("nearest_emergency_stop", "Habitat")

    if alert == "RED":
        instruction = f"Turn back now or use {emergency_stop}."
    elif alert == "AMBER":
        instruction = f"Turn back soon; the calculated turn-back point is {turn_back}% of the route."
    else:
        instruction = f"Continue while monitoring the turn-back point at {turn_back}% of the route."

    return (
        f"{route_name}: {alert} at {progress}% progress. "
        f"Return need is {return_need:.1f} minutes and {remaining:.1f} minutes remain. "
        f"{instruction}"
    )


def create_briefing(facts: dict[str, Any]) -> BriefingResult:
    """Use an optional LLM only for wording; always fall back to the template."""

    endpoint = os.getenv("CAIRN_LLM_ENDPOINT")
    if not endpoint:
        return BriefingResult(template_briefing(facts), "template")

    prompt = (
        "Rewrite this computed Mars route safety briefing in plain language. "
        "Do not change any numbers or safety level. Return one short paragraph.\n"
        f"{template_briefing(facts)}"
    )
    try:
        response = httpx.post(endpoint, json={"prompt": prompt}, timeout=5.0)
        response.raise_for_status()
        generated = response.json().get("text")
        if isinstance(generated, str) and generated.strip():
            return BriefingResult(generated.strip(), "llm")
    except (httpx.HTTPError, ValueError, TypeError):
        pass

    return BriefingResult(template_briefing(facts), "template-fallback")
