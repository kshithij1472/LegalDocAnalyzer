import { createContext, useContext, useEffect, useState } from 'react'
import axios from 'axios'
import jwtDecode from 'jwt-decode'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const login = async (credentials) => {
    const { data } = await axios.post('/auth/token', credentials)
    localStorage.setItem('token', data.access_token)
    setUser(jwtDecode(data.access_token))
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        setUser(jwtDecode(token))
      } catch {
        logout()
      }
    }
    setLoading(false)
  }, [])

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)