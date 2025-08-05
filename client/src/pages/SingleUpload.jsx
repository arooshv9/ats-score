import React, { useState } from 'react';
import axios from 'axios';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SingleUpload = ({ theme }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const isDark = theme === 'dark';

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription) {
      alert('Please upload resume and job description.');
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      setLoading(true);
      const res = await axios.post('http://localhost:5000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Error analyzing resume.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen flex items-center justify-center px-4 py-10 ${
        isDark
          ? 'bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white'
          : 'bg-gradient-to-br from-white via-gray-50 to-gray-100 text-gray-900'
      }`}
    >
      <div className="w-full max-w-3xl space-y-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-sm hover:underline"
        >
          <ArrowLeft size={18} />
          Back to Home
        </button>

        <div
          className={`p-8 rounded-2xl shadow-xl transition-all border ${
            isDark
              ? 'bg-white bg-opacity-5 backdrop-blur-sm border-gray-700'
              : 'bg-white border border-gray-300 backdrop-blur-md'
          }`}
        >
          <h1 className="text-3xl font-bold text-center mb-6">✨ ATS Resume Analyzer</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block mb-2 font-medium">Upload Resume:</label>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={handleFileChange}
                required
                className={`w-full file:px-4 file:py-2 file:border-0 file:rounded file:text-sm file:cursor-pointer
                ${
                  isDark
                    ? 'bg-gray-800 file:bg-indigo-500 file:text-white text-white'
                    : 'bg-gray-100 file:bg-blue-600 file:text-white text-gray-900'
                }`}
              />
            </div>

            <div>
              <label className="block mb-2 font-medium">Paste Job Description:</label>
              <textarea
                rows="6"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                required
                className={`w-full rounded-lg px-4 py-3 text-sm border outline-none resize-none shadow-sm ${
                  isDark
                    ? 'bg-gray-800 border-gray-700 text-white placeholder-gray-400'
                    : 'bg-white border-gray-300 text-gray-800 placeholder-gray-500'
                }`}
                placeholder="Paste the job description here..."
              />
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg shadow transition duration-300"
            >
              {loading ? (
                <span className="flex justify-center items-center gap-2 animate-pulse">
                  <Loader2 size={18} className="animate-spin" />
                  Analyzing...
                </span>
              ) : (
                'Analyze Resume'
              )}
            </button>
          </form>
        </div>

        {result && !loading && (
          <div
            className={`mt-10 p-6 rounded-2xl shadow-xl transition-all border ${
              isDark
                ? 'bg-white bg-opacity-5 backdrop-blur-sm border-gray-700'
                : 'bg-white border border-gray-300 backdrop-blur-md'
            }`}
          >
            <h2 className="text-xl font-semibold mb-4 text-center">📊 Analysis Result</h2>

            <div className="text-center mb-6">
              <p className="text-lg font-medium">
                Gemini Score:{' '}
                <span
                  className={`font-bold ${
                    result.gemini_score >= 75
                      ? 'text-green-500'
                      : result.gemini_score >= 50
                      ? 'text-yellow-500'
                      : 'text-red-500'
                  }`}
                >
                  {result.gemini_score}%
                </span>
              </p>
            </div>

            {result.missing_keywords?.length > 0 ? (
              <div>
                <p className="font-medium mb-2">Missing Keywords:</p>
                <div className="flex flex-wrap gap-3">
                  {result.missing_keywords.map((kw, idx) => (
                    <span
                      key={idx}
                      className="px-4 py-1 rounded-full text-sm font-semibold bg-pink-100 text-pink-800 shadow"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-green-400 text-center font-medium">🎉 No major keywords missing!</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SingleUpload;
