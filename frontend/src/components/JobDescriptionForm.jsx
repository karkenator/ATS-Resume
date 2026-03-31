export default function JobDescriptionForm({ data, onChange }) {
  const update = (key, value) => onChange({ ...data, [key]: value })

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Job Description</h2>
      <p className="text-sm text-gray-500 mb-4">Paste the full job description below. The AI will extract skills and tailor your resume to match.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Company Name <span className="text-red-500">*</span></label>
          <input
            value={data.company_name}
            onChange={(e) => update('company_name', e.target.value)}
            placeholder="Google"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Job Title <span className="text-red-500">*</span></label>
          <input
            value={data.job_title}
            onChange={(e) => update('job_title', e.target.value)}
            placeholder="Senior Software Engineer"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
          />
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Company URL</label>
          <input
            value={data.company_url}
            onChange={(e) => update('company_url', e.target.value)}
            placeholder="https://google.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Job Description <span className="text-red-500">*</span>
        </label>
        <textarea
          value={data.description}
          onChange={(e) => update('description', e.target.value)}
          placeholder="Paste the full job description here..."
          rows={12}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none resize-y font-mono text-sm"
        />
        <p className="text-xs text-gray-400 mt-1">{data.description.length} characters</p>
      </div>
    </div>
  )
}
