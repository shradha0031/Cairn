import { useState } from 'react'

import { fetchBriefing } from '../api/cairnApi'

function BriefingPanel({ route, safety }) {
  const [briefing, setBriefing] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function generateBriefing() {
    setLoading(true)
    setError('')
    try {
      const result = await fetchBriefing({
        alert_level: safety?.alert_level || route.safety_rating,
        nearest_emergency_stop: safety?.nearest_emergency_stop?.name || 'Habitat',
        progress: safety?.progress || 0,
        remaining_resources_minutes: safety?.remaining_resources_minutes || 0,
        return_need_minutes: safety?.return_need_minutes || 0,
        route_name: route.name,
        turn_back_progress: safety?.turn_back_progress || 1,
      })
      setBriefing(result)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="briefing-panel hud-panel">
      <div className="route-planner-header">
        <div>
          <p className="hud-label">MISSION BRIEFING // OPTIONAL</p>
          <h2 className="mt-2 text-xl font-medium text-hud-sand">Mission summary</h2>
        </div>
        <button className="briefing-button" disabled={loading} onClick={generateBriefing} type="button">{loading ? 'Preparing...' : 'Prepare briefing'}</button>
      </div>
      {briefing && <p className="briefing-copy">{briefing.summary}</p>}
      {briefing && <span className="briefing-source">Briefing based on current Cairn route and resource calculations.</span>}
      {error && <p className="route-error" role="alert">{error}</p>}
    </section>
  )
}

export default BriefingPanel
