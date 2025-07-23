'use client'

import { useState, useEffect } from 'react'
import { MessageSquare, Clock, Coins } from 'lucide-react'

interface AnalyticsData {
  totalConversations: number
  avgResponseTime: number
  tokensUsed: number
}

export default function Analytics() {
  const [analytics, setAnalytics] = useState<AnalyticsData>({
    totalConversations: 0,
    avgResponseTime: 0,
    tokensUsed: 0
  })

  // Fetch analytics data
  useEffect(() => {
    fetchAnalytics()
    // Refresh every 30 seconds
    const interval = setInterval(fetchAnalytics, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchAnalytics = async () => {
    // For now, using mock data - replace with actual API call
    // const response = await fetch('http://localhost:8000/api/v1/analytics')
    // const data = await response.json()
    
    // Mock data for demonstration
    setAnalytics({
      totalConversations: 47,
      avgResponseTime: 2.3,
      tokensUsed: 15420
    })
  }

  const statCards = [
    {
      title: 'Total Conversations',
      value: analytics.totalConversations,
      icon: MessageSquare,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100 dark:bg-blue-900/20'
    },
    {
      title: 'Avg Response Time',
      value: `${analytics.avgResponseTime}s`,
      icon: Clock,
      color: 'text-green-600',
      bgColor: 'bg-green-100 dark:bg-green-900/20'
    },
    {
      title: 'Tokens Used',
      value: analytics.tokensUsed.toLocaleString(),
      icon: Coins,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100 dark:bg-purple-900/20'
    }
  ]

  return (
    <div className="glass-panel p-6">
      <h2 className="text-xl font-semibold mb-4">Analytics</h2>
      
      <div className="space-y-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`w-5 h-5 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.title}
                  </p>
                  <p className="text-lg font-semibold">
                    {stat.value}
                  </p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
      
      {/* Usage Chart (Simple Bar) */}
      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Token Usage (Last 7 days)
        </h3>
        <div className="flex items-end gap-1 h-16">
          {[40, 65, 45, 80, 55, 70, 60].map((height, i) => (
            <div
              key={i}
              className="flex-1 bg-blue-500 rounded-t"
              style={{ height: `${height}%` }}
            />
          ))}
        </div>
        <div className="flex justify-between mt-1 text-xs text-gray-500">
          <span>Mon</span>
          <span>Sun</span>
        </div>
      </div>
    </div>
  )
}