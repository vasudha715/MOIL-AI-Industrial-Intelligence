// ==========================================
// MOIL AI - EXPLORATION GIS MAP
// ==========================================

let map = null;
let explorationLayer = null;
let topPriorityLayer = null;

// ==========================================
// PRIORITY COLOR
// ==========================================

function getPriorityColor(priority) {
  const value = String(priority || "LOW").toUpperCase();

  if (value === "HIGH") {
    return "#ef4444";
  }

  if (value === "MODERATE") {
    return "#f59e0b";
  }

  return "#22c55e";
}

// ==========================================
// INITIALIZE MAP
// ==========================================

function initializeMap() {
  console.log("Initializing Leaflet map...");

  const mapElement = document.getElementById("mapCanvas");

  if (!mapElement) {
    console.error("ERROR: mapCanvas element not found!");

    return;
  }

  // Prevent duplicate initialization

  if (map !== null) {
    console.log("Map already initialized.");

    return;
  }

  map = L.map("mapCanvas").setView([21.5, 85.5], 13);

  // ======================================
  // OPENSTREETMAP BASE LAYER
  // ======================================

  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

    {
      maxZoom: 19,

      attribution: "&copy; OpenStreetMap contributors",
    },
  ).addTo(map);

  // ======================================
  // LAYERS
  // ======================================

  explorationLayer = L.layerGroup().addTo(map);

  topPriorityLayer = L.layerGroup().addTo(map);

  console.log("Map initialized successfully!");

  // Important: force Leaflet to calculate size

  setTimeout(
    function () {
      map.invalidateSize();
    },

    500,
  );
}

// ==========================================
// CLEAR MAP
// ==========================================

function clearMapLayers() {
  if (explorationLayer) {
    explorationLayer.clearLayers();
  }

  if (topPriorityLayer) {
    topPriorityLayer.clearLayers();
  }
}

// ==========================================
// DRAW EXPLORATION ZONES
// ==========================================

function drawExplorationZones(zones) {
  console.log("Drawing exploration zones:", zones);

  if (!Array.isArray(zones)) {
    console.error("Zones is not an array:", zones);

    return;
  }

  zones.forEach(function (zone) {
    // ==================================
    // CHECK REQUIRED COORDINATES
    // ==================================

    if (
      zone.min_lat === undefined ||
      zone.min_lon === undefined ||
      zone.max_lat === undefined ||
      zone.max_lon === undefined
    ) {
      console.warn("Zone missing boundary coordinates:", zone);

      return;
    }

    const color = getPriorityColor(zone.PRIORITY);

    const bounds = [
      [Number(zone.min_lat), Number(zone.min_lon)],

      [Number(zone.max_lat), Number(zone.max_lon)],
    ];

    const rectangle = L.rectangle(
      bounds,

      {
        color: color,

        weight: 1,

        fillColor: color,

        fillOpacity: 0.45,
      },
    );

    // ==================================
    // SAFE VALUES
    // ==================================

    const score =
      zone.PROSPECTIVITY_SCORE !== undefined
        ? Number(zone.PROSPECTIVITY_SCORE).toFixed(2)
        : "N/A";

    const distance =
      zone.DISTANCE_TO_MN_KM !== undefined
        ? Number(zone.DISTANCE_TO_MN_KM).toFixed(2)
        : "N/A";

    // ==================================
    // POPUP
    // ==================================

    rectangle.bindPopup(
      `
            <div style="min-width:200px">

                <h6>
                    ${zone.zone_id || "Zone"}
                </h6>

                <hr>

                <b>Priority:</b>
                ${zone.PRIORITY || "Unknown"}

                <br><br>

                <b>Prospectivity:</b>
                ${score}

                <br><br>

                <b>Nearest Mn Site:</b>
                ${zone.NEAREST_MN_SITE || "Unknown"}

                <br><br>

                <b>Distance:</b>
                ${distance} km

            </div>
            `,
    );

    rectangle.on(
      "click",

      function () {
        showZoneDetails(zone);
      },
    );

    rectangle.addTo(explorationLayer);
  });
}

// ==========================================
// DRAW TOP PRIORITY ZONES
// ==========================================

function drawTopPriorityZones(zones) {
  console.log("Drawing top priority zones:", zones);

  if (!Array.isArray(zones)) {
    return;
  }

  zones.forEach(function (zone, index) {
    // Check coordinates

    if (zone.center_lat === undefined || zone.center_lon === undefined) {
      console.warn("Top zone missing center coordinates:", zone);

      return;
    }

    const marker = L.circleMarker(
      [Number(zone.center_lat), Number(zone.center_lon)],

      {
        radius: 8,

        color: "#ffffff",

        weight: 2,

        fillColor: "#ef4444",

        fillOpacity: 1,
      },
    );

    marker.bindPopup(
      `
                <div>

                    <h6>
                        TOP ${index + 1}
                    </h6>

                    <b>
                        ${zone.zone_id || "Zone"}
                    </b>

                    <br><br>

                    <b>Score:</b>

                    ${
                      zone.PROSPECTIVITY_SCORE !== undefined
                        ? Number(zone.PROSPECTIVITY_SCORE).toFixed(2)
                        : "N/A"
                    }

                    <br><br>

                    <b>Priority:</b>

                    ${zone.PRIORITY || "Unknown"}

                </div>
                `,
    );

    marker.on(
      "click",

      function () {
        showZoneDetails(zone);
      },
    );

    marker.addTo(topPriorityLayer);
  });
}

// ==========================================
// SHOW ZONE DETAILS
// ==========================================

function showZoneDetails(zone) {
  const detailsElement = document.getElementById("featureDetails");

  if (!detailsElement) {
    return;
  }

  detailsElement.innerHTML = `
        <div class="border p-3 rounded">

            <h6 class="text-warning">

                ${zone.zone_id || "Zone"}

            </h6>

            <hr>

            <p>
                <b>Priority:</b>
                ${zone.PRIORITY || "Unknown"}
            </p>

            <p>
                <b>Prospectivity:</b>
                ${zone.PROSPECTIVITY_SCORE || "N/A"}
            </p>

            <p>
                <b>Elevation:</b>
                ${zone.ELEVATION_M || "N/A"} m
            </p>

            <p>
                <b>Slope:</b>
                ${zone.SLOPE_DEG || "N/A"}°
            </p>

            <p>
                <b>Nearest Mn Site:</b>
                ${zone.NEAREST_MN_SITE || "Unknown"}
            </p>

            <p>
                <b>Distance:</b>
                ${zone.DISTANCE_TO_MN_KM || "N/A"} km
            </p>

        </div>
        `;
}

// ==========================================
// DISPLAY ANALYSIS RESULTS
// ==========================================

function displayAnalysisResults(result) {
  console.log("DISPLAY ANALYSIS RESULTS:", result);

  if (!map) {
    console.error("Map has not been initialized!");

    initializeMap();
  }

  clearMapLayers();

  // ======================================
  // GET ALL ZONES
  // ======================================

  const zones =
    result.exploration_results ||
    result.zones ||
    result.all_zones ||
    result.top_zones ||
    [];

  console.log("TOTAL ZONES RECEIVED:", zones.length);

  // ======================================
  // DRAW ZONES
  // ======================================

  drawExplorationZones(zones);

  // ======================================
  // DRAW TOP ZONES
  // ======================================

  drawTopPriorityZones(result.top_zones || []);

  // ======================================
  // CENTER MAP
  // ======================================

  if (
    result.location &&
    result.location.latitude !== undefined &&
    result.location.longitude !== undefined
  ) {
    const latitude = Number(result.location.latitude);

    const longitude = Number(result.location.longitude);

    console.log("Centering map:", latitude, longitude);

    map.setView(
      [latitude, longitude],

      13,
    );
  }

  // Force map redraw

  setTimeout(
    function () {
      map.invalidateSize();
    },

    300,
  );
}

// ==========================================
// RESET MAP VIEW
// ==========================================

function resetMapView() {
  if (!map) {
    return;
  }

  map.setView(
    [21.5, 85.5],

    13,
  );

  map.invalidateSize();
}

// ==========================================
// LAYER CONTROLS
// ==========================================

function setupLayerControls() {
  const zonesCheckbox = document.getElementById("layerZones");

  const topZonesCheckbox = document.getElementById("layerTopZones");

  if (zonesCheckbox) {
    zonesCheckbox.addEventListener(
      "change",

      function () {
        if (this.checked) {
          map.addLayer(explorationLayer);
        } else {
          map.removeLayer(explorationLayer);
        }
      },
    );
  }

  if (topZonesCheckbox) {
    topZonesCheckbox.addEventListener(
      "change",

      function () {
        if (this.checked) {
          map.addLayer(topPriorityLayer);
        } else {
          map.removeLayer(topPriorityLayer);
        }
      },
    );
  }
}

// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
  "DOMContentLoaded",

  function () {
    console.log("Loading Exploration Map...");

    initializeMap();

    setupLayerControls();
  },
);
