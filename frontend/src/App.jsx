import React, { useState, useEffect } from "react";
import { api } from "./api";

export default function App() {
  const [user, setUser] = useState(api.getSavedUser());
  const [authMode, setAuthMode] = useState("login"); // 'login' or 'register'
  
  // Auth Form State
  const [authUsername, setAuthUsername] = useState("");
  const [authEmail, setAuthEmail] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [authSuccess, setAuthSuccess] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  // Movies State
  const [movies, setMovies] = useState([]);
  const [loadingMovies, setLoadingMovies] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterMode, setFilterMode] = useState("all"); // 'all', 'watched', 'unwatched'

  // Add / Edit Modal State
  const [showModal, setShowModal] = useState(false);
  const [editingMovie, setEditingMovie] = useState(null);
  const [modalTitle, setModalTitle] = useState("");
  const [modalGenre, setModalGenre] = useState("");
  const [modalRating, setModalRating] = useState("8.0");
  const [modalWatched, setModalWatched] = useState(false);
  const [modalError, setModalError] = useState("");
  const [notification, setNotification] = useState("");

  // Fetch movies when user is logged in
  useEffect(() => {
    if (user) {
      fetchMovies();
    }
  }, [user]);

  const showToast = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(""), 3500);
  };

  const fetchMovies = async () => {
    setLoadingMovies(true);
    try {
      const res = await api.getMovies();
      setMovies(res.movies || []);
    } catch (err) {
      if (err.message.includes("token") || err.message.includes("401")) {
        handleLogout();
      }
    } finally {
      setLoadingMovies(false);
    }
  };

  // Auth Handler
  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setAuthError("");
    setAuthSuccess("");
    setAuthLoading(true);

    try {
      if (authMode === "register") {
        const res = await api.register(authUsername, authEmail, authPassword);
        setAuthSuccess(res.message + "! You can now log in.");
        setAuthMode("login");
        setAuthPassword("");
      } else {
        const res = await api.login(authEmail, authPassword);
        setUser({
          id: res.user_id,
          username: res.username,
          email: res.email,
        });
        showToast(res.message);
      }
    } catch (err) {
      setAuthError(err.message);
    } finally {
      setAuthLoading(false);
    }
  };

  const handleLogout = () => {
    api.logout();
    setUser(null);
    setMovies([]);
  };

  // Movie Handlers
  const handleOpenAddModal = () => {
    setEditingMovie(null);
    setModalTitle("");
    setModalGenre("");
    setModalRating("8.0");
    setModalWatched(false);
    setModalError("");
    setShowModal(true);
  };

  const handleOpenEditModal = (movie) => {
    setEditingMovie(movie);
    setModalTitle(movie.title);
    setModalGenre(movie.genre);
    setModalRating(String(movie.rating));
    setModalWatched(movie.is_watched);
    setModalError("");
    setShowModal(true);
  };

  const handleSaveMovie = async (e) => {
    e.preventDefault();
    setModalError("");

    const ratingNum = parseFloat(modalRating);
    if (isNaN(ratingNum) || ratingNum < 0 || ratingNum > 10) {
      setModalError("Rating must be between 0.0 and 10.0");
      return;
    }

    try {
      if (editingMovie) {
        const res = await api.updateMovie(editingMovie.id, {
          title: modalTitle,
          genre: modalGenre,
          rating: ratingNum,
          is_watched: modalWatched,
        });
        showToast(res.message);
      } else {
        const res = await api.addMovie({
          title: modalTitle,
          genre: modalGenre,
          rating: ratingNum,
          is_watched: modalWatched,
        });
        showToast(res.message);
      }
      setShowModal(false);
      fetchMovies();
    } catch (err) {
      setModalError(err.message);
    }
  };

  const handleToggleWatched = async (movie) => {
    try {
      const res = await api.updateMovie(movie.id, {
        is_watched: !movie.is_watched,
      });
      showToast(res.message);
      fetchMovies();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDeleteMovie = async (id, title) => {
    if (!window.confirm(`Are you sure you want to delete "${title}"?`)) return;
    try {
      const res = await api.deleteMovie(id);
      showToast(res.message);
      fetchMovies();
    } catch (err) {
      alert(err.message);
    }
  };

  // Filtered list
  const filteredMovies = movies.filter((m) => {
    const matchesSearch =
      m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.genre.toLowerCase().includes(searchQuery.toLowerCase());

    if (filterMode === "watched") return matchesSearch && m.is_watched;
    if (filterMode === "unwatched") return matchesSearch && !m.is_watched;
    return matchesSearch;
  });

  // Stats calculation
  const totalCount = movies.length;
  const watchedCount = movies.filter((m) => m.is_watched).length;
  const unwatchedCount = totalCount - watchedCount;
  const avgRating = totalCount
    ? (movies.reduce((sum, m) => sum + m.rating, 0) / totalCount).toFixed(1)
    : "0.0";

  return (
    <div>
      {/* Top Navigation */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">🎬</div>
          <span>Watchlist Hub</span>
        </div>

        {user && (
          <div className="nav-user">
            <div className="user-badge">
              <span className="user-dot"></span>
              <strong>{user.username}</strong> ({user.email})
            </div>
            <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </nav>

      {/* Toast Notification */}
      {notification && (
        <div style={{ position: "fixed", bottom: "20px", right: "20px", zIndex: 999 }}>
          <div className="alert alert-success" style={{ boxShadow: "var(--shadow-lg)" }}>
            ✓ {notification}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      {!user ? (
        // ================= AUTH VIEW =================
        <div className="auth-wrapper">
          <div className="auth-card">
            <div className="auth-header">
              <h2>{authMode === "login" ? "Welcome Back" : "Create Account"}</h2>
              <p>
                {authMode === "login"
                  ? "Log in to view and manage your movie watchlist"
                  : "Join to start tracking your favorite movies"}
              </p>
            </div>

            <div className="auth-tabs">
              <button
                className={`auth-tab ${authMode === "login" ? "active" : ""}`}
                onClick={() => {
                  setAuthMode("login");
                  setAuthError("");
                }}
              >
                Login
              </button>
              <button
                className={`auth-tab ${authMode === "register" ? "active" : ""}`}
                onClick={() => {
                  setAuthMode("register");
                  setAuthError("");
                }}
              >
                Register
              </button>
            </div>

            {authError && <div className="alert alert-danger">{authError}</div>}
            {authSuccess && <div className="alert alert-success">{authSuccess}</div>}

            <form onSubmit={handleAuthSubmit}>
              {authMode === "register" && (
                <div className="form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g. alex"
                    value={authUsername}
                    onChange={(e) => setAuthUsername(e.target.value)}
                    required
                    minLength={3}
                    maxLength={60}
                  />
                </div>
              )}

              <div className="form-group">
                <label>Email Address</label>
                <input
                  type="email"
                  className="form-control"
                  placeholder="name@example.com"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Password {authMode === "register" && "(min 8 chars)"}</label>
                <input
                  type="password"
                  className="form-control"
                  placeholder="••••••••"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  required
                  minLength={8}
                />
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: "100%", marginTop: "0.5rem" }}
                disabled={authLoading}
              >
                {authLoading
                  ? "Processing..."
                  : authMode === "login"
                  ? "Log In"
                  : "Sign Up"}
              </button>
            </form>
          </div>
        </div>
      ) : (
        // ================= DASHBOARD VIEW =================
        <div className="container">
          {/* Stats Bar */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon" style={{ background: "rgba(99, 102, 241, 0.2)", color: "#818cf8" }}>
                🎥
              </div>
              <div>
                <div className="stat-val">{totalCount}</div>
                <div className="stat-label">Total Movies</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399" }}>
                ✓
              </div>
              <div>
                <div className="stat-val">{watchedCount}</div>
                <div className="stat-label">Watched</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: "rgba(245, 158, 11, 0.2)", color: "#fbbf24" }}>
                ⏳
              </div>
              <div>
                <div className="stat-val">{unwatchedCount}</div>
                <div className="stat-label">To Watch</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: "rgba(236, 72, 153, 0.2)", color: "#f472b6" }}>
                ★
              </div>
              <div>
                <div className="stat-val">{avgRating}</div>
                <div className="stat-label">Avg Rating</div>
              </div>
            </div>
          </div>

          {/* Controls Bar */}
          <div className="controls-header">
            <div className="search-box">
              <input
                type="text"
                className="form-control"
                placeholder="🔍 Search title or genre..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            <div className="filter-pills">
              <button
                className={`filter-pill ${filterMode === "all" ? "active" : ""}`}
                onClick={() => setFilterMode("all")}
              >
                All ({totalCount})
              </button>
              <button
                className={`filter-pill ${filterMode === "unwatched" ? "active" : ""}`}
                onClick={() => setFilterMode("unwatched")}
              >
                To Watch ({unwatchedCount})
              </button>
              <button
                className={`filter-pill ${filterMode === "watched" ? "active" : ""}`}
                onClick={() => setFilterMode("watched")}
              >
                Watched ({watchedCount})
              </button>
            </div>

            <button className="btn btn-primary" onClick={handleOpenAddModal}>
              + Add Movie
            </button>
          </div>

          {/* Movies Grid */}
          {loadingMovies ? (
            <div className="empty-state">Loading your watchlist...</div>
          ) : filteredMovies.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">🍿</div>
              <h3>No movies found</h3>
              <p style={{ marginTop: "0.5rem" }}>
                {searchQuery
                  ? "No movies match your search."
                  : "Your watchlist is currently empty. Click '+ Add Movie' to get started!"}
              </p>
            </div>
          ) : (
            <div className="movie-grid">
              {filteredMovies.map((movie) => (
                <div key={movie.id} className="movie-card">
                  <div>
                    <div className="movie-top">
                      <h4 className="movie-title">{movie.title}</h4>
                      <span
                        className={`badge ${
                          movie.is_watched ? "badge-watched" : "badge-unwatched"
                        }`}
                      >
                        {movie.is_watched ? "Watched" : "To Watch"}
                      </span>
                    </div>

                    <div className="movie-meta">
                      <span className="genre-tag">{movie.genre}</span>
                      <span className="rating-tag">★ {movie.rating.toFixed(1)}</span>
                    </div>
                  </div>

                  <div className="movie-actions">
                    <button
                      className="btn btn-secondary btn-sm"
                      style={{ flex: 1 }}
                      onClick={() => handleToggleWatched(movie)}
                    >
                      {movie.is_watched ? "Mark Unwatched" : "Mark Watched"}
                    </button>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleOpenEditModal(movie)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger-outline btn-sm"
                      onClick={() => handleDeleteMovie(movie.id, movie.title)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Add / Edit Movie Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingMovie ? "Edit Movie" : "Add New Movie"}</h3>
              <button className="close-btn" onClick={() => setShowModal(false)}>
                ×
              </button>
            </div>

            {modalError && <div className="alert alert-danger">{modalError}</div>}

            <form onSubmit={handleSaveMovie}>
              <div className="form-group">
                <label>Movie Title</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. Interstellar"
                  value={modalTitle}
                  onChange={(e) => setModalTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Genre</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. Sci-Fi, Action, Drama"
                  value={modalGenre}
                  onChange={(e) => setModalGenre(e.target.value)}
                  required
                />
                <div style={{ display: "flex", gap: "0.3rem", marginTop: "0.5rem", flexWrap: "wrap" }}>
                  {["Sci-Fi", "Action", "Drama", "Comedy", "Thriller", "Anime"].map((g) => (
                    <button
                      type="button"
                      key={g}
                      className="filter-pill"
                      style={{ fontSize: "0.75rem", padding: "0.2rem 0.5rem" }}
                      onClick={() => setModalGenre(g)}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Rating (0.0 to 10.0)</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="10"
                  className="form-control"
                  value={modalRating}
                  onChange={(e) => setModalRating(e.target.value)}
                  required
                />
              </div>

              <div className="form-group" style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                <input
                  type="checkbox"
                  id="watchedCheckbox"
                  style={{ width: "18px", height: "18px", cursor: "pointer" }}
                  checked={modalWatched}
                  onChange={(e) => setModalWatched(e.target.checked)}
                />
                <label htmlFor="watchedCheckbox" style={{ marginBottom: 0, cursor: "pointer" }}>
                  I have already watched this movie
                </label>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: "100%", marginTop: "1rem" }}
              >
                {editingMovie ? "Save Changes" : "Add to Watchlist"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

