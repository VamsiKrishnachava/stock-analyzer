import apiClient from './apiService';

export const productService = {
  getProducts: () => apiClient.get('/products'),
  getProductById: (id: string) => apiClient.get(`/products/${id}`),
  createProduct: (data: any) => apiClient.post('/products', data),
};