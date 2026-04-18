import React, { useEffect, useState } from 'react'
import Link from 'next/link'

interface DashboardData {
  total_emails: number
  total_events: number
  meetings: number
  deadlines: number
  action_items: number
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        window.location.href = '/'
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/events/summary/stats`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const result = await response.json()
        setData({
          total_emails: 0,
          total_events: result.total_events || 0,
          meetings: result.by_type?.meeting || 0,
          deadlines: result.by_type?.deadline || 0,
          action_items: result.by_type?.action_item || 0,
        })
      } else {
        setError('Failed to fetch dashboard data')
      }
    } catch (err) {
      setError('Error loading dashboard')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
          <div className="space-x-4">
            <Link href="/" className="text-gray-600 hover:text-gray-900">
              Home
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
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Events</h3>
              <p className="text-3xl font-bold text-blue-600">{data.total_events}</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Meetings</h3>
              <p className="text-3xl font-bold text-green-600">{data.meetings}</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Deadlines</h3>
              <p className="text-3xl font-bold text-red-600">{data.deadlines}</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Action Items</h3>
              <p className="text-3xl font-bold text-orange-600">{data.action_items}</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Emails</h3>
              <p className="text-3xl font-bold text-purple-600">{data.total_emails}</p>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Recent Events</h2>
          <p className="text-gray-600">Events will be displayed here</p>
        </div>
      </div>
    </div>
  )
}
