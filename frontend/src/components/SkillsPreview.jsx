export default function SkillsPreview({ analysis }) {
  if (!analysis) return null

  const scorePercent = Math.round(analysis.matching_score * 100)

  return (
    <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-[#1F4E79]">Job Match Analysis</h3>
        <div className="flex items-center gap-2">
          <div className="w-32 h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${scorePercent}%`,
                backgroundColor: scorePercent >= 70 ? '#22c55e' : scorePercent >= 50 ? '#eab308' : '#ef4444',
              }}
            />
          </div>
          <span className="text-sm font-bold" style={{
            color: scorePercent >= 70 ? '#22c55e' : scorePercent >= 50 ? '#eab308' : '#ef4444',
          }}>
            {scorePercent}% Match
          </span>
        </div>
      </div>

      <div className="mb-3">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Matched Skills:</h4>
        <div className="flex flex-wrap gap-1.5">
          {analysis.matched_skills.map((skill) => (
            <span key={skill} className="px-2 py-0.5 bg-green-100 text-green-800 text-xs rounded-full font-medium">
              {skill}
            </span>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">Extracted Skills by Category:</h4>
        {Object.entries(analysis.extracted_skills).map(([category, skills]) => (
          <div key={category} className="mb-2">
            <span className="text-xs font-semibold text-gray-600">{category}:</span>
            <span className="text-xs text-gray-500 ml-1">{skills.join(', ')}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
