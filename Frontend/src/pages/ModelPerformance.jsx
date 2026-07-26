// export default function ModelPerformance() {
//   return (
//     <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//       <h1 className="text-3xl font-semibold text-slate-900">Model Performance</h1>
//       <p className="mt-4 text-slate-600">This is the model performance placeholder page.</p>
//     </div>
//   );
// }

import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const API_BASE = 'http://127.0.0.1:8000'

export default function ModelPerformance() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/model-metrics/`)
      .then((res) => {
        if (!res.ok) throw new Error(`Request failed: ${res.status}`)
        return res.json()
      })
      .then((data) => {
        setMetrics(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="p-6 text-slate-500">Loading model metrics...</div>
  if (error) return <div className="p-6 text-red-600">Failed to load metrics: {error}</div>

  const topFeatures = metrics.feature_importance.slice(0, 10)

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Model Performance</h1>
        <div className="mt-4 flex gap-8">
          <div>
            <p className="text-sm text-slate-500">MAE</p>
            <p className="text-2xl font-bold text-slate-900">{metrics.mae.toFixed(4)}</p>
          </div>
          <div>
            <p className="text-sm text-slate-500">WAPE</p>
            <p className="text-2xl font-bold text-slate-900">
              {(metrics.wape * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Top 10 Most Important Features
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={topFeatures} layout="vertical" margin={{ left: 40 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis type="category" dataKey="feature" width={150} />
            <Tooltip />
            <Bar dataKey="importance" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}