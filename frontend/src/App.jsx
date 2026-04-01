import { useState, useEffect } from 'react'
import PersonalInfoForm from './components/PersonalInfoForm'
import ExperienceForm from './components/ExperienceForm'
import EducationForm from './components/EducationForm'
import JobDescriptionForm from './components/JobDescriptionForm'
import ResumePreview from './components/ResumePreview'
import SkillsPreview from './components/SkillsPreview'
import ExportButtons from './components/ExportButtons'
import ProfileSelector from './components/ProfileSelector'
import SaveProfileDialog from './components/SaveProfileDialog'

const STEPS = ['Personal Info', 'Experience', 'Education', 'Job Description', 'Preview & Export']

const EMPTY_PERSONAL = {
  full_name: '', title: '', email: '', phone: '',
  location: '', linkedin_url: '', portfolio_url: '', github_url: '',
}
const EMPTY_EXP = [{ company_name: '', role: '', location: '', start_date: '', end_date: '', company_url: '' }]
const EMPTY_EDU = [{ institution: '', degree: '', location: '', start_date: '', end_date: '', description: '' }]

function App() {
  const [step, setStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showSaveDialog, setShowSaveDialog] = useState(false)
  const [profiles, setProfiles] = useState([])
  const [selectedProfileId, setSelectedProfileId] = useState(null)

  const [personalInfo, setPersonalInfo] = useState({ ...EMPTY_PERSONAL })
  const [experiences, setExperiences] = useState([...EMPTY_EXP])
  const [education, setEducation] = useState([...EMPTY_EDU])

  const [jobDescription, setJobDescription] = useState({
    company_name: '', company_url: '', job_title: '', description: '',
  })

  const [analysisResult, setAnalysisResult] = useState(null)
  const [resumeResult, setResumeResult] = useState(null)

  // Load profiles on mount
  useEffect(() => {
    fetchProfiles()
  }, [])

  const fetchProfiles = async () => {
    try {
      const res = await fetch('/api/profiles')
      if (res.ok) setProfiles(await res.json())
    } catch {}
  }

  const handleProfileSelect = async (profileId) => {
    if (!profileId) {
      // "Start from scratch"
      setSelectedProfileId(null)
      setPersonalInfo({ ...EMPTY_PERSONAL })
      setExperiences(EMPTY_EXP.map(e => ({ ...e })))
      setEducation(EMPTY_EDU.map(e => ({ ...e })))
      setStep(0)
      return
    }
    try {
      const res = await fetch(`/api/profiles/${profileId}`)
      if (!res.ok) throw new Error('Failed to load profile')
      const data = await res.json()
      setSelectedProfileId(profileId)
      setPersonalInfo(data.personal_info)
      setExperiences(data.experiences)
      setEducation(data.education)
      setStep(0)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleSaveProfile = async () => {
    try {
      const res = await fetch('/api/profiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ personal_info: personalInfo, experiences, education }),
      })
      if (!res.ok) throw new Error('Failed to save profile')
      const saved = await res.json()
      setSelectedProfileId(saved.id)
      await fetchProfiles()
      setShowSaveDialog(false)
    } catch (err) {
      setError(err.message)
    }
  }

  const next = () => setStep((s) => Math.min(s + 1, STEPS.length - 1))
  const prev = () => setStep((s) => Math.max(s - 1, 0))

  const handleAnalyzeAndGenerate = async () => {
    setLoading(true)
    setError(null)
    try {
      const analyzeRes = await fetch('/api/analyze-job', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jobDescription, experiences }),
      })
      if (!analyzeRes.ok) {
        const err = await analyzeRes.json()
        throw new Error(err.detail || 'Failed to analyze job description')
      }
      const analysis = await analyzeRes.json()
      setAnalysisResult(analysis)

      const generateRes = await fetch('/api/generate-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personal_info: personalInfo, experiences, education,
          job_description: jobDescription, extracted_skills: analysis.extracted_skills,
        }),
      })
      if (!generateRes.ok) {
        const err = await generateRes.json()
        throw new Error(err.detail || 'Failed to generate resume')
      }
      const resume = await generateRes.json()
      setResumeResult(resume)
      next()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Show save dialog when moving from Education (step 2) to Job Description (step 3)
  const handleNextFromEducation = () => {
    if (!selectedProfileId && personalInfo.full_name) {
      setShowSaveDialog(true)
    } else {
      next()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-[#1F4E79] text-white py-6 shadow-lg">
        <div className="max-w-4xl mx-auto px-6">
          <h1 className="text-2xl font-bold">ATS Resume Generator</h1>
          <p className="text-blue-200 mt-1">Generate tailored, ATS-friendly resumes</p>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-4">
        {/* Profile selector */}
        <ProfileSelector
          profiles={profiles}
          selectedId={selectedProfileId}
          onSelect={handleProfileSelect}
        />

        {/* Step indicator */}
        <div className="flex items-center gap-2 mb-6 overflow-x-auto">
          {STEPS.map((label, i) => (
            <button
              key={label}
              onClick={() => {
                if (i < step || (i === STEPS.length - 1 && resumeResult)) setStep(i)
              }}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                i === step
                  ? 'bg-[#1F4E79] text-white'
                  : i < step
                  ? 'bg-[#1F4E79]/10 text-[#1F4E79] cursor-pointer hover:bg-[#1F4E79]/20'
                  : 'bg-gray-200 text-gray-500'
              }`}
            >
              <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                i === step ? 'bg-white text-[#1F4E79]' : i < step ? 'bg-[#1F4E79] text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                {i < step ? '✓' : i + 1}
              </span>
              {label}
            </button>
          ))}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
            <button onClick={() => setError(null)} className="ml-2 font-bold">×</button>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          {step === 0 && <PersonalInfoForm data={personalInfo} onChange={setPersonalInfo} />}
          {step === 1 && <ExperienceForm experiences={experiences} onChange={setExperiences} />}
          {step === 2 && <EducationForm education={education} onChange={setEducation} />}
          {step === 3 && <JobDescriptionForm data={jobDescription} onChange={setJobDescription} />}
          {step === 4 && resumeResult && (
            <div>
              {analysisResult && <SkillsPreview analysis={analysisResult} />}
              <ResumePreview data={resumeResult} />
              <ExportButtons filename={resumeResult.filename} />
            </div>
          )}
        </div>

        <div className="flex justify-between mt-6">
          <button
            onClick={prev}
            disabled={step === 0}
            className="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Back
          </button>
          {step < 2 && (
            <button onClick={next}
              className="px-6 py-2 rounded-lg bg-[#1F4E79] text-white hover:bg-[#163a5c] transition-colors">
              Next
            </button>
          )}
          {step === 2 && (
            <button onClick={handleNextFromEducation}
              className="px-6 py-2 rounded-lg bg-[#1F4E79] text-white hover:bg-[#163a5c] transition-colors">
              Next
            </button>
          )}
          {step === 3 && (
            <button onClick={handleAnalyzeAndGenerate} disabled={loading}
              className="px-6 py-2 rounded-lg bg-[#1F4E79] text-white hover:bg-[#163a5c] transition-colors disabled:opacity-60">
              {loading ? 'Generating Resume...' : 'Generate Resume'}
            </button>
          )}
        </div>
      </div>

      {/* Save profile dialog */}
      {showSaveDialog && (
        <SaveProfileDialog
          name={personalInfo.full_name}
          onSave={() => { handleSaveProfile(); next() }}
          onSkip={() => { setShowSaveDialog(false); next() }}
          onCancel={() => setShowSaveDialog(false)}
        />
      )}
    </div>
  )
}

export default App
