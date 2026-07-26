// export default function InventoryDashboard() {
//   return (
//     <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
//       <h1 className="text-3xl font-semibold text-slate-900">Inventory Dashboard</h1>
//       <p className="mt-4 text-slate-600">This is the inventory dashboard placeholder page.</p>
//     </div>
//   );
// }

// import { useEffect, useState } from 'react'

// const API_BASE = 'http://127.0.0.1:8000'

// function getStatus(index) {
//   if (index === null || index === undefined) {
//     return { label: 'Unknown', color: 'bg-gray-100 text-gray-600' }
//   }
//   if (index > 1.3) {
//     return { label: 'Priced Too High', color: 'bg-red-100 text-red-700' }
//   }
//   if (index < 0.7) {
//     return { label: 'Priced Too Low', color: 'bg-yellow-100 text-yellow-700' }
//   }
//   return { label: 'Optimal', color: 'bg-green-100 text-green-700' }
// }

// function InventoryDashboard() {
//   const [products, setProducts] = useState([])
//   const [loading, setLoading] = useState(true)
//   const [error, setError] = useState(null)

//   useEffect(() => {
//     fetch(`${API_BASE}/products/?skip=0&limit=100`)
//       .then((res) => {
//         if (!res.ok) throw new Error(`Request failed: ${res.status}`)
//         return res.json()
//       })
//       .then((data) => {
//         setProducts(data)
//         setLoading(false)
//       })
//       .catch((err) => {
//         setError(err.message)
//         setLoading(false)
//       })
//   }, [])

//   if (loading) {
//     return <div className="p-6 text-slate-500">Loading products...</div>
//   }

//   if (error) {
//     return (
//       <div className="p-6 text-red-600">
//         Failed to load products: {error}
//         <div className="mt-2 text-sm text-slate-500">
//           Is the backend running at {API_BASE}?
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className="p-6">
//       <h1 className="mb-4 text-2xl font-bold">Inventory Dashboard</h1>
//       <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
//         <table className="min-w-full text-left text-sm">
//           <thead className="bg-slate-100 text-slate-600">
//             <tr>
//               <th className="px-4 py-3">Product ID</th>
//               <th className="px-4 py-3">Category</th>
//               <th className="px-4 py-3">Current Price</th>
//               <th className="px-4 py-3">Price Index</th>
//               <th className="px-4 py-3">Status</th>
//             </tr>
//           </thead>
//           <tbody>
//             {products.map((product) => {
//               const status = getStatus(product.category_price_index)
//               return (
//                 <tr key={product.id} className="border-t">
//                   <td className="px-4 py-3 font-mono text-xs text-slate-700">
//                     {product.name}
//                   </td>
//                   <td className="px-4 py-3 text-slate-700">{product.category}</td>
//                   <td className="px-4 py-3 text-slate-700">
//                     ${product.current_price.toFixed(2)}
//                   </td>
//                   <td className="px-4 py-3 text-slate-700">
//                     {product.category_price_index !== null
//                       ? product.category_price_index.toFixed(2)
//                       : '—'}
//                   </td>
//                   <td className="px-4 py-3">
//                     <span
//                       className={`rounded-full px-3 py-1 text-xs font-medium ${status.color}`}
//                     >
//                       {status.label}
//                     </span>
//                   </td>
//                 </tr>
//               )
//             })}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   )
// }

// export default InventoryDashboard


import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = 'http://127.0.0.1:8000'

function getStatus(index) {
  if (index === null || index === undefined) {
    return { label: 'Unknown', color: 'bg-gray-100 text-gray-600' }
  }
  if (index > 1.3) {
    return { label: 'Priced Too High', color: 'bg-red-100 text-red-700' }
  }
  if (index < 0.7) {
    return { label: 'Priced Too Low', color: 'bg-yellow-100 text-yellow-700' }
  }
  return { label: 'Optimal', color: 'bg-green-100 text-green-700' }
}

function InventoryDashboard() {
  const navigate = useNavigate()
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/products/?skip=0&limit=100`)
      .then((res) => {
        if (!res.ok) throw new Error(`Request failed: ${res.status}`)
        return res.json()
      })
      .then((data) => {
        setProducts(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="p-6 text-slate-500">Loading products...</div>
  }

  if (error) {
    return (
      <div className="p-6 text-red-600">
        Failed to load products: {error}
        <div className="mt-2 text-sm text-slate-500">
          Is the backend running at {API_BASE}?
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <h1 className="mb-4 text-2xl font-bold">Inventory Dashboard</h1>
      <div className="overflow-x-auto rounded-lg border bg-white shadow-sm">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-100 text-slate-600">
            <tr>
              <th className="px-4 py-3">Product ID</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Current Price</th>
              <th className="px-4 py-3">Price Index</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              const status = getStatus(product.category_price_index)
              return (
                <tr
                  key={product.id}
                  onClick={() => navigate(`/product/${product.name}`)}
                  className="cursor-pointer border-t hover:bg-slate-50"
                >
                  <td className="px-4 py-3 font-mono text-xs text-slate-700">
                    {product.name}
                  </td>
                  <td className="px-4 py-3 text-slate-700">{product.category}</td>
                  <td className="px-4 py-3 text-slate-700">
                    ${product.current_price.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {product.category_price_index !== null
                      ? product.category_price_index.toFixed(2)
                      : '—'}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-medium ${status.color}`}
                    >
                      {status.label}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default InventoryDashboard
