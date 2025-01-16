import React from 'react';
import useSWR from 'swr';
import { Users as UsersIcon, Trophy, Flag, Activity } from 'lucide-react';
import type { User, Challenge, Progress } from '../types';

function StatCard({ icon: Icon, label, value, className }: any) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-full ${className}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className="ml-4">
          <p className="text-sm text-gray-500">{label}</p>
          <h3 className="text-2xl font-semibold">{value}</h3>
        </div>
      </div>
    </div>
  );
}

function Dashboard() {
  const { data: users } = useSWR<User[]>('/users');
  const { data: challenges } = useSWR<Challenge[]>('/challenges');
  const { data: progress } = useSWR<Progress[]>('/progress');

  const activeUsers = users?.length || 0;
  const totalChallenges = challenges?.length || 0;
  const ongoingChallenges = challenges?.filter(c => new Date(c.timestamp) > new Date()).length || 0;
  const completions = progress?.filter(p => p.submit).length || 0;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={UsersIcon}
          label="Total Users"
          value={activeUsers}
          className="bg-blue-500"
        />
        <StatCard
          icon={Flag}
          label="Total Challenges"
          value={totalChallenges}
          className="bg-green-500"
        />
        <StatCard
          icon={Activity}
          label="Ongoing Challenges"
          value={ongoingChallenges}
          className="bg-yellow-500"
        />
        <StatCard
          icon={Trophy}
          label="Total Completions"
          value={completions}
          className="bg-purple-500"
        />
      </div>

      <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Challenges</h2>
          <div className="space-y-4">
            {challenges?.slice(0, 5).map(challenge => (
              <div key={challenge.id} className="border-b pb-4">
                <h3 className="font-medium">{challenge.challenge_name}</h3>
                <p className="text-sm text-gray-500">Duration: {challenge.duration} days</p>
                <p className="text-sm text-gray-500">Prize: {challenge.prize}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Completions</h2>
          <div className="space-y-4">
            {progress?.filter(p => p.submit).slice(0, 5).map(p => (
              <div key={p.id} className="border-b pb-4">
                <h3 className="font-medium">{p.challenge_name}</h3>
                <p className="text-sm text-gray-500">Day {p.day}</p>
                <p className="text-sm text-gray-500">
                  Submitted: {new Date(p.submition_day).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;