function parseBold(text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    return <span key={i}>{part}</span>
  })
}

function highlightKeywords(text, keywords) {
  if (!keywords || keywords.length === 0) return text
  const sorted = [...keywords].sort((a, b) => b.length - a.length)
  const pattern = new RegExp(`(${sorted.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'gi')
  const parts = text.split(pattern)
  return parts.map((part, i) => {
    if (sorted.some(kw => kw.toLowerCase() === part.toLowerCase())) {
      return <strong key={i}>{part}</strong>
    }
    return <span key={i}>{part}</span>
  })
}

export default function ResumePreview({ data }) {
  if (!data) return null

  const pi = data.personal_info
  const contactParts = [pi.email, pi.phone, pi.location].filter(Boolean).join('  |  ')
  const urlParts = [pi.linkedin_url, pi.github_url, pi.portfolio_url].filter(Boolean).join('  |  ')

  return (
    <div className="border border-gray-300 bg-white p-8 max-w-[8.5in] mx-auto" style={{ fontFamily: "'Noto Sans', sans-serif" }}>
      {/* Name */}
      <h1 style={{ fontSize: '28pt', color: '#1F4E79', lineHeight: 1, marginBottom: '2pt' }}>
        {pi.full_name}
      </h1>

      {/* Title */}
      <div style={{ fontSize: '14pt', color: '#5A5A5A', marginBottom: '6pt' }}>
        {pi.title}
      </div>

      {/* Contact */}
      <div style={{ fontFamily: 'Verdana, sans-serif', fontSize: '10pt', marginBottom: '2pt' }}>
        {contactParts}
      </div>
      {urlParts && (
        <div style={{ fontFamily: 'Verdana, sans-serif', fontSize: '10pt', marginBottom: '8pt' }}>
          {urlParts}
        </div>
      )}

      {/* Profile */}
      <SectionHeader>Profile</SectionHeader>
      <p style={{ fontSize: '10.5pt', marginBottom: '4pt' }}>
        {parseBold(data.summary)}
      </p>

      {/* Skills */}
      <SectionHeader>Skills</SectionHeader>
      {Object.entries(data.skills).map(([category, skills]) => (
        <div key={category}>
          <div style={{ fontFamily: "'Merriweather', serif", fontSize: '12pt', fontWeight: 'bold', marginTop: '4pt' }}>
            {category}
          </div>
          <div style={{ fontSize: '10.5pt', marginBottom: '2pt' }}>
            {skills.join(', ')}
          </div>
        </div>
      ))}

      {/* Work Experience */}
      <SectionHeader>Work Experience</SectionHeader>
      {data.experiences.map((exp, i) => (
        <div key={i}>
          <div style={{ fontFamily: "'Merriweather', serif", fontSize: '12pt', fontWeight: 'bold', marginTop: '8pt' }}>
            {exp.role}, {exp.company_name}
          </div>
          <div style={{ fontSize: '11pt', color: '#595959', margin: '2pt 0' }}>
            {exp.period} | {exp.location}
          </div>
          <ul style={{ paddingLeft: '24pt', margin: '2pt 0 4pt 0' }}>
            {exp.bullets.map((bullet, j) => (
              <li key={j} style={{ fontSize: '10.5pt', marginBottom: '2pt' }}>
                {highlightKeywords(bullet.text, bullet.bold_keywords)}
              </li>
            ))}
          </ul>
        </div>
      ))}

      {/* Education */}
      <SectionHeader>Education</SectionHeader>
      {data.education.map((edu, i) => (
        <div key={i}>
          <div style={{ fontFamily: "'Merriweather', serif", fontSize: '12pt', fontWeight: 'bold', marginTop: '8pt' }}>
            {edu.degree}, {edu.institution}
          </div>
          <div style={{ fontSize: '11pt', color: '#595959', margin: '2pt 0' }}>
            {edu.start_date} – {edu.end_date} | {edu.location}
          </div>
          {edu.description && (
            <p style={{ fontSize: '10.5pt', marginBottom: '4pt' }}>{edu.description}</p>
          )}
        </div>
      ))}
    </div>
  )
}

function SectionHeader({ children }) {
  return (
    <div style={{
      fontSize: '16pt',
      color: '#1F4E79',
      textTransform: 'uppercase',
      borderBottom: '1px solid #1F4E79',
      paddingBottom: '2pt',
      marginTop: '12pt',
      marginBottom: '4pt',
      fontFamily: "'Noto Sans', sans-serif",
    }}>
      {children}
    </div>
  )
}
