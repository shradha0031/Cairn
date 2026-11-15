function StopPanel({ stops }) {
  const scienceStops = stops.filter((stop) => stop.stop_type === 'science')

  return (
    <section className="stops-panel hud-panel">
      <div className="route-planner-header">
        <div>
          <p className="hud-label">EXPLORATION POINTS</p>
          <h2 className="mt-2 text-xl font-medium text-hud-sand">Science stops &amp; support</h2>
        </div>
        <span className="route-origin">{scienceStops.length} SCIENCE STOPS</span>
      </div>
      <div className="stop-list">
        {scienceStops.map((stop) => (
          <article className="stop-card" key={stop.stop_id}>
            <div className="stop-card-heading">
              <h3>{stop.name}</h3>
              <span className={`rating rating-${stop.safety_rating}`}>{stop.safety_rating}</span>
            </div>
            <span className="stop-coordinate">GRID {stop.point[0]} / {stop.point[1]}</span>
            <p>{stop.description}</p>
            {stop.photo_url ? (
              <img alt={`${stop.name} Perseverance preview`} className="stop-photo" src={stop.photo_url} />
            ) : (
              <div className="stop-photo stop-photo-empty">PHOTO PENDING</div>
            )}
            <span className="photo-status">{stop.photo_status}</span>
          </article>
        ))}
      </div>
      <div className="support-strip">
        <span className="hud-label">SUPPORT NETWORK</span>
        <div className="support-list">
          {stops.filter((stop) => stop.stop_type === 'emergency').map((stop) => (
            <span className="support-chip" key={stop.stop_id}><i />{stop.name}</span>
          ))}
        </div>
      </div>
    </section>
  )
}

export default StopPanel
