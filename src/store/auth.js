import { reactive } from 'vue'
import axios from 'axios'

const LOCAL_STORAGE_KEY = 'admin_token'
const API_BASE = 'http://127.0.0.1:8000'

const state = reactive({
  token: localStorage.getItem(LOCAL_STORAGE_KEY) || '',
  error: '',
  loading: false,
})

function isAuthenticated() {
  return Boolean(state.token)
}

function setAuthHeader(token) {
  axios.defaults.headers.common.Authorization = token ? `Bearer ${token}` : ''
}

async function login(username, password) {
  state.loading = true
  state.error = ''

  try {
    const response = await axios.post(`${API_BASE}/admin/login`, {
      username,
      password,
    })

    if (response.data?.token) {
      state.token = response.data.token
      localStorage.setItem(LOCAL_STORAGE_KEY, state.token)
      setAuthHeader(state.token)
      return true
    }

    state.error = 'Login failed. Please try again.'
    return false
  } catch (error) {
    state.error = error.response?.data?.detail || error.message || 'Invalid credentials.'
    return false
  } finally {
    state.loading = false
  }
}

function logout() {
  state.token = ''
  localStorage.removeItem(LOCAL_STORAGE_KEY)
  setAuthHeader('')
}

if (state.token) {
  setAuthHeader(state.token)
}

export default {
  state,
  login,
  logout,
  isAuthenticated,
}
