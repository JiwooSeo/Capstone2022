import React, { useState, useEffect } from 'react'
import Link from 'next/link'

interface UserInfo {
  id: string
  email: string
  name: string
  is_active: boolean
}

export default function Settings() {
  const [user, setUser] = useState<UserInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    fetchUserInfo()
  }, [])

  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        window.location.href = '/'
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/user`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data)
      }
    } catch (err) {
      console.error('Failed to fetch user info:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      }
      localStorage.removeItem('access_token')
      window.location.href = '/'
    } catch (err) {
      setMessage({ type: 'error', text: 'Logout failed' })
    }
  }

  const handleRevokeAccess = async () => {
    if (!window.confirm('Revoke Gmail access? You will need to re-authenticate.')) {
      return
    }

    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/revoke-gmail-access`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        setMessage({ type: 'success', text: 'Gmail access revoked' })
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to revoke access' })
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Settings</h1>
          <div className="space-x-4">
            <Link href="/" className="text-gray-600 hover:text-gray-900">
              Home
            </Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link href="/calendar" className="text-gray-600 hover:text-gray-900">
              Calendar
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-4 py-8">
        {message && (
          <div
            className={`mb-4 p-4 rounded ${
              message.type === 'success'
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}
          >
            {message.text}
          </div>
        )}

        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h2 className="text-lg font-bold text-gray-800">Account Settings</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center text-gray-600">Loading...</div>
          ) : user ? (
            <div className="p-6 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={user.name}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded bg-gray-50 text-gray-600"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={user.email}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded bg-gray-50 text-gray-600"
                />
              </div>

              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Gmail Integration
                </h3>
                <p className="text-gray-600 mb-4">
                  Your Gmail account is connected for automated email processing.
                </p>
                <button
                  onClick={handleRevokeAccess}
                  className="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded transition"
                >
                  Revoke Gmail Access
                </button>
              </div>

              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Account Management
                </h3>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition"
                >
                  Logout
                </button>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
