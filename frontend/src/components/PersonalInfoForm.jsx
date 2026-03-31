const FIELDS = [
  { key: 'full_name', label: 'Full Name', placeholder: 'John Doe', required: true },
  { key: 'title', label: 'Professional Title', placeholder: 'Senior Software Engineer', required: true },
  { key: 'email', label: 'Email', placeholder: 'john@example.com', type: 'email', required: true },
  { key: 'phone', label: 'Phone', placeholder: '+1 (555) 123-4567', required: true },
  { key: 'location', label: 'Location', placeholder: 'San Francisco, CA', required: true },
  { key: 'linkedin_url', label: 'LinkedIn URL', placeholder: 'https://linkedin.com/in/johndoe' },
  { key: 'portfolio_url', label: 'Portfolio URL', placeholder: 'https://johndoe.dev' },
  { key: 'github_url', label: 'GitHub URL', placeholder: 'https://github.com/johndoe' },
]

export default function PersonalInfoForm({ data, onChange }) {
  const update = (key, value) => onChange({ ...data, [key]: value })

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Personal Information</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {FIELDS.map((f) => (
          <div key={f.key} className={f.key === 'full_name' || f.key === 'title' ? 'md:col-span-2' : ''}>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {f.label} {f.required && <span className="text-red-500">*</span>}
            </label>
            <input
              type={f.type || 'text'}
              value={data[f.key]}
              onChange={(e) => update(f.key, e.target.value)}
              placeholder={f.placeholder}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1F4E79]/50 focus:border-[#1F4E79] outline-none transition-colors"
            />
          </div>
        ))}
      </div>
    </div>
  )
}
