import React, { useState } from 'react';
import useSWR, { mutate } from 'swr';
import { Plus } from 'lucide-react';
import type { Challenge } from '../types';
import { createChallenge } from '../lib/api';

function Challenges() {
  const { data: challenges } = useSWR<Challenge[]>('/challenges');
  const [isCreating, setIsCreating] = useState(false);
  const [newChallenge, setNewChallenge] = useState({
    challenge_name: '',
    task: '',
    duration: 0,
    prize: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createChallenge(newChallenge);
      setIsCreating(false);
      setNewChallenge({ challenge_name: '', task: '', duration: 0, prize: '' });
      mutate('/challenges');
    } catch (error) {
      console.error('Failed to create challenge:', error);
    }
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Challenges</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          <Plus className="w-5 h-5 mr-2" />
          New Challenge
        </button>
      </div>

      {isCreating && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full">
            <h2 className="text-2xl font-bold mb-6">Create New Challenge</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  value={newChallenge.challenge_name}
                  onChange={e => setNewChallenge(prev => ({ ...prev, challenge_name: e.target.value }))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Task</label>
                <textarea
                  value={newChallenge.task}
                  onChange={e => setNewChallenge(prev => ({ ...prev, task: e.target.value }))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Duration (days)</label>
                <input
                  type="number"
                  value={newChallenge.duration}
                  onChange={e => setNewChallenge(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Prize</label>
                <input
                  type="text"
                  value={newChallenge.prize}
                  onChange={e => setNewChallenge(prev => ({ ...prev, prize: e.target.value }))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setIsCreating(false)}
                  className="px-4 py-2 text-gray-700 hover:text-gray-900"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                >
                  Create Challenge
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {challenges?.map(challenge => (
          <div key={challenge.id} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold mb-2">{challenge.challenge_name}</h3>
            <p className="text-gray-600 mb-4">{challenge.task}</p>
            <div className="flex justify-between text-sm text-gray-500">
              <span>Duration: {challenge.duration} days</span>
              <span>Prize: {challenge.prize}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Challenges;