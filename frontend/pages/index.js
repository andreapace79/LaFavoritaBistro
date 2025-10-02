export default function Home() {
  return (
    <div style={{ 
      display: "flex", 
      flexDirection: "column", 
      alignItems: "center", 
      justifyContent: "center", 
      minHeight: "100vh", 
      fontFamily: "Arial, sans-serif" 
    }}>
      <h1>🍷 La Favorita Bistro</h1>
      <img 
        src="/LaFavoritaLogo.jpeg" 
        alt="La Favorita Bistro Logo" 
        style={{ maxWidth: "400px", borderRadius: "12px", marginTop: "20px" }}
      />
      <p style={{ marginTop: "30px" }}>
        👉 Vai a <a href="/users">Gestione utenti</a>
      </p>
    </div>
  );
}
