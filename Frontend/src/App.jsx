import { Routes, Route, Link } from 'react-router-dom';
import InventoryDashboard from './pages/InventoryDashboard';
import ProductDetail from './pages/ProductDetail';
import ModelPerformance from './pages/ModelPerformance';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <div className="text-lg font-semibold">RetailPulse</div>
          <nav className="flex gap-4 text-sm font-medium text-slate-700">
            <Link to="/" className="hover:text-slate-900">Inventory</Link>
            <Link to="/model-performance" className="hover:text-slate-900">Model</Link>
            <Link to="/product/1" className="hover:text-slate-900">Product</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <Routes>
          <Route path="/" element={<InventoryDashboard />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/model-performance" element={<ModelPerformance />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
