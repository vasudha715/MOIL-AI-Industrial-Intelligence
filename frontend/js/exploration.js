// ==========================================
// MOIL AI - EXPLORATION PAGE CONTROLLER
// ==========================================

// ==========================================
// BACKEND STATUS
// ==========================================

async function checkBackend() {
  const statusElement = document.getElementById("backendStatus");

  try {
    await window.MOILAPI.checkHealth();

    statusElement.textContent = "Backend Online";

    statusElement.className = "text-success small fw-bold";
  } catch (error) {
    console.error("BACKEND ERROR:", error);

    statusElement.textContent = "Backend Offline";

    statusElement.className = "text-danger small fw-bold";
  }
}

// ==========================================
// RUN REAL ANALYSIS
// ==========================================

async function runRealAnalysis() {
  console.log("Starting real industrial analysis...");

  const locationInput = document.getElementById("locationInput");

  const gridSize = document.getElementById("gridSize");

  const bufferSize = document.getElementById("bufferSize");

  const analyzeButton = document.getElementById("analyzeButton");

  const statusElement = document.getElementById("analysisStatus");

  const locationName = locationInput.value.trim();

  // ======================================
  // VALIDATION
  // ======================================

  if (!locationName) {
    statusElement.innerHTML = `<span class="text-danger">

                Please enter a valid location.

            </span>`;

    return;
  }

  const gridValue = Number(gridSize.value);

  const bufferValue = Number(bufferSize.value);

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

        Analyzing...
        `;

  statusElement.innerHTML = `
        <span class="text-warning">

            Collecting real satellite,
            terrain, elevation and
            manganese data...

        </span>
        `;

  try {
    // ==================================
    // CALL FASTAPI
    // ==================================

    const data = await window.MOILAPI.analyzeArea(
      locationName,

      bufferValue,

      gridValue,

      gridValue,
    );

    console.log("ANALYSIS RESULT:", data);

    // ==================================
    // UPDATE STATISTICS
    // ==================================

    updateExplorationStatistics(data);

    // ==================================
    // UPDATE MAP
    // ==================================

    displayAnalysisResults(data);

    // ==================================
    // SUCCESS MESSAGE
    // ==================================

    statusElement.innerHTML = `
            <span class="text-success">

                <i class="bi bi-check-circle me-1"></i>

                Real industrial analysis
                completed successfully.

            </span>
            `;
  } catch (error) {
    console.error("ANALYSIS ERROR:", error);

    statusElement.innerHTML = `
            <span class="text-danger">

                <i
                    class="
                        bi
                        bi-exclamation-triangle
                        me-1
                    "
                ></i>

                Analysis failed:
                ${error.message}

            </span>
            `;
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

            Analyze
            `;
  }
}

// ==========================================
// UPDATE EXPLORATION STATISTICS
// ==========================================

function updateExplorationStatistics(data) {
  console.log("Updating exploration statistics...");

  // ======================================
  // LOCATION
  // ======================================

  const location = data.location || {};

  document.getElementById("locationResult").textContent =
    location.name || "Unknown";

  // ======================================
  // TOTAL ZONES
  // ======================================

  document.getElementById("totalZones").textContent = data.total_zones ?? 0;

  // ======================================
  // HIGH PRIORITY
  // ======================================

  const prioritySummary = data.priority_summary || {};

  document.getElementById("highPriority").textContent =
    prioritySummary.HIGH || 0;

  // ======================================
  // WEATHER
  // ======================================

  const weather = data.weather_risk || {};

  const weatherElement = document.getElementById("weatherRisk");

  weatherElement.textContent = weather.risk || "Unknown";

  // ======================================
  // WEATHER COLOR
  // ======================================

  const risk = String(weather.risk || "").toUpperCase();

  if (risk === "LOW") {
    weatherElement.className = "text-success mt-2";
  } else if (risk === "MODERATE") {
    weatherElement.className = "text-warning mt-2";
  } else {
    weatherElement.className = "text-danger mt-2";
  }

  // ======================================
  // SATELLITE DETAILS
  // ======================================

  const satellite = data.satellite || {};

  const satelliteElement = document.getElementById("satelliteDetails");

  const cloudCover =
    satellite.cloud_cover !== undefined
      ? (Number(satellite.cloud_cover) * 100).toFixed(4)
      : "Unknown";

  satelliteElement.innerHTML = `
        <div class="mb-2">

            <b>Image ID:</b>

            <br>

            ${satellite.image_id || "Unavailable"}

        </div>


        <div>

            <b>Cloud Cover:</b>

            ${cloudCover}%

        </div>
        `;
}

// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
  "DOMContentLoaded",

  async function () {
    console.log("Exploration page loaded");

    await checkBackend();
  },
);
