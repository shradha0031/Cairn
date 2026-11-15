function LayerToggle({ layers, visibleLayers, onToggle }) {
  return (
    <div className="mt-4 space-y-3">
      {layers.map((layer) => (
        <label className="flex items-center justify-between text-sm" key={layer.id}>
          <span>{layer.label}</span>
          <input
            aria-label={`Toggle ${layer.label}`}
            checked={visibleLayers[layer.id]}
            onChange={() => onToggle(layer.id)}
            type="checkbox"
          />
        </label>
      ))}
    </div>
  )
}

export default LayerToggle
