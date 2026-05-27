import axios from 'axios'

declare const process: {
  env: {
    NEXT_PUBLIC_API_URL?: string
  }
}

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
})

// Attach JWT to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const scanUrl = (url: string) =>
  api.post('/api/v1/scan/url', { url }).then(r => r.data)

export const scanContract = (address: string) =>
  api.post('/api/v1/scan/contract', { address }).then(r => r.data)

export const scanWallet = (address: string) =>
  api.post('/api/v1/scan/wallet', { address }).then(r => r.data)

export const login = (email: string, password: string) =>
  api.post('/auth/login', { email, password }).then(r => r.data)

export const register = (email: string, password: string) =>
  api.post('/auth/register', { email, password }).then(r => r.data)

export default api