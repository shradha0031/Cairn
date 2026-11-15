import { useEffect, useState } from 'react'

import { fetchSafety } from '../api/cairnApi'

function SafetyPanel({ routeId, onSafetyChange }) {
  const [progress, setProgress] = useState(0)
  const [availableMinutes, setAvailableMinutes] = useState(30)
  const [assessment, setAssessment] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    setError('')
    if (!routeId) {
      setAssessment(null)
      return () => { active = false }
    }
    fetchSafety(routeId, progress / 100, availableMinutes)
      .then((nextAssessment) => {
        if (active) {
          setAssessment(nextAssessment)
          onSafetyChange(nextAssessment)
        }
      })
      .catch((requestError) => {
        if (active) setError(`${requestError.message}. Is the FastAPI server running?`)
      })
    return () => { active = false }
  }, [availableMinutes, onSafetyChange, progress, routeId])

  if (error) return <section className="hud-panel route-error" role="alert">{error}</section>

  if (!routeId) {
    return (
      <section className="safety-panel hud-panel">
        <div className="safety-heading">
          <div>
            <p className="hud-label">RETURN SAFETY // STANDBY</p>
            <h2 className="mt-2 text-xl font-medium text-hud-sand">Way back to habitat</h2>
          </div>
          <span className="alert-badge alert-checking">STANDBY</span>
        </div>
        <p className="safety-message">Compare routes to activate the live return calculation.</p>
      </section>
    )
  }

  return (
    <section className="safety-panel hud-panel">
      <div className="safety-heading">
        <div>
          <p className="hud-label">RETURN SAFETY // LIVE</p>
          <h2 className="mt-2 text-xl font-medium text-hud-sand">Way back to habitat</h2>
        </div>
        <span className={`alert-badge alert-${assessment?.alert_level?.toLowerCase() || 'green'}`}>{assessment?.alert_level || 'CHECKING'}</span>
      </div>
      <label className="safety-control" htmlFor="progress">
        <span>Route progress</span>
        <strong>{progress}%</strong>
      </label>
      <input className="progress-slider" id="progress" max="100" min="0" onChange={(event) => setProgress(Number(event.target.value))} type="range" value={progress} />
      <label className="safety-control" htmlFor="available-minutes">
        <span>Demo resource budget (assumption)</span>
        <strong>{availableMinutes} min</strong>
      </label>
      <input id="available-minutes" min="10" onChange={(event) => setAvailableMinutes(Number(event.target.value))} type="range" value={availableMinutes} />
      {assessment && (
        <>
          <p className="safety-message">{assessment.message}</p>
          <div className="safety-metrics">
            <div><span>Way back</span><strong>{assessment.return_time_minutes} min</strong></div>
            <div><span>Return need</span><strong>{assessment.return_need_minutes} min</strong></div>
            <div><span>Reserve</span><strong>{assessment.resource_buffer_minutes} min</strong></div>
            <div><span>Turn-back point</span><strong>{Math.round(assessment.turn_back_progress * 100)}%</strong></div>
          </div>
          <p className="nearest-stop">Nearest emergency stop: <strong>{assessment.nearest_emergency_stop.name}</strong></p>
        </>
      )}
    </section>
  )
}

export default SafetyPanel
