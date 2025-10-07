export default function Dashboard() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <h1 className="text-2xl font-bold text-primary mb-4">
        Dashboard – La Favorita Bistrò
      </h1>
      <p className="text-gray-600 mb-6">Accesso avvenuto con successo.</p>
      <button
        onClick={() => {
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }}
        className="bg-gray-800 text-white px-4 py-2 rounded hover:bg-gray-700"
      >
        Logout
      </button>
    </div>
  )
}
