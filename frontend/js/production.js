// ==========================================
// MOIL AI — DYNAMIC PRODUCTION INTELLIGENCE
// ==========================================


// ==========================================
// GLOBAL VARIABLES
// ==========================================

let productionChart = null;

let forecastData = [];

let selectedForecastYear = null;


// ==========================================
// AUTHENTICATION
// ==========================================

MOILAPI.requireAuth();


// ==========================================
// FORMAT TONNES
// ==========================================

function formatTonnes(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "--";

    }


    return Number(value)
        .toLocaleString(

            "en-IN",

            {

                maximumFractionDigits:
                    0

            }

        );

}


// ==========================================
// FORMAT COMPACT TONNES
// ==========================================

function formatCompact(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "--";

    }


    if (
        value >= 1000000
    ) {

        return (

            (
                value /
                1000000
            )
            .toFixed(2)

            +

            "M t"

        );

    }


    if (
        value >= 1000
    ) {

        return (

            (
                value /
                1000
            )
            .toFixed(1)

            +

            "K t"

        );

    }


    return value + " t";

}


// ==========================================
// LOAD USER
// ==========================================

function loadUser() {

    const user =
        MOILAPI.getCurrentUser();


    const userElement =
        document.getElementById(
            "userName"
        );


    if (
        user &&
        userElement
    ) {

        userElement.innerHTML =
            `
            <i class="bi bi-person-circle"></i>

            <span>

            ${user.name || user.email}

            </span>
            `;

    }

}


// ==========================================
// LOAD AVAILABLE YEARS
// ==========================================

async function loadForecastYears() {

    try {

        const data =
            await MOILAPI.productionYears();


        const select =
            document.getElementById(
                "forecastYearSelect"
            );


        if (
            !select
        ) {

            console.error(
                "Forecast year selector not found."
            );

            return;

        }


        select.innerHTML =
            "";


        const defaultYear =
            data.default_forecast_year;


        selectedForecastYear =
            defaultYear;


        // --------------------------------------
        // ADD FORECAST YEARS
        // --------------------------------------

        // Show the default forecast year
        // and several future years.

        const numberOfYears =
            5;


        for (

            let i = 0;

            i < numberOfYears;

            i++

        ) {

            const year =
                defaultYear + i;


            const option =
                document.createElement(
                    "option"
                );


            option.value =
                year;


            option.textContent =
                `${year} Forecast`;


            if (
                year === defaultYear
            ) {

                option.selected =
                    true;

            }


            select.appendChild(
                option
            );

        }


        // --------------------------------------
        // YEAR CHANGE EVENT
        // --------------------------------------

        select.addEventListener(

            "change",

            async function () {

                selectedForecastYear =
                    Number(
                        select.value
                    );


                await reloadProductionData();

            }

        );


    }

    catch (
        error
    ) {

        console.error(
            "Unable to load forecast years:",
            error
        );

    }

}


// ==========================================
// LOAD SUMMARY
// ==========================================

async function loadSummary() {

    try {

        const data =
            await MOILAPI.productionSummary(

                selectedForecastYear

            );


        // --------------------------------------
        // HISTORICAL 2024
        // --------------------------------------

        const production2024 =
            document.getElementById(
                "production2024"
            );


        if (
            production2024
        ) {

            production2024.textContent =
                formatCompact(
                    data.total_2024_tonnes
                );

        }


        // --------------------------------------
        // HISTORICAL 2025
        // --------------------------------------

        const production2025 =
            document.getElementById(
                "production2025"
            );


        if (
            production2025
        ) {

            production2025.textContent =
                formatCompact(
                    data.total_2025_tonnes
                );

        }


        // --------------------------------------
        // GROWTH
        // --------------------------------------

        const growth =
            document.getElementById(
                "growth"
            );


        if (
            growth
        ) {

            const growthValue =
                data.growth_2025_vs_2024_pct;


            growth.textContent =
                growthValue !== null &&
                growthValue !== undefined

                    ?

                    `${growthValue}%`

                    :

                    "--";

        }


        // --------------------------------------
        // FORECAST
        // --------------------------------------

        const forecastElement =
            document.getElementById(
                "forecast2026"
            );


        if (
            forecastElement
        ) {

            forecastElement.textContent =
                formatCompact(

                    data.forecast_2026_total_tonnes

                );

        }


        // --------------------------------------
        // DYNAMIC LABEL
        // --------------------------------------

        const forecastLabel =
            document.getElementById(
                "forecastLabel"
            );


        if (
            forecastLabel
        ) {

            forecastLabel.textContent =
                `${selectedForecastYear} Forecast`;

        }


        // --------------------------------------
        // PRODUCTION CHART TITLE
        // --------------------------------------

        const chartTitle =
            document.getElementById(
                "productionChartTitle"
            );


        if (
            chartTitle
        ) {

            chartTitle.textContent =
                `Historical Production + ${selectedForecastYear} Forecast`;

        }


        // --------------------------------------
        // SHORTFALL TITLE
        // --------------------------------------

        const shortfallTitle =
            document.getElementById(
                "shortfallTitle"
            );


        if (
            shortfallTitle
        ) {

            shortfallTitle.textContent =
                `${selectedForecastYear} Target vs Forecast`;

        }


        // --------------------------------------
        // MODEL INFORMATION
        // --------------------------------------

        const model =
            data.model;


        const modelInfo =
            document.getElementById(
                "modelInfo"
            );


        if (
            model &&
            modelInfo
        ) {

            modelInfo.innerHTML =
                `

                <div class="row g-3">


                    <div class="col-md-3">


                        <div class="model-item">


                            <span>

                            Selected Model

                            </span>


                            <strong>

                            ${model.selected || "--"}

                            </strong>


                        </div>


                    </div>



                    <div class="col-md-3">


                        <div class="model-item">


                            <span>

                            Backtest Period

                            </span>


                            <strong>

                            ${model.backtest_period || "--"}

                            </strong>


                        </div>


                    </div>



                    <div class="col-md-3">


                        <div class="model-item">


                            <span>

                            MAE

                            </span>


                            <strong>

                            ${formatTonnes(
                                model.mae_tonnes
                            )} t

                            </strong>


                        </div>


                    </div>



                    <div class="col-md-3">


                        <div class="model-item">


                            <span>

                            Forecast Method

                            </span>


                            <strong>

                            ${model.note || "--"}

                            </strong>


                        </div>


                    </div>


                </div>

                `;

        }


    }

    catch (
        error
    ) {

        console.error(
            "Unable to load production summary:",
            error
        );

    }

}


// ==========================================
// LOAD HISTORY
// ==========================================

async function loadHistory() {

    try {

        const history =
            await MOILAPI.productionHistory();


        return history;

    }

    catch (
        error
    ) {

        console.error(
            "Unable to load history:",
            error
        );


        return [];

    }

}


// ==========================================
// LOAD FORECAST
// ==========================================

async function loadForecast() {

    try {

        forecastData =
            await MOILAPI.productionForecast(

                selectedForecastYear

            );


        populateTargetMonths();


        return forecastData;

    }

    catch (
        error
    ) {

        console.error(
            "Unable to load forecast:",
            error
        );


        forecastData =
            [];


        return [];

    }

}


// ==========================================
// POPULATE TARGET MONTHS
// ==========================================

function populateTargetMonths() {

    const select =
        document.getElementById(
            "targetMonth"
        );


    if (
        !select
    ) {

        return;

    }


    select.innerHTML =
        "";


    forecastData.forEach(

        row => {


            const option =
                document.createElement(
                    "option"
                );


            option.value =
                row.month;


            option.textContent =
                row.month;


            select.appendChild(
                option
            );


        }

    );

}


// ==========================================
// CREATE PRODUCTION CHART
// ==========================================

function createChart(

    history,

    forecast

) {

    const canvas =
        document.getElementById(
            "productionChart"
        );


    if (
        !canvas
    ) {

        console.error(
            "Production chart canvas not found."
        );


        return;

    }


    // --------------------------------------
    // HISTORY
    // --------------------------------------

    const historyLabels =
        history.map(

            row =>
                row.month

        );


    const historyValues =
        history.map(

            row =>
                row.production_tonnes

        );


    // --------------------------------------
    // FORECAST
    // --------------------------------------

    const forecastLabels =
        forecast.map(

            row =>
                row.month

        );


    const forecastValues =
        forecast.map(

            row =>
                row.forecast_tonnes

        );


    // --------------------------------------
    // COMBINED LABELS
    // --------------------------------------

    const labels =
        [

            ...historyLabels,

            ...forecastLabels

        ];


    // --------------------------------------
    // HISTORICAL DATASET
    // --------------------------------------

    const historicalDataset =
        [

            ...historyValues,


            ...Array(

                forecastValues.length

            ).fill(

                null

            )

        ];


    // --------------------------------------
    // FORECAST DATASET
    // --------------------------------------

    const forecastDataset =
        [

            ...Array(

                historyValues.length

            ).fill(

                null

            ),


            ...forecastValues

        ];


    // --------------------------------------
    // DESTROY OLD CHART
    // --------------------------------------

    if (
        productionChart
    ) {

        productionChart.destroy();

    }


    // --------------------------------------
    // CREATE NEW CHART
    // --------------------------------------

    productionChart =
        new Chart(

            canvas,

            {

                type:
                    "line",


                data:
                    {


                        labels,


                        datasets:
                            [


                                {

                                    label:
                                        "Historical Production",


                                    data:
                                        historicalDataset,


                                    borderWidth:
                                        3,


                                    tension:
                                        0.3,


                                    spanGaps:
                                        true


                                },


                                {

                                    label:
                                        `${selectedForecastYear} Forecast`,


                                    data:
                                        forecastDataset,


                                    borderWidth:
                                        3,


                                    borderDash:
                                        [

                                            8,

                                            5

                                        ],


                                    tension:
                                        0.3,


                                    spanGaps:
                                        true


                                }


                            ]


                    },


                options:
                    {


                        responsive:
                            true,


                        maintainAspectRatio:
                            false,


                        plugins:
                            {


                                legend:
                                    {


                                        position:
                                            "top"


                                    },


                                tooltip:
                                    {


                                        callbacks:
                                            {


                                                label:

                                                function (

                                                    context

                                                ) {


                                                    const value =
                                                        context.raw;


                                                    if (

                                                        value === null

                                                    ) {

                                                        return "";

                                                    }


                                                    return (

                                                        context.dataset.label

                                                        +

                                                        ": "

                                                        +

                                                        formatTonnes(
                                                            value
                                                        )

                                                        +

                                                        " tonnes"

                                                    );


                                                }


                                            }


                                    }


                            },


                        scales:
                            {


                                y:
                                    {


                                        ticks:
                                            {


                                                callback:

                                                function (

                                                    value

                                                ) {


                                                    return (

                                                        value /
                                                        1000

                                                    )

                                                    +

                                                    "K";


                                                }


                                            }


                                    }


                            }


                    }


            }

        );

}


// ==========================================
// LOAD SHORTFALL
// ==========================================

async function loadShortfall() {

    try {

        const data =
            await MOILAPI.productionShortfall(

                selectedForecastYear

            );


        const table =
            document.getElementById(
                "shortfallTable"
            );


        if (
            !table
        ) {

            return;

        }


        table.innerHTML =
            "";


        data.forEach(

            row => {


                let badgeClass =
                    "bg-secondary";


                if (
                    row.status ===
                    "On track"
                ) {

                    badgeClass =
                        "bg-success";

                }


                else if (
                    row.status ===
                    "At risk of shortfall"
                ) {

                    badgeClass =
                        "bg-danger";

                }


                const shortfall =
                    row.shortfall_tonnes !==
                    null

                        ?

                        formatTonnes(

                            row.shortfall_tonnes

                        )

                        +

                        " t"

                        :

                        "--";


                const target =
                    row.approved_target_tonnes !==
                    null

                        ?

                        formatTonnes(

                            row.approved_target_tonnes

                        )

                        +

                        " t"

                        :

                        "--";


                const tr =
                    document.createElement(
                        "tr"
                    );


                tr.innerHTML =
                    `

                    <td>

                    ${row.month}

                    </td>


                    <td>

                    ${formatTonnes(
                        row.forecast_tonnes
                    )} t

                    </td>


                    <td>

                    ${target}

                    </td>


                    <td>

                    ${shortfall}

                    </td>


                    <td>


                        <span
                            class="badge ${badgeClass}">


                            ${row.status}


                        </span>


                    </td>

                    `;


                table.appendChild(
                    tr
                );


            }

        );


    }

    catch (
        error
    ) {

        console.error(
            "Unable to load shortfall:",
            error
        );

    }

}


// ==========================================
// SET TARGET
// ==========================================

async function setTarget() {

    const month =
        document
            .getElementById(
                "targetMonth"
            )
            .value;


    const tonnes =
        Number(

            document
                .getElementById(
                    "targetTonnes"
                )
                .value

        );


    const message =
        document.getElementById(
            "targetMessage"
        );


    if (

        !month ||

        !tonnes ||

        tonnes <= 0

    ) {

        message.innerHTML =
            `

            <div
                class="alert alert-warning">


                Please select a month and enter
                a valid production target.


            </div>

            `;


        return;

    }


    try {


        await MOILAPI.setProductionTarget(

            month,

            tonnes

        );


        message.innerHTML =
            `

            <div
                class="alert alert-success">


                Production target saved successfully.


            </div>

            `;


        document
            .getElementById(
                "targetTonnes"
            )
            .value =
            "";


        await loadShortfall();


        await loadAlerts();


    }

    catch (
        error
    ) {


        console.error(
            error
        );


        message.innerHTML =
            `

            <div
                class="alert alert-danger">


                ${error.message}


            </div>

            `;


    }

}


// ==========================================
// LOAD ALERTS
// ==========================================

async function loadAlerts() {

    try {

        const alerts =
            await MOILAPI.productionAlerts(

                selectedForecastYear

            );


        const container =
            document.getElementById(
                "alertsContainer"
            );


        if (
            !container
        ) {

            return;

        }


        container.innerHTML =
            "";


        // --------------------------------------
        // NO ALERTS
        // --------------------------------------

        if (

            !alerts ||

            alerts.length === 0

        ) {


            container.innerHTML =
                `

                <div
                    class="alert alert-success">


                    <i
                        class="bi bi-check-circle">

                    </i>


                    No significant production risks
                    detected for ${selectedForecastYear}.


                </div>

                `;


            return;

        }


        // --------------------------------------
        // DISPLAY ALERTS
        // --------------------------------------

        alerts.forEach(

            alert => {


                let icon =
                    "bi-info-circle";


                let alertClass =
                    "alert-info";


                if (

                    alert.severity ===
                    "high"

                ) {


                    icon =
                        "bi-exclamation-triangle";


                    alertClass =
                        "alert-danger";


                }


                else if (

                    alert.severity ===
                    "medium"

                ) {


                    icon =
                        "bi-exclamation-circle";


                    alertClass =
                        "alert-warning";


                }


                else if (

                    alert.severity ===
                    "low"

                ) {


                    icon =
                        "bi-info-circle";


                    alertClass =
                        "alert-info";


                }


                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    `alert ${alertClass}`;


                div.innerHTML =
                    `

                    <i
                        class="bi ${icon}">

                    </i>


                    <strong>

                    ${alert.type}:

                    </strong>


                    ${alert.message}

                    `;


                container.appendChild(
                    div
                );


            }

        );


    }

    catch (
        error
    ) {

        console.error(
            "Unable to load alerts:",
            error
        );

    }

}


// ==========================================
// RELOAD PRODUCTION DATA
// ==========================================

async function reloadProductionData() {

    try {


        // --------------------------------------
        // LOAD FORECAST
        // --------------------------------------

        const forecast =
            await loadForecast();


        // --------------------------------------
        // LOAD HISTORY
        // --------------------------------------

        const history =
            await loadHistory();


        // --------------------------------------
        // CREATE CHART
        // --------------------------------------

        createChart(

            history,

            forecast

        );


        // --------------------------------------
        // LOAD OTHER DATA
        // --------------------------------------

        await Promise.all(

            [


                loadSummary(),


                loadShortfall(),


                loadAlerts()


            ]

        );


    }

    catch (
        error
    ) {

        console.error(
            "Unable to reload production data:",
            error
        );

    }

}


// ==========================================
// LOGOUT
// ==========================================

function logout() {

    MOILAPI.logout();

}


// ==========================================
// INITIALIZE PAGE
// ==========================================

async function initializeProduction() {

    try {


        // --------------------------------------
        // USER
        // --------------------------------------

        loadUser();


        // --------------------------------------
        // LOGOUT BUTTON
        // --------------------------------------

        const logoutButton =
            document.getElementById(
                "logoutBtn"
            );


        if (
            logoutButton
        ) {

            logoutButton.addEventListener(

                "click",

                logout

            );

        }


        // --------------------------------------
        // LOAD FORECAST YEARS
        // --------------------------------------

        await loadForecastYears();


        // --------------------------------------
        // LOAD PRODUCTION DATA
        // --------------------------------------

        await reloadProductionData();


        // --------------------------------------
        // SAVE TARGET BUTTON
        // --------------------------------------

        const saveTargetButton =
            document.getElementById(
                "saveTargetBtn"
            );


        if (
            saveTargetButton
        ) {

            saveTargetButton.addEventListener(

                "click",

                setTarget

            );

        }


    }

    catch (
        error
    ) {

        console.error(
            "Production initialization failed:",
            error
        );


        alert(

            "Unable to load Production Intelligence. "

            +

            error.message

        );

    }

}


// ==========================================
// START
// ==========================================

document.addEventListener(

    "DOMContentLoaded",

    initializeProduction

); 