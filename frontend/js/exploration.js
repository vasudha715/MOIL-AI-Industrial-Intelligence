// ==========================================
// MOIL AI — EXPLORATION PAGE
// ==========================================


// ==========================================
// ELEMENT HELPERS
// ==========================================

function getElement(id) {
    return document.getElementById(id);
}


// ==========================================
// SAFE VALUE
// ==========================================

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


// ==========================================
// NUMBER FORMAT
// ==========================================

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


// ==========================================
// PRIORITY BADGE
// ==========================================

function getPriorityClass(priority) {

    const value = String(
        priority || ""
    ).toLowerCase();

    if (value.includes("very high")) {
        return "bg-danger";
    }

    if (value.includes("high")) {
        return "bg-warning text-dark";
    }

    if (value.includes("medium")) {
        return "bg-info text-dark";
    }

    if (value.includes("low")) {
        return "bg-success";
    }

    return "bg-secondary";
}


// ==========================================
// GET ZONE VALUE
// ==========================================

function getZoneValue(zone, names, fallback = null) {

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
// RENDER ALL EXPLORATION ZONES
// ==========================================

function renderAllZones(data) {

    const table =
        getElement("allZonesTable");

    const count =
        getElement("allZonesCount");


    if (!table) {

        console.warn(
            "allZonesTable element not found."
        );

        return;
    }


    // ======================================
    // BACKEND RETURNS:
    // data.exploration_zones
    // ======================================

    let zones = [];

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
        "Total exploration zones:",
        zones.length
    );


    // ======================================
    // UPDATE COUNT
    // ======================================

    if (count) {

        count.textContent =
            `${zones.length} Zones`;
    }


    // ======================================
    // NO DATA
    // ======================================

    if (!zones.length) {

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


    // ======================================
    // SORT BY PROSPECTIVITY SCORE
    // ======================================

    zones = [...zones].sort(
        (a, b) => {

            const scoreA = Number(
                getZoneValue(
                    a,
                    [
                        "PROSPECTIVITY_SCORE",
                        "prospectivity_score",
                        "prospectivity"
                    ],
                    0
                )
            );

            const scoreB = Number(
                getZoneValue(
                    b,
                    [
                        "PROSPECTIVITY_SCORE",
                        "prospectivity_score",
                        "prospectivity"
                    ],
                    0
                )
            );

            return scoreB - scoreA;
        }
    );


    // ======================================
    // BUILD TABLE
    // ======================================

    table.innerHTML = zones
        .map(
            (zone, index) => {

                const zoneId =
                    getZoneValue(
                        zone,
                        [
                            "ZONE_ID",
                            "zone_id",
                            "ZONE",
                            "zone",
                            "id"
                        ],
                        `Z${String(
                            index + 1
                        ).padStart(3, "0")}`
                    );


                const score =
                    getZoneValue(
                        zone,
                        [
                            "PROSPECTIVITY_SCORE",
                            "prospectivity_score",
                            "prospectivity"
                        ],
                        0
                    );


                const priority =
                    getZoneValue(
                        zone,
                        [
                            "PRIORITY",
                            "priority",
                            "PRIORITY_LEVEL",
                            "priority_level"
                        ],
                        "Unknown"
                    );


                const latitude =
                    getZoneValue(
                        zone,
                        [
                            "CENTER_LAT",
                            "center_lat",
                            "LATITUDE",
                            "latitude",
                            "lat"
                        ]
                    );


                const longitude =
                    getZoneValue(
                        zone,
                        [
                            "CENTER_LON",
                            "center_lon",
                            "LONGITUDE",
                            "longitude",
                            "lon"
                        ]
                    );


                const elevation =
                    getZoneValue(
                        zone,
                        [
                            "ELEVATION",
                            "elevation",
                            "ELEVATION_M",
                            "elevation_m"
                        ]
                    );


                const distance =
                    getZoneValue(
                        zone,
                        [
                            "DISTANCE_TO_MN_KM",
                            "distance_to_mn_km",
                            "DISTANCE_TO_MANGANESE_KM",
                            "distance_to_manganese_km"
                        ]
                    );


                return `
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
                                    2
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
                                    priority,
                                    "Unknown"
                                )}
                            </span>
                        </td>

                        <td>
                            ${formatNumber(
                                latitude,
                                5
                            )}
                        </td>

                        <td>
                            ${formatNumber(
                                longitude,
                                5
                            )}
                        </td>

                        <td>
                            ${formatNumber(
                                elevation,
                                1
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
        )
        .join("");
}


// ==========================================
// UPDATE EXPLORATION PAGE
// ==========================================

function updateExplorationPage(data) {

    console.log(
        "MOIL Exploration Response:",
        data
    );


    // ======================================
    // RENDER 100-ZONE TABLE
    // ======================================

    renderAllZones(data);


    // ======================================
    // UPDATE EXISTING STATISTICS
    // ======================================

    if (
        typeof updateExplorationStatistics ===
        "function"
    ) {

        updateExplorationStatistics(
            data
        );
    }


    // ======================================
    // UPDATE EXISTING MAP
    // ======================================

    if (
        typeof updateExplorationMap ===
        "function"
    ) {

        updateExplorationMap(
            data
        );

    }
    else if (
        typeof renderExplorationMap ===
        "function"
    ) {

        renderExplorationMap(
            data
        );
    }
}


// ==========================================
// RUN EXPLORATION ANALYSIS
// ==========================================

async function runExplorationAnalysis() {

    const locationInput =
        getElement("locationInput");

    const gridRowsInput =
        getElement("gridRows");

    const gridColsInput =
        getElement("gridCols");

    const bufferInput =
        getElement("bufferDegrees");

    const button =
        getElement("runAnalysisBtn");


    // ======================================
    // READ INPUTS
    // ======================================

    const location =
        locationInput
            ? locationInput.value.trim()
            : "Keonjhar, Odisha";


    const gridRows =
        gridRowsInput
            ? Number(
                gridRowsInput.value
            )
            : 10;


    const gridCols =
        gridColsInput
            ? Number(
                gridColsInput.value
            )
            : 10;


    const bufferDegrees =
        bufferInput
            ? Number(
                bufferInput.value
            )
            : 0.01;


    // ======================================
    // BUTTON LOADING STATE
    // ======================================

    if (button) {

        button.disabled = true;

        button.dataset.originalText =
            button.textContent;

        button.textContent =
            "Analyzing...";
    }


    try {

        // ==================================
        // CALL REAL MOIL API
        // ==================================

        if (
            !window.MOILAPI ||
            typeof window.MOILAPI.analyzeArea !==
            "function"
        ) {

            throw new Error(
                "MOIL API client is not available."
            );
        }


        const data =
            await window.MOILAPI.analyzeArea(
                location,
                bufferDegrees,
                gridRows,
                gridCols
            );


        console.log(
            "Exploration analysis completed:",
            data
        );


        // ==================================
        // UPDATE PAGE
        // ==================================

        updateExplorationPage(
            data
        );


        // ==================================
        // STORE LAST RESULT
        // ==================================

        window.lastExplorationData =
            data;


    }
    catch (error) {

        console.error(
            "Exploration analysis failed:",
            error
        );


        const table =
            getElement(
                "allZonesTable"
            );


        if (table) {

            table.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Exploration analysis failed:
                        ${safeValue(
                            error.message,
                            "Please try again."
                        )}
                    </td>
                </tr>
            `;
        }


        alert(
            "Exploration analysis failed. " +
            error.message
        );


    }
    finally {

        if (button) {

            button.disabled = false;

            button.textContent =
                button.dataset.originalText ||
                "Run AI Analysis";
        }
    }
}


// ==========================================
// PAGE INITIALIZATION
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "MOIL AI Exploration page loaded."
        );


        // ==================================
        // RUN ANALYSIS BUTTON
        // ==================================

        const button =
            getElement(
                "runAnalysisBtn"
            );


        if (button) {

            button.addEventListener(
                "click",
                runExplorationAnalysis
            );
        }


        // ==================================
        // RENDER EXISTING DATA
        // ==================================

        if (
            window.lastExplorationData
        ) {

            renderAllZones(
                window.lastExplorationData
            );
        }

    }
);