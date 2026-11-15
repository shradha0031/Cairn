import { useState } from 'react'

import { fetchRoutes } from '../api/cairnApi'
import RouteTable from './RouteTable'

function RoutePlanner({ onRoutesLoaded, routes, selectedRouteId, onSelectRoute, stops }) {
  const scienceDestinations = stops
    .filter((stop) => stop.stop_type === 'science')
    .map((stop) => ({ id: stop.stop_id, label: stop.name, point: stop.point }))
  const destinations = scienceDestinations
  const [destinationId, setDestinationId] = useState('delta-deposit')
  const selectedDestination = destinations.find((destination) => destination.id === destinationId) || destinations[0]
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function planRoutes(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const destination = destinations.find((item) => item.id === destinationId) || destinations[0]
      const result = await fetchRoutes([41, 55], destination.point)
      onRoutesLoaded(result.routes)
    } catch (requestError) {
      setError(`${requestError.message}. Is the FastAPI server running?`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="route-planner hud-panel">
      <div className="route-planner-header">
        <div>
          <p className="hud-label">ROUTE PLANNER</p>
          <h2 className="mt-2 text-xl font-medium text-hud-sand">Choose a destination</h2>
        </div>
        <span className="route-origin">SOURCE MODEL LAT 18.90 / LON 77.50</span>
      </div>
      <form className="route-form" onSubmit={planRoutes}>
        <label htmlFor="destination">Destination</label>
        <select id="destination" onChange={(event) => setDestinationId(event.target.value)} value={destinationId}>
          {destinations.map((destination) => <option key={destination.id} value={destination.id}>{destination.label}</option>)}
        </select>
        {selectedDestination && <span className="destination-coordinates">DESTINATION MODEL LAT {marsLatitude(selectedDestination.point[0])} / LON {marsLongitude(selectedDestination.point[1])}</span>}
        <button className="route-button" disabled={loading} type="submit">{loading ? 'Planning...' : 'Compare routes'}</button>
      </form>
      {error && <p className="route-error" role="alert">{error}</p>}
      {routes.length > 0 && <RouteTable onSelect={onSelectRoute} routes={routes} selectedRouteId={selectedRouteId} />}
    </section>
  )
}

function marsLatitude(row) {
  return (23 - row * 0.1).toFixed(2)
}

function marsLongitude(column) {
  return (72 + column * 0.1).toFixed(2)
}

export default RoutePlanner
