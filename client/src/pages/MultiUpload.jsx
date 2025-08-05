import React, { useState } from 'react';
import axios from 'axios';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const MultiUpload = ({ theme }) => {
  const [numFiles, setNumFiles] = useState(1);
  const [files, setFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const isDark = theme === 'dark';

  const handleFileChange = (e, index) => {
    const newFiles = [...files];
    newFiles[index] = e.target.files[0];
    setFiles(newFiles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobDescription || files.length !== numFiles || files.includes(undefined)) {
      alert("Please provide job description and all resume files.");
      return;
    }

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    files.forEach((file, index) => formData.append(`resume${index + 1}`, file));

    try {
      setLoading(true);
      const res = await axios.post('http://localhost:5000/analyze-multiple', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResults(res.data.results);
    } catch (error) {
      console.error(error);
      alert("Error analyzing resumes.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen px-6 py-10 flex flex-col items-center justify-start transition-all ${
        isDark
          ? 'bg-gradient-to-br from-black via-zinc-900 to-gray-900 text-white'
          : 'bg-gradient-to-br from-white via-gray-50 to-slate-100 text-gray-900'
      }`}
    >
      <button
        onClick={() => navigate('/')}
        className="absolute top-4 left-6 flex items-center gap-2 text-sm hover:underline"
      >
        <ArrowLeft size={18} /> Back
      </button>

      <h1 className="text-4xl font-bold mb-10 text-center">Multiple Resume Upload</h1>

      <form onSubmit={handleSubmit} className="w-full max-w-2xl space-y-6">
        <div className="text-center">
          <label className="block mb-2 font-semibold text-lg">Enter number of resumes:</label>
          <input
            type="number"
            value={numFiles}
            min={1}
            max={10}
            onChange={(e) => {
              const count = parseInt(e.target.value);
              setNumFiles(count);
              setFiles(new Array(count).fill(undefined));
            }}
            className={`w-24 mx-auto px-3 py-2 rounded border text-center outline-none focus:ring-2 ${
              isDark
                ? 'bg-zinc-800 text-white border-zinc-600 focus:ring-purple-500'
                : 'bg-white text-gray-800 border-gray-300 focus:ring-purple-600'
            } cursor-text`}
          />
        </div>

        {[...Array(numFiles)].map((_, i) => (
          <div key={i} className="text-center">
            <label className="block mb-2">Resume {i + 1}</label>
            <input
              type="file"
              accept=".pdf,.doc,.docx,.txt"
              onChange={(e) => handleFileChange(e, i)}
              required
              className={`w-full md:w-3/4 mx-auto px-3 py-2 border rounded outline-none focus:ring-2 ${
                isDark
                  ? 'bg-zinc-800 text-white border-zinc-600 focus:ring-purple-500'
                  : 'bg-white text-gray-800 border-gray-300 focus:ring-purple-600'
              } cursor-pointer`}
            />
          </div>
        ))}

        <div className="text-center">
          <label className="block mb-2 font-semibold">Paste Job Description:</label>
          <textarea
            rows="6"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            required
            className={`w-full md:w-3/4 mx-auto px-4 py-3 border rounded shadow-md outline-none focus:ring-2 ${
              isDark
                ? 'bg-zinc-800 text-white border-zinc-600 focus:ring-purple-500'
                : 'bg-white text-gray-800 border-gray-300 focus:ring-purple-600'
            } cursor-text`}
          />
        </div>

        <div className="text-center">
          <button
            type="submit"
            className="bg-gradient-to-r from-purple-600 via-pink-500 to-red-500 hover:brightness-110 text-white font-bold px-8 py-3 rounded-full shadow-lg transform hover:scale-105 transition duration-300"
          >
            Analyze Resumes
          </button>
        </div>
      </form>

      {loading && (
        <div className="mt-8 text-lg animate-pulse">Analyzing resumes...</div>
      )}

      {results.length > 0 && !loading && (
        <div className="mt-10 w-full max-w-3xl">
          <h2 className="text-2xl font-bold mb-4 text-center">Sorted Results</h2>
          <div className="space-y-4">
            {results.map((res, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white rounded-xl px-6 py-4 shadow-xl flex justify-between items-center"
              >
                <span className="font-medium truncate w-2/3">{res.filename}</span>
                <span className="text-xl font-bold">{res.score}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MultiUpload;
