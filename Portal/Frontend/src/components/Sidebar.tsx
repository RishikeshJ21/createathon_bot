import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Trophy, Users, Flag } from 'lucide-react';

function Sidebar() {
  const links = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/challenges', icon: Flag, label: 'Challenges' },
    { to: '/users', icon: Users, label: 'Users' },
    { to: '/leaderboard', icon: Trophy, label: 'Leaderboard' },
  ];

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-gray-800">Admin Panel</h1>
      </div>
      <nav className="mt-6">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${
                isActive ? 'bg-gray-100 border-r-4 border-indigo-500' : ''
              }`
            }
          >
            <Icon className="w-5 h-5 mr-3" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;