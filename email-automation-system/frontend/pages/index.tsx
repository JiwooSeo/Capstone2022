import React, { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    setIsLoggedIn(!!token)
  }, [])

  const handleGoogleLogin = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/google-oauth`)
      const data = await response.json()
      window.location.href = data.auth_url
    } catch (error) {
      console.error('Failed to start OAuth:', error)
    }
  }

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Email Automation
          </h1>
          <p className="text-gray-600 mb-8">
            Intelligent email scheduling and task management powered by AI
          </p>

          <button
            onClick={handleGoogleLogin}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition mb-4"
          >
            Sign in with Google
          </button>

          <div className="text-gray-600 text-sm">
            <h3 className="font-semibold mb-2">Features:</h3>
            <ul className="list-disc list-inside space-y-1">
              <li>Hourly email analysis</li>
              <li>AI-powered task extraction</li>
              <li>Intelligent scheduling</li>
              <li>Meeting and deadline tracking</li>
            </ul>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Email Automation</h1>
          <div className="space-x-4">
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link href="/calendar" className="text-gray-600 hover:text-gray-900">
              Calendar
            </Link>
            <Link href="/settings" className="text-gray-600 hover:text-gray-900">
              Settings
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-2">
              Total Emails
            </h2>
            <p className="text-3xl font-bold text-blue-600">--</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-2">
              Upcoming Meetings
            </h2>
            <p className="text-3xl font-bold text-green-600">--</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-2">
              Action Items
            </h2>
            <p className="text-3xl font-bold text-orange-600">--</p>
          </div>
        </div>
      </div>
    </div>
  )
}
