import { Fragment, useEffect, useState } from 'react'

import {
  Circle,
  CircleMarker,
  ImageOverlay,
  MapContainer,
  Polyline,
  Polygon,
  Rectangle,
  TileLayer,
  Tooltip,
  useMap,
  useMapEvents,
} from 'react-leaflet'
import { CRS } from 'leaflet'

const mapBounds = [[13, 72], [23, 88]]
const craterRimGrid = [[18, 30], [11, 62], [14, 108], [28, 140], [61, 151], [88, 125], [95, 78], [87, 30], [57, 10]]
const craterFloorGrid = [[25, 35], [20, 67], [25, 105], [38, 132], [64, 137], [82, 113], [86, 73], [78, 35], [55, 20]]

// The backend uses a small local raster grid. This maps that grid to the
// Jezero region so real Mars Trek imagery can sit underneath the demo layers.
function gridToMars([row, column]) {
  return [23 - row * 0.1, 72 + column * 0.1]
}

function rectangleToMars([[top, left], [bottom, right]]) {
  return [gridToMars([top, left]), gridToMars([bottom, right])]
}

function FitMapToBounds() {
  const map = useMap()

  useEffect(() => {
    map.fitBounds(mapBounds)
  }, [map])

  return null
}

function CursorCoordinates() {
  const [coordinates, setCoordinates] = useState(null)

  useMapEvents({
    mousemove: (event) => {
      setCoordinates({ latitude: event.latlng.lat, longitude: event.latlng.lng })
    },
    mouseout: () => setCoordinates(null),
  })

  return (
    <div className="map-coordinate-readout">
      {coordinates ? `LAT ${coordinates.latitude.toFixed(4)} / LON ${coordinates.longitude.toFixed(4)}` : 'MOVE CURSOR OVER MAP'}
    </div>
  )
}

const routeColors = { safest: '#78d5a3', shortest: '#d8b15e', science: '#9b8cc2' }

function MapView({ routes, safetyAssessment, selectedRouteId, stops, visibleLayers }) {
  return (
    <MapContainer
      aria-label="Synthetic Jezero Crater map"
      bounds={mapBounds}
      className="cairn-map"
      crs={CRS.EPSG4326}
      doubleClickZoom
      dragging
      keyboard
      maxBounds={mapBounds}
      maxBoundsViscosity={1}
      maxZoom={7}
      minZoom={0}
      scrollWheelZoom
      zoomDelta={0.5}
      zoomSnap={0.25}
      zoomControl
    >
      <FitMapToBounds />
      <CursorCoordinates />

      {visibleLayers.base && (
        <>
          <ImageOverlay
            alt="Mars Trek Mars surface imagery"
            bounds={mapBounds}
            opacity={1}
            url="/data/mars-trek-jezero-mosaic.jpg"
            zIndex={0}
          />
          <TileLayer
            attribution="Mars Trek / NASA"
            keepBuffer={4}
            noWrap
            opacity={1}
            updateWhenZooming
            updateWhenIdle
            url="https://trek.nasa.gov/tiles/Mars/EQ/Mars_Viking_MDIM21_ClrMosaic_global_232m/1.0.0//default/default028mm/{z}/{x}/{y}.jpg"
            zIndex={1}
          />
          <Polygon
            pathOptions={{ color: '#f0a36f', fillColor: '#7d4433', fillOpacity: 0.08, weight: 2 }}
            positions={craterRimGrid.map(gridToMars)}
          >
            <Tooltip sticky>Jezero rim - synthetic overlay on Mars Trek imagery</Tooltip>
          </Polygon>
          <Polygon
            pathOptions={{ color: '#e18a5f', fillColor: '#5d3028', fillOpacity: 0.06, weight: 1 }}
            positions={craterFloorGrid.map(gridToMars)}
          />
          <Circle center={gridToMars([68, 91])} pathOptions={{ color: '#3d211f', fillColor: '#41221f', fillOpacity: 0.35, weight: 2 }} radius={11000}>
            <Tooltip>Impact crater - synthetic surface detail</Tooltip>
          </Circle>
          <Circle center={gridToMars([39, 78])} pathOptions={{ color: '#3d211f', fillColor: '#41221f', fillOpacity: 0.3, weight: 1 }} radius={6000} />
          <Circle center={gridToMars([63, 128])} pathOptions={{ color: '#d28a5d', fill: false, opacity: 0.6, weight: 2 }} radius={8000} />
        </>
      )}

      {visibleLayers.elevation && (
        <>
          {[22, 32, 42, 52].map((radius, index) => (
            <Circle
              center={gridToMars([50, 80])}
              key={radius}
              pathOptions={{ color: '#d8b15e', fill: false, opacity: 0.7, weight: 1 }}
              radius={radius}
            >
              <Tooltip>Elevation contour {index + 1} - synthetic</Tooltip>
            </Circle>
          ))}
        </>
      )}

      {visibleLayers.slope && (
        <>
          <Polygon
            pathOptions={{ color: '#c65a4e', fillColor: '#c65a4e', fillOpacity: 0.35, weight: 1 }}
              positions={[[65, 110], [79, 125], [91, 112], [82, 98]].map(gridToMars)}
          >
            <Tooltip sticky>Steep slope zone - synthetic hazard overlay</Tooltip>
          </Polygon>
          <Polygon
            pathOptions={{ color: '#d8b15e', fillColor: '#d8b15e', fillOpacity: 0.25, weight: 1 }}
              positions={[[24, 50], [38, 63], [42, 46], [29, 34]].map(gridToMars)}
          >
            <Tooltip sticky>Moderate slope zone - synthetic hazard overlay</Tooltip>
          </Polygon>
        </>
      )}

      {visibleLayers.terrain && (
        <>
          <Rectangle
            bounds={rectangleToMars([[35, 75], [57, 101]])}
            pathOptions={{ color: '#78d5a3', fillColor: '#78d5a3', fillOpacity: 0.24, weight: 1 }}
          >
            <Tooltip>Ancient delta unit - synthetic terrain unit</Tooltip>
          </Rectangle>
          <Rectangle
            bounds={rectangleToMars([[58, 45], [73, 71]])}
            pathOptions={{ color: '#9b8cc2', fillColor: '#9b8cc2', fillOpacity: 0.24, weight: 1 }}
          >
            <Tooltip>Layered rock unit - synthetic terrain unit</Tooltip>
          </Rectangle>
        </>
      )}

      {routes.map((route) => (
        <Fragment key={route.route_id}>
          <Polyline
            key={`${route.route_id}-casing`}
            pathOptions={{ color: '#101619', opacity: route.route_id === selectedRouteId ? 0.95 : 0.65, weight: route.route_id === selectedRouteId ? 11 : 8 }}
            positions={route.path.map(gridToMars)}
          />
          <Polyline
            key={`${route.route_id}-line`}
            pathOptions={{ color: routeColors[route.route_id], opacity: route.route_id === selectedRouteId ? 1 : 0.8, weight: route.route_id === selectedRouteId ? 7 : 5, lineCap: 'round', lineJoin: 'round' }}
            positions={route.path.map(gridToMars)}
          >
            <Tooltip sticky>{route.name} - {route.distance_m} m</Tooltip>
          </Polyline>
        </Fragment>
      ))}

      {safetyAssessment && (
        <CircleMarker center={gridToMars(safetyAssessment.turn_back_point)} pathOptions={{ color: '#c65a4e', fillColor: '#c65a4e', fillOpacity: 1 }} radius={8}>
          <Tooltip permanent direction="left" offset={[-8, 0]}>Turn back at {Math.round(safetyAssessment.turn_back_progress * 100)}%</Tooltip>
        </CircleMarker>
      )}

      {stops.map((stop) => {
        const isEmergency = stop.stop_type === 'emergency'
        const color = isEmergency ? '#78d5a3' : stop.safety_rating === 'green' ? '#78d5a3' : '#d8b15e'
        return (
          <CircleMarker center={gridToMars(stop.point)} key={stop.stop_id} pathOptions={{ color, fillColor: color, fillOpacity: 1 }} radius={isEmergency ? 7 : 6}>
            <Tooltip permanent={stop.stop_id === 'habitat'} direction="right" offset={[8, 0]}>{stop.name}</Tooltip>
          </CircleMarker>
        )
      })}
    </MapContainer>
  )
}

export default MapView
