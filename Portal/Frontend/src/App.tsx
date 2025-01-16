import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SWRConfig } from 'swr';
import { fetcher } from './lib/api';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import Challenges from './components/Challenges';
import Users from './components/Users';
import Leaderboard from './components/Leaderboard';

function App() {
  return (
    <SWRConfig value={{ fetcher }}>
      <Router>
        <div className="flex h-screen bg-gray-100">
          <Sidebar />
          <div className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/challenges" element={<Challenges />} />
              <Route path="/users" element={<Users />} />
              <Route path="/leaderboard" element={<Leaderboard />} />
            </Routes>
          </div>
        </div>
      </Router>
    </SWRConfig>
  );
}

export default App;