import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = ({ theme }) => {
  const navigate = useNavigate();

  const isDark = theme === 'dark';

  return (
    <div
      className={`h-screen flex items-center justify-center transition-all duration-300 ${
        isDark
          ? 'bg-gradient-to-br from-black via-zinc-900 to-gray-900'
          : 'bg-gradient-to-br from-white via-gray-100 to-slate-100'
      }`}
    >
      <div className="text-center">
        <h1 className={`text-4xl md:text-6xl font-bold mb-10 ${isDark ? 'text-white' : 'text-gray-900'}`}>
          ⚡ ATS Resume Analyzer
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            onClick={() => navigate('/single')}
            className={`p-8 rounded-2xl shadow-md cursor-pointer hover:scale-105 transition-all ${
              isDark
                ? 'bg-white bg-opacity-5 border border-gray-700 text-white'
                : 'bg-white border border-gray-300 text-gray-900'
            }`}
          >
            <h2 className="text-2xl font-semibold mb-2">Single Resume Upload</h2>
            <p>Upload one resume and job description to get score + missing keywords.</p>
          </div>
          <div
            onClick={() => navigate('/multiple')}
            className={`p-8 rounded-2xl shadow-md cursor-pointer hover:scale-105 transition-all ${
              isDark
                ? 'bg-white bg-opacity-5 border border-gray-700 text-white'
                : 'bg-white border border-gray-300 text-gray-900'
            }`}
          >
            <h2 className="text-2xl font-semibold mb-2">Multiple Resume Uploads</h2>
            <p>Upload multiple resumes and compare scores for each.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
