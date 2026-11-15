function RouteTable({ routes, selectedRouteId, onSelect }) {
  return (
    <div className="overflow-x-auto">
      <table className="route-table">
        <thead>
          <tr>
            <th>Route</th>
            <th>Distance</th>
            <th>Walk time</th>
            <th>Avg slope</th>
            <th>Safety</th>
            <th>Science</th>
          </tr>
        </thead>
        <tbody>
          {routes.map((route) => (
            <tr className={route.route_id === selectedRouteId ? 'route-row-selected' : ''} key={route.route_id}>
              <td><button className="route-name" onClick={() => onSelect(route.route_id)} type="button">{route.name}</button></td>
              <td>{(route.distance_m / 1000).toFixed(2)} km</td>
              <td>{route.walking_time_minutes.toFixed(0)} min</td>
              <td>{route.average_slope_degrees.toFixed(1)} deg</td>
              <td><span className={`rating rating-${route.safety_rating}`}>{route.safety_rating}</span></td>
              <td>{route.science_value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RouteTable
