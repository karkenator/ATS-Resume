const EMPTY = { company_name: '', role: '', location: '', start_date: '', end_date: '', company_url: '' }

export default function ExperienceForm({ experiences, onChange }) {
  const update = (index, key, value) => {
    const updated = experiences.map((exp, i) => (i === index ? { ...exp, [key]: value } : exp))
    onChange(updated)
  }

  const add = () => onChange([...experiences, { ...EMPTY }])
  const remove = (index) => onChange(experiences.filter((_, i) => i !== index))

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Work Experience</h2>
      <p className="text-sm text-gray-500 mb-4">Add your work experience, most recent first. The most recent role will have the most bullet points on the resume.</p>

      {experiences.map((exp, i) => (
        <div key={i} className="border border-gray-200 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-medium text-gray-700">Experience {i + 1}</h3>
            {experiences.length > 1 && (
              <button onClick={() => remove(i)} className="text-red-500 hover:text-red-700 text-sm">
                Remove
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company Name <span className="text-red-500">*</span></label>
              <input
                value={exp.company_name}
                onChange={(e) => update(i, 'company_name', e.target.value)}
                placeholder="Google"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Role <span className="text-red-500">*</span></label>
              <input
                value={exp.role}
                onChange={(e) => update(i, 'role', e.target.value)}
                placeholder="Senior Software Engineer"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location <span className="text-red-500">*</span></label>
              <input
                value={exp.location}
                onChange={(e) => update(i, 'location', e.target.value)}
                placeholder="San Francisco, CA"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company URL</label>
              <input
                value={exp.company_url}
                onChange={(e) => update(i, 'company_url', e.target.value)}
                placeholder="https://google.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date <span className="text-red-500">*</span></label>
              <input
                value={exp.start_date}
                onChange={(e) => update(i, 'start_date', e.target.value)}
                placeholder="01/2021"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date <span className="text-red-500">*</span></label>
              <input
                value={exp.end_date}
                onChange={(e) => update(i, 'end_date', e.target.value)}
                placeholder="Present"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
          </div>
        </div>
      ))}

      <button
        onClick={add}
        className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-[#1F4E79] hover:text-[#1F4E79] transition-colors"
      >
        + Add Experience
      </button>
    </div>
  )
}
