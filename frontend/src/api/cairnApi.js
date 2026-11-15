const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function fetchRoutes(start, end) {
  const response = await fetch(`${API_URL}/routes`, {
    body: JSON.stringify({ start, end }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error(`Route request failed (${response.status})`)
  }

  return response.json()
}

export async function fetchSafety(routeId, progress, availableMinutes) {
  const response = await fetch(`${API_URL}/safety`, {
    body: JSON.stringify({ route_id: routeId, progress, available_minutes: availableMinutes }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error(`Safety request failed (${response.status})`)
  }

  return response.json()
}

export async function fetchBriefing(facts) {
  const response = await fetch(`${API_URL}/briefing`, {
    body: JSON.stringify({ facts }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error(`Briefing request failed (${response.status})`)
  }

  return response.json()
}
