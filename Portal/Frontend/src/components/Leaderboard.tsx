import React from 'react';
import useSWR from 'swr';
import { Trophy, Award, Medal } from 'lucide-react';
import type { User, Progress, Winner } from '../types';

function Leaderboard() {
  const { data: users } = useSWR<User[]>('/users');
  const { data: progress } = useSWR<Progress[]>('/progress');
  const { data: winners } = useSWR<Winner[]>('/winners');

  const getUserStats = () => {
    if (!users || !progress || !winners) return [];

    return users.map(user => {
      const completions = progress.filter(p => p.user_id === user.user_id && p.submit).length;
      const wins = winners.filter(w => w.user_id === user.user_id).length;
      
      return {
        ...user,
        completions,
        wins,
        score: completions * 10 + wins * 50,
      };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
  };

  const leaderboard = getUserStats();

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Leaderboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center">
            <Trophy className="w-6 h-6 mr-2 text-yellow-500" />
            Top Performers
          </h2>
          
          <div className="space-y-4">
            {leaderboard.map((user, index) => (
              <div key={user.user_id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <span className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-200 mr-4">
                    {index + 1}
                  </span>
                  <div>
                    <h3 className="font-medium">{user.first_name}</h3>
                    <p className="text-sm text-gray-500">Score: {user.score}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    <Award className="w-5 h-5 text-blue-500 mr-1" />
                    <span>{user.completions}</span>
                  </div>
                  <div className="flex items-center">
                    <Medal className="w-5 h-5 text-yellow-500 mr-1" />
                    <span>{user.wins}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-6">Statistics</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Total Completions</h3>
              <p className="text-3xl font-bold">
                {progress?.filter(p => p.submit).length || 0}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Active Users</h3>
              <p className="text-3xl font-bold">
                {users?.length || 0}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Winners Declared</h3>
              <p className="text-3xl font-bold">
                {winners?.length || 0}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;