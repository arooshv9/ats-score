
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
