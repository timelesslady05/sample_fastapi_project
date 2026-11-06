const BASE_URL = "http://127.0.0.1:8000";

// Helper for making HTTP requests
async function request(endpoint, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    // If backend returns detail error string (or array of pydantic errors)
    let errorMsg = "Something went wrong";
    if (data && data.detail) {
      if (Array.isArray(data.detail)) {
        errorMsg = data.detail.map((err) => `${err.loc?.slice(-1)[0] || 'field'}: ${err.msg}`).join(", ");
      } else {
        errorMsg = data.detail;
      }
    }
    throw new Error(errorMsg);
  }

  return data;
}

export const api = {
  // ==================== AUTH APIs ====================
  register: (username, email, password) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    }),

  login: async (email, password) => {
    const data = await request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (data.access_token) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem(
        "user",
        JSON.stringify({
          id: data.user_id,
          username: data.username,
          email: data.email,
        })
      );
    }
    return data;
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },

  getSavedUser: () => {
    const raw = localStorage.getItem("user");
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  isAuthenticated: () => {
    return !!localStorage.getItem("access_token");
  },

  // ==================== MOVIE APIs ====================
  getMovies: () => request("/movies", { method: "GET" }),

  getMovie: (id) => request(`/movies/${id}`, { method: "GET" }),

  addMovie: (movieData) =>
    request("/movies", {
      method: "POST",
      body: JSON.stringify(movieData),
    }),

  updateMovie: (id, updateData) =>
    request(`/movies/${id}`, {
      method: "PUT",
      body: JSON.stringify(updateData),
    }),

  deleteMovie: (id) =>
    request(`/movies/${id}`, {
      method: "DELETE",
    }),
};

