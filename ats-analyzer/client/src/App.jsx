// import React, { useState } from 'react';
// import axios from 'axios';

// const App = () => {
//   const [resumeFile, setResumeFile] = useState(null);
//   const [jobDescription, setJobDescription] = useState('');
//   const [result, setResult] = useState(null);
//   const [fileKey, setFileKey] = useState(Date.now()); // Used to reset file input

//   const handleFileChange = (e) => {
//     setResumeFile(e.target.files[0]);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!resumeFile || !jobDescription) {
//       alert("Both resume and job description are required.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append('resume', resumeFile);
//     formData.append('job_description', jobDescription);

//     try {
//       const response = await axios.post('http://localhost:5000/analyze', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });
//       setResult(response.data);

//       // Reset form after successful submission
//       setResumeFile(null);
//       // setJobDescription('');
//       setFileKey(Date.now()); // Force file input to reset
//     } catch (error) {
//       console.error('Error submitting form:', error);
//       alert("Failed to analyze resume. See console for details.");
//     }
//   };

//   return (
//     <div className="p-6 max-w-xl mx-auto">
//       <h1 className="text-2xl font-bold mb-4">ATS Resume Analyzer</h1>
//       <form onSubmit={handleSubmit} className="space-y-4">
//         <div>
//           <label className="block font-medium">Upload Resume:</label>
//           <input
//             key={fileKey}
//             type="file"
//             accept=".pdf,.doc,.docx,.txt"
//             onChange={handleFileChange}
//             required
//           />
//         </div>
//         <div>
//           <label className="block font-medium">Paste Job Description:</label>
//           <textarea
//             value={jobDescription}
//             onChange={(e) => setJobDescription(e.target.value)}
//             rows="6"
//             className="w-full border rounded p-2"
//             required
//           />
//         </div>
//         <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
//           Analyze
//         </button>
//       </form>

//       {result && (
//         <div className="mt-6 p-4 border rounded bg-gray-100">
//           <h2 className="text-lg font-semibold">Results:</h2>
//           <p><strong>Gemini Score:</strong> {result.gemini_score}%</p>
//         </div>
//       )}
//     </div>
//   );
// };

// export default App;
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import SingleUpload from './pages/SingleUpload';
import MultiUpload from './pages/MultiUpload';
import { Sun, Moon } from 'lucide-react';

const App = () => {
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <div className={theme === 'dark' ? 'bg-black text-white min-h-screen' : 'bg-white text-gray-900 min-h-screen'}>
      {/* Top-right Theme Toggle Button */}
      <div className="absolute top-4 right-6 z-50">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full border hover:scale-110 transition duration-300 shadow-md 
            bg-white text-black border-gray-300"
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? <Sun size={22} /> : <Moon size={22} />}
        </button>
      </div>

      <Router>
        <Routes>
          <Route path="/" element={<Home theme={theme} />} />
          <Route path="/single" element={<SingleUpload theme={theme} />} />
          <Route path="/multiple" element={<MultiUpload theme={theme} />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
