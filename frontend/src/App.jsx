import { useEffect, useState } from 'react'

import LayerToggle from './components/LayerToggle'
import MapView from './components/MapView'
import RoutePlanner from './components/RoutePlanner'
import SafetyPanel from './components/SafetyPanel'
import StopPanel from './components/StopPanel'
import BriefingPanel from './components/BriefingPanel'
import { fetchStops } from './api/stopsApi'

const layers = [
  { id: 'base', label: 'Base imagery' },
  { id: 'elevation', label: 'Elevation' },
  { id: 'slope', label: 'Slope' },
  { id: 'terrain', label: 'Terrain units' },
]

const initialVisibleLayers = {
  base: true,
  elevation: false,
  slope: false,
  terrain: false,
}

const fallbackStops = [
  { stop_id: 'delta-deposit', name: 'Delta deposit', stop_type: 'science', point: [54, 88], safety_rating: 'blue', description: 'Layered sedimentary terrain and a candidate ancient river delta.', photo_url: 'https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/02024/ids/edr/browse/zcam/ZL0_2024_0846622583_145EBY_N0930000ZCAM10058_1100LMJ02_320.jpg', photo_status: 'NASA Perseverance preview; not georegistered to this synthetic stop' },
  { stop_id: 'river-channel', name: 'Ancient river channel', stop_type: 'science', point: [62, 100], safety_rating: 'green', description: 'A smoother channel approach suitable for careful sampling.', photo_url: null, photo_status: 'pending verification' },
  { stop_id: 'layered-outcrop', name: 'Layered rock outcrop', stop_type: 'science', point: [48, 70], safety_rating: 'blue', description: 'Exposed rock layers with a moderate footing caution.', photo_url: null, photo_status: 'pending verification' },
  { stop_id: 'habitat', name: 'Habitat', stop_type: 'emergency', point: [41, 55], safety_rating: 'green', description: 'Primary return point.', photo_url: null, photo_status: 'not applicable' },
  { stop_id: 'delta-shelter', name: 'Delta shelter', stop_type: 'emergency', point: [55, 80], safety_rating: 'green', description: 'Synthetic shelter waypoint.', photo_url: null, photo_status: 'not applicable' },
  { stop_id: 'rover-cache', name: 'Rover cache', stop_type: 'emergency', point: [64, 96], safety_rating: 'blue', description: 'Synthetic rover support waypoint.', photo_url: null, photo_status: 'not applicable' },
]

function App() {
  const [visibleLayers, setVisibleLayers] = useState(initialVisibleLayers)
  const [routes, setRoutes] = useState([])
  const [selectedRouteId, setSelectedRouteId] = useState('safest')
  const [safetyAssessment, setSafetyAssessment] = useState(null)
  const [stops, setStops] = useState(fallbackStops)
  const selectedRoute = routes.find((route) => route.route_id === selectedRouteId)
  const routeStatus = selectedRoute?.safety_rating || 'standby'

  useEffect(() => {
    fetchStops().then((result) => setStops(result.stops)).catch(() => {})
  }, [])

  function toggleLayer(layerId) {
    setVisibleLayers((currentLayers) => ({
      ...currentLayers,
      [layerId]: !currentLayers[layerId],
    }))
  }

  function handleRoutesLoaded(nextRoutes) {
    setRoutes(nextRoutes)
    setSelectedRouteId(nextRoutes[0]?.route_id || '')
  }

  return (
    <main className="min-h-screen bg-hud-ink px-6 py-8 text-slate-100 sm:px-10">
      <section className="mx-auto max-w-7xl">
        <header className="flex flex-wrap items-end justify-between gap-6 border-b border-hud-line pb-6">
          <div>
            <p className="hud-label">CAIRN // MISSION MAP 01</p>
            <h1 className="mt-2 text-4xl font-semibold tracking-tight text-hud-sand sm:text-6xl">Safe routes across the red planet</h1>
            <p className="mt-3 max-w-xl text-sm text-slate-400">Mission navigation console. Plan the route, read the terrain, and know the way back.</p>
          </div>
          <div className="status-chip"><span className="status-dot" /> Mars Trek imagery // synthetic terrain</div>
        </header>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
          <section className="map-frame overflow-hidden" aria-label="Jezero Crater map">
            <div className="map-heading">
              <span className="hud-label">JEZERO CRATER // MARS TREK BASE</span>
              <span className="map-coordinates">LOCAL GRID 00-160 / 00-100</span>
            </div>
            <MapView routes={routes} safetyAssessment={safetyAssessment} selectedRouteId={selectedRouteId} stops={stops} visibleLayers={visibleLayers} />
          </section>

          <aside className="space-y-5">
            <section className="hud-panel">
              <p className="hud-label">AVAILABLE LAYERS</p>
              <LayerToggle layers={layers} onToggle={toggleLayer} visibleLayers={visibleLayers} />
              <p className="mt-5 text-xs leading-relaxed text-slate-500">Base imagery is from Mars Trek. Elevation, geology, and hazard overlays remain synthetic until matching products are verified.</p>
            </section>
            <section className="hud-panel">
              <p className="hud-label">ROUTE RATING</p>
              <p className={`route-status-value route-status-${routeStatus}`}>{routeStatus.toUpperCase()}</p>
              <p className="mt-1 text-sm text-slate-400">{selectedRoute ? 'Return planning activates in Step 5.' : 'Compare routes to begin.'}</p>
            </section>
          </aside>
        </div>
        <RoutePlanner onRoutesLoaded={handleRoutesLoaded} onSelectRoute={setSelectedRouteId} routes={routes} selectedRouteId={selectedRouteId} stops={stops} />
        <SafetyPanel onSafetyChange={setSafetyAssessment} routeId={selectedRoute?.route_id} />
        {selectedRoute && <BriefingPanel route={selectedRoute} safety={safetyAssessment} />}
        <StopPanel stops={stops} />
      </section>
    </main>
  )
}

export default App
