const API_URL =
    "https://phishing-api-6xwr.onrender.com/predict";

async function checkPhishing() {

    const url =
        document
        .getElementById("urlInput")
        .value
        .trim();

    const resultBox =
        document.getElementById("result");

    // URL 형식 검사
    if (
        !url.startsWith("http://") &&
        !url.startsWith("https://")
    ) {

        resultBox.innerHTML = `

            <div class="result-card">

                <p style="
                    color:#dc2626;
                    font-weight:600;
                ">

                    Please enter a valid URL
                    including https://

                </p>

            </div>

        `;

        return;
    }

    // 로딩 화면
    resultBox.innerHTML = `

        <div class="result-card">

            <div class="loader"></div>

            <p style="
                text-align:center;
                margin-top:18px;
                color:#6b7280;
            ">
                AI is analyzing the URL...
            </p>

        </div>

    `;

    try {

        const response = await fetch(
            API_URL,
            {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    url: url
                })
            }
        );

        if (!response.ok) {
            throw new Error("API Error");
        }

        const data = await response.json();

        const resultColor =
            data.result.includes("피싱")
            ? "#dc2626"
            : "#16a34a";

        resultBox.innerHTML = `

            <div style="
                animation:fadeIn 0.4s ease;
            ">

                <div class="result-card">

                    <div
                        class="result-title"
                        style="
                            color:${resultColor};
                        "
                    >

                        ${data.result}

                    </div>

                    <p>
                        <strong>
                            Normal Probability:
                        </strong>

                        ${data.normal_prob}%
                    </p>

                    <p style="
                        margin-top:10px;
                    ">
                        <strong>
                            Phishing Probability:
                        </strong>

                        ${data.phishing_prob}%
                    </p>

                </div>

                <div class="result-card">

                    <div
                        class="section-title"
                        style="
                            color:#dc2626;
                        "
                    >

                        Risk Factors

                    </div>

                    <ul>

                        ${data.danger_reasons.length > 0

                            ? data.danger_reasons.map(
                                item => `
                                    <li style="
                                        color:#b91c1c;
                                    ">
                                        ${item}
                                    </li>
                                `
                            ).join("")

                            :

                            `
                                <li style="
                                    color:#16a34a;
                                ">
                                    No dangerous factors detected
                                </li>
                            `
                        }

                    </ul>

                </div>

                <div class="result-card">

                    <div
                        class="section-title"
                        style="
                            color:#16a34a;
                        "
                    >

                        Safe Factors

                    </div>

                    <ul>

                        ${data.safe_reasons.map(
                            item => `
                                <li style="
                                    color:#15803d;
                                ">
                                    ${item}
                                </li>
                            `
                        ).join("")}

                    </ul>

                </div>

                <div class="result-card">

                    <div class="section-title">

                        URL Feature Analysis

                    </div>

                    <img
                        class="graph-img"
                        src="
                            data:image/png;base64,
                            ${data.feature_plot}
                        "
                    >

                </div>

            </div>

        `;

    } catch (error) {

        console.error(error);

        resultBox.innerHTML = `

            <div class="result-card">

                <p style="
                    color:#dc2626;
                    font-weight:600;
                    line-height:1.8;
                ">

                    Failed to connect to server.<br>

                    Render free server may take
                    30~60 seconds on first request.

                </p>

            </div>

        `;
    }
}
