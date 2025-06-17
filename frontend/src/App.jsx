// React + Tailwind Frontend (frontend/src/App.js)
import React, { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [jobDesc, setJobDesc] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [score, setScore] = useState(null);
  const [geminiResponse, setGeminiResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobDesc || !file) return alert("Please provide both JD and resume");

    const formData = new FormData();
    formData.append("job_desc", jobDesc);
    formData.append("resume", file);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/analyze", formData);
      setScore(res.data.score);
      setGeminiResponse(res.data.gemini_response);
    } catch (err) {
      alert("Error analyzing resume");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white shadow-lg p-6 rounded-xl">
        <h1 className="text-3xl font-bold mb-6 text-center">📊 ATS Resume Analyzer</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring"
            rows="6"
            placeholder="Paste Job Description Here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
          ></textarea>
          <input
            type="file"
            accept=".pdf,.docx"
            className="block w-full p-2 border rounded-lg"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>

        {score !== null && (
          <div className="mt-6 bg-green-50 p-4 rounded-lg">
            <h2 className="text-xl font-semibold">Fine-Tuned Model Score: {score}/100</h2>
            <div className="w-full bg-gray-200 rounded-full h-4 mt-2">
              <div className="bg-green-500 h-4 rounded-full" style={{ width: `${score}%` }}></div>
            </div>
          </div>
        )}

        {geminiResponse && (
          <div className="mt-6 bg-purple-50 p-4 rounded-lg">
            <h2 className="text-xl font-semibold">Gemini Response:</h2>
            <p className="mt-2 text-gray-800 whitespace-pre-line">{geminiResponse}</p>
          </div>
        )}
      </div>
    </div>
  );
}
