// ==========================================
// MOIL AI — UNIFIED API CLIENT
// ==========================================
// Talks to the real FastAPI backend in /backend.
// Requires js/config.js to be loaded first (defines BACKEND_BASE_URL).

const TOKEN_KEY = "minewise_token";
const USER_KEY = "minewise_user";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function isLoggedIn() {
  return !!getToken();
}

function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY) || "null");
  } catch {
    return null;
  }
}

function saveSession(tokenResponse) {
  localStorage.setItem(TOKEN_KEY, tokenResponse.access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(tokenResponse.user));
}

function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// Redirects to login if there's no token. Call at the top of every
// protected page (dashboard, exploration, production, risk, ai).
function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "login.html";
  }
}

async function apiRequest(
  path,
  { method = "GET", body = null, auth = true } = {},
) {
  const headers = {
    "Content-Type": "application/json",
  };

  // ==========================================
  // ADD JWT AUTHORIZATION TOKEN
  // ==========================================

  if (auth) {
    const token = getToken();

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }
  const response = await fetch(
    `${window.BACKEND_BASE_URL}${path}`,

    {
      method,

      headers,

      body: body ? JSON.stringify(body) : undefined,
    },
  );

  // ==========================================
  // HANDLE 401
  // ==========================================

  if (response.status === 401 && auth) {
    clearSession();

    window.location.href = "login.html";

    throw new Error("Session expired. Please log in again.");
  }
  // ==========================================
  // HANDLE ERRORS
  // ==========================================

  if (!response.ok) {
    let message = `Request failed (${response.status})`;

    try {
      const errData = await response.json();

      message = errData.detail || message;
    } catch {
      // Ignore JSON parsing error
    }

    throw new Error(message);
  }

  return response.json();
}

window.MOILAPI = {
  // ---------------- Health ----------------
  async checkHealth() {
    return apiRequest("/health", { auth: false });
  },

  // ---------------- Auth ----------------
  async register(name, email, password, role = "industrialist") {
    const data = await apiRequest("/auth/register", {
      method: "POST",
      auth: false,
      body: { name, email, password, role },
    });
    saveSession(data);
    return data;
  },

  async login(email, password) {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      auth: false,
      body: { email, password },
    });
    saveSession(data);
    return data;
  },

  logout() {
    clearSession();
    window.location.href = "login.html";
  },

  isLoggedIn,
  getCurrentUser,
  requireAuth,

  // ---------------- Mines ----------------
  async listMines() {
    return apiRequest("/mines/");
  },

  async createMine(name, location_name, latitude = null, longitude = null) {
    return apiRequest("/mines/", {
      method: "POST",
      body: { name, location_name, latitude, longitude },
    });
  },

  async deleteMine(mineId) {
    return apiRequest(`/mines/${mineId}`, { method: "DELETE" });
  },

  // ---------------- Exploration (M2) ----------------
  async analyzeArea(
    location,
    bufferDegrees = 0.01,
    gridRows = 10,
    gridCols = 10,
    mineId = null,
  ) {
    return apiRequest("/exploration/analyze", {
      method: "POST",
      body: {
        location,
        buffer_degrees: bufferDegrees,
        grid_rows: gridRows,
        grid_cols: gridCols,
        mine_id: mineId,
      },
    });
  },

  async explorationHistory(mineId) {
    return apiRequest(`/exploration/history/${mineId}`);
  },

    // ---------------- Production (M3) ----------------

  async productionYears() {
    return apiRequest("/production/years");
  },

  async productionHistory() {
    return apiRequest("/production/history");
  },

  async productionForecast(forecastYear = null) {

    let path = "/production/forecast";

    if (forecastYear) {
      path += `?forecast_year=${forecastYear}`;
    }

    return apiRequest(path);
  },

  async productionSummary(forecastYear = null) {

    let path = "/production/summary";

    if (forecastYear) {
      path += `?forecast_year=${forecastYear}`;
    }

    return apiRequest(path);
  },

  async productionShortfall(forecastYear = null) {

    let path = "/production/shortfall";

    if (forecastYear) {
      path += `?forecast_year=${forecastYear}`;
    }

    return apiRequest(path);
  },

  async setProductionTarget(month, targetTonnes) {

    return apiRequest("/production/target", {

      method: "POST",

      body: {

        month: month,

        target_tonnes: targetTonnes,

      },

    });

  },

  async productionAlerts(forecastYear = null) {

    let path = "/production/alerts";

    if (forecastYear) {
      path += `?forecast_year=${forecastYear}`;
    }

    return apiRequest(path);

  },
  // ---------------- AI Recommendations (M4) ----------------
  async getRecommendations(
    location = null,
    bufferDegrees = 0.01,
    gridRows = 10,
    gridCols = 10,
  ) {
    return apiRequest("/ai/recommendations", {
      method: "POST",
      body: {
        location,
        buffer_degrees: bufferDegrees,
        grid_rows: gridRows,
        grid_cols: gridCols,
      },
    });
  },
};
