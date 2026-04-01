export default function SaveProfileDialog({ name, onSave, onSkip, onCancel }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl p-6 max-w-md w-full mx-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Save Profile?</h3>
        <p className="text-gray-600 mb-6">
          Save <strong>{name}</strong>'s information as a profile so you can reuse it next time?
        </p>
        <div className="flex gap-3 justify-end">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            onClick={onSkip}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100"
          >
            Don't Save
          </button>
          <button
            onClick={onSave}
            className="px-4 py-2 bg-[#1F4E79] text-white rounded-lg hover:bg-[#163a5c] transition-colors"
          >
            Save Profile
          </button>
        </div>
      </div>
    </div>
  )
}
