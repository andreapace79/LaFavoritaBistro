import { useEffect, useState } from "react";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({ username: "", password: "" });

  // Carica utenti dal backend
  useEffect(() => {
    fetch("http://localhost:8000/rbac/users/")
      .then((res) => res.json())
      .then((data) => setUsers(data))
      .catch((err) => console.error("Errore fetch utenti:", err));
  }, []);

  // Funzione per iniziare l'edit
  const handleEdit = (user) => {
    setEditingUser(user.id);
    setFormData({ username: user.username, password: "" });
  };

  // Funzione per salvare l'edit
  const handleSave = async () => {
    try {
      const res = await fetch(`http://localhost:8000/rbac/users/${editingUser}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error("Errore update utente");
      const updatedUser = await res.json();

      setUsers(users.map((u) => (u.id === editingUser ? updatedUser : u)));
      setEditingUser(null);
      setFormData({ username: "", password: "" });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>👥 Gestione Utenti</h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "20px",
        }}
      >
        <thead>
          <tr>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>ID</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Username</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{user.id}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                {editingUser === user.id ? (
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) =>
                      setFormData({ ...formData, username: e.target.value })
                    }
                  />
                ) : (
                  user.username
                )}
              </td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                {editingUser === user.id ? (
                  <>
                    <input
                      type="password"
                      placeholder="Nuova password"
                      value={formData.password}
                      onChange={(e) =>
                        setFormData({ ...formData, password: e.target.value })
                      }
                    />
                    <button
                      onClick={handleSave}
                      style={{ marginLeft: "10px", padding: "4px 8px" }}
                    >
                      💾 Salva
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => handleEdit(user)}
                    style={{ padding: "4px 8px" }}
                  >
                    ✏️ Modifica
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

