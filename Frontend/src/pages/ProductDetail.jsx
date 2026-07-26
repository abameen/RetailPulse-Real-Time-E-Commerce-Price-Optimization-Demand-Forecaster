// import { useParams } from 'react-router-dom';

// export default function ProductDetail() {
//   const { id } = useParams();
//   return (
//     <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//       <h1 className="text-3xl font-semibold text-slate-900">Product Detail</h1>
//       <p className="mt-4 text-slate-600">Viewing product ID: {id}</p>
//     </div>
//   );
// }
// import { useEffect, useState } from 'react'
// import { useParams } from 'react-router-dom'
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
// } from 'recharts'

// const API_BASE = 'http://127.0.0.1:8000'

// export default function ProductDetail() {
//   const { id } = useParams()

//   const [history, setHistory] = useState([])
//   const [historyLoading, setHistoryLoading] = useState(true)
//   const [historyError, setHistoryError] = useState(null)

//   const [price, setPrice] = useState(50)
//   const [targetDate, setTargetDate] = useState('')
//   const [prediction, setPrediction] = useState(null)
//   const [predictLoading, setPredictLoading] = useState(false)
//   const [predictError, setPredictError] = useState(null)

//   // Load historical sales/price data for the chart
//   useEffect(() => {
//     setHistoryLoading(true)
//     fetch(`${API_BASE}/sales-history/${id}`)
//       .then((res) => {
//         if (!res.ok) throw new Error(`Request failed: ${res.status}`)
//         return res.json()
//       })
//       .then((data) => {
//         setHistory(data)
//         setHistoryLoading(false)

//         if (data.length > 0) {
//           const last = data[data.length - 1]
//           setPrice(last.avg_price)

//           const nextDay = new Date(last.order_date)
//           nextDay.setDate(nextDay.getDate() + 1)
//           setTargetDate(nextDay.toISOString().split('T')[0])
//         }
//       })
//       .catch((err) => {
//         setHistoryError(err.message)
//         setHistoryLoading(false)
//       })
//   }, [id])

//   // Call /forecast/predict whenever price or targetDate changes
//   useEffect(() => {
//     if (!targetDate) return

//     setPredictLoading(true)
//     setPredictError(null)

//     fetch(`${API_BASE}/forecast/predict`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({
//         product_id: id,
//         target_date: targetDate,
//         simulated_price: price,
//       }),
//     })
//       .then((res) => {
//         if (!res.ok) {
//           return res.json().then((body) => {
//             throw new Error(body.detail || `Request failed: ${res.status}`)
//           })
//         }
//         return res.json()
//       })
//       .then((data) => {
//         setPrediction(data.predicted_units_sold)
//         setPredictLoading(false)
//       })
//       .catch((err) => {
//         setPredictError(err.message)
//         setPredictLoading(false)
//         setPrediction(null)
//       })
//   }, [id, targetDate, price])

//   return (
//     <div className="space-y-6">
//       <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//         <h1 className="text-3xl font-semibold text-slate-900">Product Detail</h1>
//         <p className="mt-2 text-slate-600">Product ID: {id}</p>
//       </div>

//       {/* Historical chart */}
//       <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//         <h2 className="mb-4 text-xl font-semibold text-slate-900">
//           Sales Volume vs. Price History
//         </h2>

//         {historyLoading && <p className="text-slate-500">Loading history...</p>}
//         {historyError && (
//           <p className="text-red-600">Failed to load history: {historyError}</p>
//         )}

//         {!historyLoading && !historyError && history.length > 0 && (
//           <ResponsiveContainer width="100%" height={350}>
//             <LineChart data={history}>
//               <CartesianGrid strokeDasharray="3 3" />
//               <XAxis dataKey="order_date" />
//               <YAxis yAxisId="left" />
//               <YAxis yAxisId="right" orientation="right" />
//               <Tooltip />
//               <Legend />
//               <Line
//                 yAxisId="left"
//                 type="monotone"
//                 dataKey="units_sold"
//                 stroke="#2563eb"
//                 name="Units Sold"
//                 dot={false}
//               />
//               <Line
//                 yAxisId="right"
//                 type="monotone"
//                 dataKey="avg_price"
//                 stroke="#16a34a"
//                 name="Avg Price"
//                 dot={false}
//               />
//             </LineChart>
//           </ResponsiveContainer>
//         )}
//       </div>

//       {/* What-If Simulator */}
//       <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//         <h2 className="mb-4 text-xl font-semibold text-slate-900">
//           What-If Price Simulator
//         </h2>

//         <label className="mb-2 block text-sm text-slate-600">
//           Adjust price: <span className="font-semibold">${price.toFixed(2)}</span>
//         </label>
//         <input
//           type="range"
//           min={1}
//           max={500}
//           step={0.5}
//           value={price}
//           onChange={(e) => setPrice(parseFloat(e.target.value))}
//           className="w-full"
//         />

//         <div className="mt-4 text-sm text-slate-600">
//           Forecast date: <span className="font-medium">{targetDate || '—'}</span>
//         </div>

//         <div className="mt-6 rounded-lg bg-slate-50 p-4">
//           {predictLoading && <p className="text-slate-500">Calculating...</p>}
//           {predictError && (
//             <p className="text-red-600">Prediction failed: {predictError}</p>
//           )}
//           {!predictLoading && !predictError && prediction !== null && (
//             <p className="text-lg">
//               Predicted units sold:{' '}
//               <span className="font-semibold text-slate-900">
//                 {prediction.toFixed(2)}
//               </span>
//             </p>
//           )}
//         </div>
//       </div>
//     </div>
//   )
// }

import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const API_BASE = 'http://127.0.0.1:8000'
const MIN_ROWS_REQUIRED = 7
const LOOKBACK_DAYS = 30

// Walks backward from the day after the last known sale, checking how many
// history rows fall in the 30-day window before each candidate date, and
// returns the most recent candidate that has enough rows for lag_7 to work.
function findRobustDefaultDate(history) {
  if (history.length === 0) return null

  const dates = history.map((h) => new Date(h.order_date))
  const lastDate = dates[dates.length - 1]

  // Start one day after the last known sale, then step backward until
  // we find a date whose trailing 30-day window has enough rows.
  for (let offset = 1; offset <= 365; offset++) {
    const candidate = new Date(lastDate)
    candidate.setDate(candidate.getDate() + 1 - (offset - 1))

    const windowStart = new Date(candidate)
    windowStart.setDate(windowStart.getDate() - LOOKBACK_DAYS)

    const rowsInWindow = dates.filter(
      (d) => d >= windowStart && d < candidate
    ).length

    if (rowsInWindow >= MIN_ROWS_REQUIRED) {
      return candidate.toISOString().split('T')[0]
    }
  }

  // Fallback: shouldn't normally hit this if history has >=7 rows total
  return lastDate.toISOString().split('T')[0]
}

export default function ProductDetail() {
  const { id } = useParams()

  const [history, setHistory] = useState([])
  const [historyLoading, setHistoryLoading] = useState(true)
  const [historyError, setHistoryError] = useState(null)

  const [price, setPrice] = useState(50)
  const [targetDate, setTargetDate] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [predictLoading, setPredictLoading] = useState(false)
  const [predictError, setPredictError] = useState(null)

  useEffect(() => {
    setHistoryLoading(true)
    fetch(`${API_BASE}/sales-history/${id}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Request failed: ${res.status}`)
        return res.json()
      })
      .then((data) => {
        setHistory(data)
        setHistoryLoading(false)

        if (data.length > 0) {
          const last = data[data.length - 1]
          setPrice(last.avg_price)
          setTargetDate(findRobustDefaultDate(data))
        }
      })
      .catch((err) => {
        setHistoryError(err.message)
        setHistoryLoading(false)
      })
  }, [id])

  useEffect(() => {
    if (!targetDate) return

    setPredictLoading(true)
    setPredictError(null)

    fetch(`${API_BASE}/forecast/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_id: id,
        target_date: targetDate,
        simulated_price: price,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((body) => {
            throw new Error(body.detail || `Request failed: ${res.status}`)
          })
        }
        return res.json()
      })
      .then((data) => {
        setPrediction(data.predicted_units_sold)
        setPredictLoading(false)
      })
      .catch((err) => {
        setPredictError(err.message)
        setPredictLoading(false)
        setPrediction(null)
      })
  }, [id, targetDate, price])

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-semibold text-slate-900">Product Detail</h1>
        <p className="mt-2 text-slate-600">Product ID: {id}</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          Sales Volume vs. Price History
        </h2>

        {historyLoading && <p className="text-slate-500">Loading history...</p>}
        {historyError && (
          <p className="text-red-600">Failed to load history: {historyError}</p>
        )}

        {!historyLoading && !historyError && history.length > 0 && (
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="order_date" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="units_sold"
                stroke="#2563eb"
                name="Units Sold"
                dot={false}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="avg_price"
                stroke="#16a34a"
                name="Avg Price"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold text-slate-900">
          What-If Price Simulator
        </h2>

        <label className="mb-2 block text-sm text-slate-600">
          Adjust price: <span className="font-semibold">${price.toFixed(2)}</span>
        </label>
        <input
          type="range"
          min={1}
          max={500}
          step={0.5}
          value={price}
          onChange={(e) => setPrice(parseFloat(e.target.value))}
          className="w-full"
        />

        <div className="mt-4 flex items-center gap-2 text-sm text-slate-600">
          <label htmlFor="target-date">Forecast date:</label>
          <input
            id="target-date"
            type="date"
            value={targetDate}
            onChange={(e) => setTargetDate(e.target.value)}
            className="rounded border border-slate-300 px-2 py-1"
          />
        </div>

        <div className="mt-6 rounded-lg bg-slate-50 p-4">
          {predictLoading && <p className="text-slate-500">Calculating...</p>}
          {predictError && (
            <p className="text-red-600">Prediction failed: {predictError}</p>
          )}
          {!predictLoading && !predictError && prediction !== null && (
            <p className="text-lg">
              Predicted units sold:{' '}
              <span className="font-semibold text-slate-900">
                {prediction.toFixed(2)}
              </span>
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
