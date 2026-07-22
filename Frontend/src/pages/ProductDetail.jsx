import { useParams } from 'react-router-dom';

export default function ProductDetail() {
  const { id } = useParams();
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="text-3xl font-semibold text-slate-900">Product Detail</h1>
      <p className="mt-4 text-slate-600">Viewing product ID: {id}</p>
    </div>
  );
}
