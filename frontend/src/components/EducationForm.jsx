const EMPTY = { institution: '', degree: '', location: '', start_date: '', end_date: '', description: '' }

export default function EducationForm({ education, onChange }) {
  const update = (index, key, value) => {
    const updated = education.map((edu, i) => (i === index ? { ...edu, [key]: value } : edu))
    onChange(updated)
  }

  const add = () => onChange([...education, { ...EMPTY }])
  const remove = (index) => onChange(education.filter((_, i) => i !== index))

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Education</h2>

      {education.map((edu, i) => (
        <div key={i} className="border border-gray-200 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-medium text-gray-700">Education {i + 1}</h3>
            {education.length > 1 && (
              <button onClick={() => remove(i)} className="text-red-500 hover:text-red-700 text-sm">
                Remove
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Institution <span className="text-red-500">*</span></label>
              <input
                value={edu.institution}
                onChange={(e) => update(i, 'institution', e.target.value)}
                placeholder="Princeton University"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Degree <span className="text-red-500">*</span></label>
              <input
                value={edu.degree}
                onChange={(e) => update(i, 'degree', e.target.value)}
                placeholder="Bachelor's Degree in Computer Science"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location <span className="text-red-500">*</span></label>
              <input
                value={edu.location}
                onChange={(e) => update(i, 'location', e.target.value)}
                placeholder="Princeton, NJ"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Start Date <span className="text-red-500">*</span></label>
                <input
                  value={edu.start_date}
                  onChange={(e) => update(i, 'start_date', e.target.value)}
                  placeholder="09/2016"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">End Date <span className="text-red-500">*</span></label>
                <input
                  value={edu.end_date}
                  onChange={(e) => update(i, 'end_date', e.target.value)}
                  placeholder="05/2020"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none"
                />
              </div>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
              <textarea
                value={edu.description}
                onChange={(e) => update(i, 'description', e.target.value)}
                placeholder="Relevant coursework, honors, etc."
                rows={2}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none resize-y"
              />
            </div>
          </div>
        </div>
      ))}

      <button
        onClick={add}
        className="w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-[#1F4E79] hover:text-[#1F4E79] transition-colors"
      >
        + Add Education
      </button>
    </div>
  )
}
