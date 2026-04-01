export default function ProfileSelector({ profiles, selectedId, onSelect }) {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">Load Profile</label>
      <select
        value={selectedId || ''}
        onChange={(e) => onSelect(e.target.value || null)}
        className="w-full md:w-80 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none bg-white"
      >
        <option value="">Start from scratch</option>
        {profiles.map((p) => (
          <option key={p.id} value={p.id}>{p.name}</option>
        ))}
      </select>
    </div>
  )
}
