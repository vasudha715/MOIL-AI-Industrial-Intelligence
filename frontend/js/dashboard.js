// ==========================================
// MOIL AI INDUSTRIAL EXPLORATION DASHBOARD
// ==========================================

// ==========================================
// FORMAT NUMBER
// ==========================================

function formatNumber(value, decimals = 2) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "—";
  }

  return Number(value).toFixed(decimals);
}

// ==========================================
// GET PRIORITY BADGE
// ==========================================

function getPriorityBadge(priority) {
  const value = String(priority).toUpperCase();

  if (value === "HIGH") {
    return `
            <span
                class="
                badge
                badge-risk-high
                "
            >
                HIGH
            </span>
        `;
  }

  if (value === "MODERATE") {
    return `
            <span
                class="
                badge
                badge-risk-med
                "
            >
                MODERATE
            </span>
        `;
  }

  return `
        <span
            class="
            badge
            badge-risk-low
            "
        >
            LOW
        </span>
    `;
}

// ==========================================
// UPDATE BACKEND STATUS
// ==========================================

async function checkBackend() {
  const statusElement = document.getElementById("backendStatus");

  const systemStatus = document.getElementById("systemStatus");

  try {
    const result = await window.MOILAPI.checkHealth();

    console.log("BACKEND HEALTH:", result);

    statusElement.textContent = "Backend Online";

    systemStatus.innerHTML = `

            <i
                class="
                bi
                bi-broadcast
                me-1
                "
            ></i>

            AI Engine Online

        `;
  } catch (error) {
    console.error(error);

    statusElement.textContent = "Backend Offline";

    systemStatus.innerHTML = `

            <i
                class="
                bi
                bi-exclamation-triangle
                me-1
                "
            ></i>

            Backend Offline

        `;

    systemStatus.className =
      "badge bg-danger-subtle " + "text-danger border " + "border-danger";
  }
}

// ==========================================
// UPDATE DASHBOARD
// ==========================================

function updateDashboard(data) {
  console.log("REAL ANALYSIS DATA:", data);

  // ======================================
  // LOCATION
  // ======================================

  const location = data.location || {};

  document.getElementById("statLocation").textContent =
    location.name || "Unknown";

  document.getElementById("statCoordinates").textContent = `Lat: ${formatNumber(
    location.latitude,
    4,
  )}
        | Lon: ${formatNumber(location.longitude, 4)}`;

  // ======================================
  // WEATHER
  // ======================================

  const weather = data.weather_risk || {};

  document.getElementById("statWeather").textContent =
    weather.risk || "Unknown";

  document.getElementById("weatherMessage").textContent =
    weather.message || "Weather information unavailable";

  // ======================================
  // SATELLITE
  // ======================================

  const satellite = data.satellite || {};

  let cloudCover = satellite.cloud_cover;

  if (cloudCover !== undefined && cloudCover !== null) {
    cloudCover = Number(cloudCover);

    document.getElementById("statCloud").textContent =
      (cloudCover * 100).toFixed(4) + "%";
  } else {
    document.getElementById("statCloud").textContent = "—";
  }

  document.getElementById("satelliteId").textContent =
    satellite.image_id || "Satellite image unavailable";

  // ======================================
  // TOTAL ZONES
  // ======================================

  document.getElementById("statZones").textContent = data.total_zones ?? "—";

  // ======================================
  // PRIORITY SUMMARY
  // ======================================

  const prioritySummary = data.priority_summary || {};

  document.getElementById("highPriority").textContent =
    prioritySummary.HIGH || 0;

  document.getElementById("moderatePriority").textContent =
    prioritySummary.MODERATE || 0;

  document.getElementById("lowPriority").textContent = prioritySummary.LOW || 0;

  // ======================================
  // TOP ZONES
  // ======================================

  const zones = data.top_zones || [];

  document.getElementById("zonesCount").textContent =
    `${zones.length} Top Zones`;

  updateZonesTable(zones);

  // ======================================
  // AI INSIGHT
  // ======================================

  if (zones.length > 0) {
    const topZone = zones[0];

    document.getElementById("insightTitle").textContent =
      `${topZone.zone_id} is the highest-ranked exploration zone`;

    document.getElementById("highestScore").textContent = `${formatNumber(
      topZone.PROSPECTIVITY_SCORE,
      2,
    )}%`;

    const nearestSite = topZone.NEAREST_MN_SITE || "No known occurrence";

    const distance = topZone.DISTANCE_TO_MN_KM;

    let distanceText = "Distance unavailable";

    if (distance !== null && distance !== undefined) {
      distanceText = `${formatNumber(
        distance,
        2,
      )} km from nearest known manganese occurrence`;
    }

    document.getElementById("insightMessage").textContent = `Zone ${
      topZone.zone_id
    } received the highest prospectivity score based on the current analysis pipeline. Nearest manganese occurrence: ${
      nearestSite
    }. ${distanceText}. Priority classification: ${topZone.PRIORITY}.`;
  } else {
    document.getElementById("insightTitle").textContent =
      "No exploration zones available";

    document.getElementById("insightMessage").textContent =
      "The analysis completed but no exploration zones were returned.";

    document.getElementById("highestScore").textContent = "—";
  }
}

// ==========================================
// UPDATE TOP ZONES TABLE
// ==========================================

function updateZonesTable(zones) {
  const tableBody = document.getElementById("topZonesTable");

  tableBody.innerHTML = "";

  if (zones.length === 0) {
    tableBody.innerHTML = `

            <tr>

                <td
                    colspan="8"
                    class="
                    text-center
                    text-muted
                    py-4
                    "
                >

                    No exploration zones found.

                </td>

            </tr>

        `;

    return;
  }

  zones.forEach((zone, index) => {
    const row = document.createElement("tr");

    const distance = zone.DISTANCE_TO_MN_KM;

    let distanceText = "N/A";

    if (distance !== null && distance !== undefined) {
      distanceText = formatNumber(distance, 2);
    }

    row.innerHTML = `


                <td>

                    <span
                        class="
                        text-warning
                        fw-bold
                        "
                    >

                        #${index + 1}

                    </span>

                </td>


                <td
                    class="
                    fw-bold
                    "
                >

                    ${zone.zone_id || "—"}

                </td>


                <td
                    class="
                    text-warning
                    fw-bold
                    "
                >

                    ${formatNumber(zone.PROSPECTIVITY_SCORE, 2)}

                </td>


                <td>

                    ${getPriorityBadge(zone.PRIORITY)}

                </td>


                <td>

                    ${formatNumber(zone.center_lat, 5)}

                </td>


                <td>

                    ${formatNumber(zone.center_lon, 5)}

                </td>


                <td>

                    ${zone.NEAREST_MN_SITE || "Unknown"}

                </td>


                <td>

                    ${distanceText}

                </td>


            `;

    tableBody.appendChild(row);
  });
}

// ==========================================
// RUN ANALYSIS
// ==========================================

async function runAnalysis() {
  const locationInput = document.getElementById("locationInput");

  const analyzeButton = document.getElementById("analyzeButton");

  const statusElement = document.getElementById("analysisStatus");

  const locationName = locationInput.value.trim();

  // ======================================
  // VALIDATE LOCATION
  // ======================================

  if (locationName.length === 0) {
    statusElement.textContent = "Please enter a valid location.";

    statusElement.className = "text-danger";

    return;
  }

  // ======================================
  // LOADING STATE
  // ======================================

  analyzeButton.disabled = true;

  analyzeButton.innerHTML = `

        <span
            class="
            spinner-border
            spinner-border-sm
            me-2
            "
        ></span>

        Running Real Analysis...

    `;

  statusElement.textContent =
    "Collecting real satellite, terrain, weather and mineral occurrence data. This may take some time...";

  statusElement.className = "text-warning";

  try {
    // ==================================
    // CALL REAL BACKEND
    // ==================================

    const data = await window.MOILAPI.analyzeArea(
      locationName,

      0.01,

      10,

      10,
    );

    // ==================================
    // UPDATE DASHBOARD
    // ==================================

    console.log("ANALYSIS RESPONSE RECEIVED:", data);

updateDashboard(data);

console.log("DASHBOARD UPDATED SUCCESSFULLY");

    statusElement.textContent =
      "Industrial analysis completed successfully using real data.";

    statusElement.className = "text-success";
  } catch (error) {
    console.error("ANALYSIS ERROR:", error);

    statusElement.textContent = `Analysis failed: ${error.message}`;

    statusElement.className = "text-danger";
  } finally {
    analyzeButton.disabled = false;

    analyzeButton.innerHTML = `

            <i
                class="
                bi
                bi-cpu
                me-2
                "
            ></i>

            Run AI Analysis

        `;
  }
}

// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
  "DOMContentLoaded",

  async () => {
    // ======================================
    // AUTHENTICATION CHECK
    // ======================================
    const demoAuthenticated =
      localStorage.getItem("moilAuthenticated") === "true";

    const realAuthenticated = window.MOILAPI.isLoggedIn();

    if (!demoAuthenticated && !realAuthenticated) {
      window.location.href = "login.html";

      return;
    }

    // ======================================
    // CHECK BACKEND
    // ======================================

    await checkBackend();
    await loadProductionIntelligence();

    // ======================================
    // ANALYZE BUTTON
    // ======================================

    document
      .getElementById("analyzeButton")

      .addEventListener(
        "click",

        runAnalysis,
      );
  },
);
// ==========================================
// PRODUCTION INTELLIGENCE
// ==========================================

async function loadProductionIntelligence() {
  try {
    // ======================================
    // LOAD DATA
    // ======================================

    const summary = await window.MOILAPI.productionSummary();

    const forecast = await window.MOILAPI.productionForecast();

    const shortfall = await window.MOILAPI.productionShortfall();

    const alerts = await window.MOILAPI.productionAlerts();

    // ======================================
    // SUMMARY
    // ======================================

    document.getElementById("production2024").textContent =
      Math.round(summary.total_2024_tonnes).toLocaleString() + " t";

    document.getElementById("production2025").textContent =
      Math.round(summary.total_2025_tonnes).toLocaleString() + " t";

    document.getElementById("productionGrowth").textContent =
      summary.growth_2025_vs_2024_pct + "%";

    document.getElementById("forecast2026").textContent =
      Math.round(summary.forecast_2026_total_tonnes).toLocaleString() + " t";

    // ======================================
    // FORECAST TABLE
    // ======================================

    const forecastTable = document.getElementById("forecastTable");

    forecastTable.innerHTML = "";

    forecast.forEach((row) => {
      forecastTable.innerHTML += `

          <tr>

            <td>
              ${row.month}
            </td>


            <td>
              ${Math.round(row.forecast_tonnes).toLocaleString()}
            </td>


            <td>
              ${row.method}
            </td>


            <td>
              ${row.basis}
            </td>

          </tr>

        `;
    });

    // ======================================
    // SHORTFALL TABLE
    // ======================================

    const shortfallTable = document.getElementById("shortfallTable");

    shortfallTable.innerHTML = "";

    shortfall.forEach((row) => {
      let target = row.approved_target_tonnes;

      let shortfallValue = row.shortfall_tonnes;

      shortfallTable.innerHTML += `

          <tr>

            <td>

              ${row.month}

            </td>


            <td>

              ${Math.round(row.forecast_tonnes).toLocaleString()}

            </td>


            <td>

              ${target ? Math.round(target).toLocaleString() : "Not set"}

            </td>


            <td>

              ${
                shortfallValue !== null
                  ? Math.round(shortfallValue).toLocaleString()
                  : "--"
              }

            </td>


            <td>

              ${row.status}

            </td>

          </tr>

        `;
    });

    // ======================================
    // ALERTS
    // ======================================

    const alertsContainer = document.getElementById("productionAlerts");

    alertsContainer.innerHTML = "";

    alerts.forEach((alert) => {
      alertsContainer.innerHTML += `

          <div
            class="alert alert-warning"
          >

            <strong>

              ${alert.type}

            </strong>

            <br>

            ${alert.message}

          </div>

        `;
    });

    console.log("Production Intelligence loaded successfully");
  } catch (error) {
    console.error("Production Intelligence error:", error);

    const alertsContainer = document.getElementById("productionAlerts");

    if (alertsContainer) {
      alertsContainer.innerHTML = `

        <div class="alert alert-danger">

          Failed to load production data:

          ${error.message}

        </div>

      `;
    }
  }
}

// ==========================================
// MAKE FUNCTION AVAILABLE TO HTML
// ==========================================

window.loadProductionIntelligence = loadProductionIntelligence;
