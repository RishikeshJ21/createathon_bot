import React from 'react';
import useSWR from 'swr';
import type { User, Instagram, Youtube } from '../types';

function Users() {
  const { data: users } = useSWR<User[]>('/users');
  const { data: instagram } = useSWR<Instagram[]>('/instagram');
  const { data: youtube } = useSWR<Youtube[]>('/youtube');

  const getUserDetails = (user: User) => {
    const instaProfile = instagram?.find(i => i.insta_id === user.insta_id);
    const youtubeProfile = youtube?.find(y => y.youtube_id === user.youtube_id);
    return { instaProfile, youtubeProfile };
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Users</h1>
      
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Instagram
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                YouTube
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Joined
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users?.map(user => {
              const { instaProfile, youtubeProfile } = getUserDetails(user);
              return (
                <tr key={user.user_id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{user.first_name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {instaProfile && (
                      <div className="text-sm text-gray-900">
                        @{instaProfile.username}
                        <div className="text-xs text-gray-500">
                          {instaProfile.followers.toLocaleString()} followers
                        </div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {youtubeProfile && (
                      <div className="text-sm text-gray-900">
                        {youtubeProfile.channel_name}
                        <div className="text-xs text-gray-500">
                          {youtubeProfile.subscribers.toLocaleString()} subscribers
                        </div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(user.timestamp).toLocaleDateString()}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Users;