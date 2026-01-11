import apiClient from './apiService';

export const userService = {
  getUsers: () => apiClient.get('/users'),
  getUserById: (id: string) => apiClient.get(`/users/${id}`),
  createUser: (data: any) => apiClient.post('/users', data),
};