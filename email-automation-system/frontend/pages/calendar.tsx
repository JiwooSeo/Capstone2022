import React, { useState, useEffect } from 'react'
import Link from 'next/link'

interface Event {
  id: string
  title: string
  event_type: string
  extracted_date: string
  extracted_time: string
}

export default function Calendar() {
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        window.location.href = '/'
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/events`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setEvents(data)
      }
    } catch (err) {
      console.error('Failed to fetch events:', err)
    } finally {
      setLoading(false)
    }
  }

  const getEventColor = (type: string) => {
    switch (type) {
      case 'meeting':
        return 'bg-green-100 text-green-800'
      case 'deadline':
        return 'bg-red-100 text-red-800'
      case 'action_item':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Calendar</h1>
          <div className="space-x-4">
            <Link href="/" className="text-gray-600 hover:text-gray-900">
              Home
            </Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link href="/settings" className="text-gray-600 hover:text-gray-900">
              Settings
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h2 className="text-lg font-bold text-gray-800">Upcoming Events</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center text-gray-600">Loading events...</div>
          ) : events.length === 0 ? (
            <div className="p-6 text-center text-gray-600">No events scheduled</div>
          ) : (
            <div className="divide-y">
              {events.map((event) => (
                <div key={event.id} className="p-4 flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${getEventColor(event.event_type)}`}>
                        {event.event_type}
                      </span>
                    </div>
                    <h3 className="font-semibold text-gray-800">{event.title}</h3>
                    <p className="text-sm text-gray-600">
                      {event.extracted_date} {event.extracted_time || ''}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
