// ==========================================
// MOIL AI - EXPLORATION PAGE CONTROLLER
// ==========================================

// ------------------------------------------
// HELPER
// ------------------------------------------

function getElement(id) {
    return document.getElementById(id);
}


// ------------------------------------------
// SAFE VALUE
// ------------------------------------------

function safeValue(value, fallback = "-") {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return fallback;
    }

    return value;
}


// ------------------------------------------
// FORMAT NUMBER
// ------------------------------------------

function formatNumber(value, decimals = 2) {

    if (
        value === null ||
        value === undefined ||
        value === "" ||
        isNaN(Number(value))
    ) {
        return "-";
    }

    return Number(value).toFixed(decimals);
}


// ------------------------------------------
// PRIORITY BADGE
// ------------------------------------------

function getPriorityClass(priority) {

    const value =
        String(priority || "").toLowerCase();

    if (value.includes("very high")) {
        return "bg-danger";
    }

    if (value.includes("high")) {
        return "bg-warning text-dark";
    }

    if (
        value.includes("moderate") ||
        value.includes("medium")
    ) {
        return "bg-info text-dark";
    }

    if (value.includes("low")) {
        return "bg-success";
    }

    return "bg-secondary";
}


// ------------------------------------------
// GET ZONE VALUE
// ------------------------------------------

function getZoneValue(
    zone,
    names,
    fallback = null
) {

    for (const name of names) {

        if (
            zone[name] !== undefined &&
            zone[name] !== null &&
            zone[name] !== ""
        ) {
            return zone[name];
        }
    }

    return fallback;
}


// ==========================================
// RENDER ALL 100 EXPLORATION ZONES
// ==========================================

function renderAllZones(data) {

    const table =
        getElement("allZonesTable");

    const count =
        getElement("allZonesCount");

    if (!table) {

        console.warn(
            "allZonesTable not found."
        );

        return;
    }


    let zones = [];


    // Backend sends the complete grid here
    if (
        data &&
        Array.isArray(
            data.exploration_zones
        )
    ) {

        zones =
            data.exploration_zones;
    }


    console.log(
        "Total exploration zones received:",
        zones.length
    );


    // Update badge
    if (count) {

        count.textContent =
            `${zones.length} Zones`;
    }


    // No zones
    if (zones.length === 0) {

        table.innerHTML = `
            <tr>
                <td
                    colspan="8"
                    class="text-center text-muted py-4"
                >
                    No exploration zones found.
                </td>
            </tr>
        `;

        return;
    }


    // Sort highest prospectivity first
    zones =
        [...zones].sort(
            function (a, b) {

                const scoreA =
                    Number(
                        getZoneValue(
                            a,
                            [
                                "PROSPECTIVITY_SCORE",
                                "prospectivity_score",
                                "prospectivity",
                                "score"
                            ],
                            0
                        )
                    );

                const scoreB =
                    Number(
                        getZoneValue(
                            b,
                            [
                                "PROSPECTIVITY_SCORE",
                                "prospectivity_score",
                                "prospectivity",
                                "score"
                            ],
                            0
                        )
                    );

                return scoreB - scoreA;
            }
        );


    let html = "";


    zones.forEach(
        function (zone, index) {

            const zoneId =
                getZoneValue(
                    zone,
                    [
                        "zone_id",
                        "ZONE_ID",
                        "id",
                        "ID"
                    ],
                    `ZONE_${String(
                        index + 1
                    ).padStart(3, "0")}`
                );


            const score =
                getZoneValue(
                    zone,
                    [
                        "PROSPECTIVITY_SCORE",
                        "prospectivity_score",
                        "prospectivity",
                        "score"
                    ],
                    0
                );


            const priority =
                getZoneValue(
                    zone,
                    [
                        "PRIORITY",
                        "priority",
                        "priority_level"
                    ],
                    "LOW"
                );


            const latitude =
                getZoneValue(
                    zone,
                    [
                        "latitude",
                        "lat",
                        "center_lat",
                        "min_lat"
                    ],
                    null
                );


            const longitude =
                getZoneValue(
                    zone,
                    [
                        "longitude",
                        "lon",
                        "center_lon",
                        "min_lon"
                    ],
                    null
                );


            const elevation =
                getZoneValue(
                    zone,
                    [
                        "elevation",
                        "elevation_m",
                        "ELEVATION",
                        "mean_elevation"
                    ],
                    null
                );


            const distance =
                getZoneValue(
                    zone,
                    [
                        "distance_to_manganese_km",
                        "distance_to_mn_km",
                        "distance_to_mn",
                        "DISTANCE_TO_MN_KM"
                    ],
                    null
                );


            html += `
                <tr>

                    <td>
                        ${index + 1}
                    </td>

                    <td>
                        <strong>
                            ${safeValue(zoneId)}
                        </strong>
                    </td>

                    <td>
                        <strong>
                            ${formatNumber(
                                score,
                                4
                            )}
                        </strong>
                    </td>

                    <td>

                        <span
                            class="badge ${getPriorityClass(
                                priority
                            )}"
                        >
                            ${safeValue(
                                priority
                            )}
                        </span>

                    </td>

                    <td>
                        ${formatNumber(
                            latitude,
                            6
                        )}
                    </td>

                    <td>
                        ${formatNumber(
                            longitude,
                            6
                        )}
                    </td>

                    <td>
                        ${formatNumber(
                            elevation,
                            2
                        )}
                    </td>

                    <td>
                        ${formatNumber(
                            distance,
                            2
                        )}
                    </td>

                </tr>
            `;
        }
    );


    table.innerHTML = html;


    console.log(
        "All exploration zones rendered:",
        zones.length
    );
}


// ==========================================
// UPDATE EXPLORATION PAGE
// ==========================================

function updateExplorationPage(data) {

    if (!data) {

        console.warn(
            "No exploration data received."
        );

        return;
    }


    console.log(
        "Updating Exploration page..."
    );


    // --------------------------------------
    // 1. Render 100-zone table
    // --------------------------------------

    renderAllZones(data);


    // --------------------------------------
    // 2. Update total zone counter
    // --------------------------------------

    const totalZones =
        getElement("totalZones");

    if (totalZones) {

        totalZones.textContent =
            safeValue(
                data.total_zones,
                Array.isArray(
                    data.exploration_zones
                )
                    ? data.exploration_zones.length
                    : 0
            );
    }


    // --------------------------------------
    // 3. Update map
    // --------------------------------------

    if (
        typeof clearMapLayers ===
        "function"
    ) {

        clearMapLayers();
    }


    if (
        typeof drawExplorationZones ===
        "function" &&
        Array.isArray(
            data.exploration_zones
        )
    ) {

        drawExplorationZones(
            data.exploration_zones
        );
    }


    if (
        typeof drawTopPriorityZones ===
        "function" &&
        Array.isArray(
            data.top_zones
        )
    ) {

        drawTopPriorityZones(
            data.top_zones
        );
    }


    console.log(
        "Exploration page updated successfully."
    );
}


// ==========================================
// RUN AI EXPLORATION ANALYSIS
// ==========================================

async function runExplorationAnalysis() {

    const button =
        getElement("analyzeButton");


    if (!button) {

        console.error(
            "Analyze button not found."
        );

        return;
    }


    // --------------------------------------
    // LOCATION
    // --------------------------------------

    const locationInput =
        getElement("locationInput");


    const location =
        locationInput
            ? locationInput.value.trim()
            : "Keonjhar, Odisha";


    // --------------------------------------
    // GRID SIZE
    // --------------------------------------

    const gridInput =
        getElement("gridSize");


    let gridSize = 10;


    if (gridInput) {

        const value =
            parseInt(
                gridInput.value,
                10
            );


        if (!isNaN(value)) {

            gridSize = value;
        }
    }


    const gridRows =
        gridSize;

    const gridCols =
        gridSize;


    // --------------------------------------
    // AREA BUFFER
    // --------------------------------------

    const bufferInput =
        getElement("bufferSize");


    let bufferDegrees =
        0.01;


    if (bufferInput) {

        const value =
            parseFloat(
                bufferInput.value
            );


        if (!isNaN(value)) {

            bufferDegrees =
                value;
        }
    }


    // --------------------------------------
    // BUTTON STATE
    // --------------------------------------

    const originalText =
        button.textContent;


    button.disabled = true;

    button.textContent =
        "Analyzing...";


    try {

        console.log(
            "================================"
        );

        console.log(
            "STARTING MOIL AI ANALYSIS"
        );

        console.log(
            "================================"
        );


        console.log(
            "Location:",
            location
        );


        console.log(
            "Grid:",
            gridRows,
            "x",
            gridCols
        );


        console.log(
            "Buffer:",
            bufferDegrees
        );


        // ----------------------------------
        // CHECK API
        // ----------------------------------

        if (
            !window.MOILAPI ||
            typeof
                window.MOILAPI.analyzeArea
                !== "function"
        ) {

            throw new Error(
                "MOILAPI.analyzeArea is not available."
            );
        }


        // ----------------------------------
        // CALL FASTAPI BACKEND
        // ----------------------------------

        const data =
            await window.MOILAPI.analyzeArea(
                location,
                bufferDegrees,
                gridRows,
                gridCols
            );


        console.log(
            "Backend response:",
            data
        );


        // ----------------------------------
        // VALIDATE RESPONSE
        // ----------------------------------

        if (
            !data ||
            data.status !== "success"
        ) {

            throw new Error(
                "Backend returned an unsuccessful response."
            );
        }


        // ----------------------------------
        // STORE RESPONSE
        // ----------------------------------

        window.lastExplorationData =
            data;


        // ----------------------------------
        // UPDATE EVERYTHING
        // ----------------------------------

        updateExplorationPage(
            data
        );


        console.log(
            "================================"
        );

        console.log(
            "AI ANALYSIS COMPLETED"
        );

        console.log(
            "================================"
        );


    } catch (error) {

        console.error(
            "Exploration analysis error:",
            error
        );


        alert(
            "Exploration analysis failed:\n\n" +
            error.message
        );


    } finally {

        button.disabled =
            false;

        button.textContent =
            originalText;
    }
}


// ==========================================
// PAGE INITIALIZATION
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "MOIL AI Exploration page loaded."
        );


        // ----------------------------------
        // INITIALIZE LEAFLET MAP
        // ----------------------------------

        if (
            typeof initializeMap ===
            "function"
        ) {

            initializeMap();

        } else {

            console.error(
                "initializeMap() not found."
            );
        }


        // ----------------------------------
        // CONNECT ANALYZE BUTTON
        // ----------------------------------

        const analyzeButton =
            getElement(
                "analyzeButton"
            );


        if (analyzeButton) {

            analyzeButton.addEventListener(
                "click",
                runExplorationAnalysis
            );


            console.log(
                "Analyze button connected successfully."
            );

        } else {

            console.error(
                "ERROR: analyzeButton not found."
            );
        }


        // ----------------------------------
        // RESTORE PREVIOUS DATA
        // ----------------------------------

        if (
            window.lastExplorationData
        ) {

            updateExplorationPage(
                window.lastExplorationData
            );
        }

    }
);