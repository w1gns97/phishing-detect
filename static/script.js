const API_URL = "https://phishing-api-6xwr.onrender.com/predict";

async function checkPhishing() {

    const url = document.getElementById("urlInput").value.trim();

    const resultBox = document.getElementById("result");

    // URL 형식 검사
    if (
        !url.startsWith("http://") &&
        !url.startsWith("https://")
    ) {

        resultBox.innerHTML = `
            <div style="
                color:#dc2626;
                font-weight:600;
                padding:16px;
            ">
                올바른 URL 형식을 입력하세요.<br>
                (https:// 포함)
            </div>
        `;

        return;
    }

    // 로딩 화면
    resultBox.innerHTML = `

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            padding:30px;
        ">

            <div class="loader"></div>

            <p style="
                margin-top:18px;
                color:#374151;
                font-weight:500;
            ">
                AI가 URL을 분석중입니다...
            </p>

        </div>

    `;

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        if (!response.ok) {
            throw new Error("API Error");
        }

        const data = await response.json();

        // 결과 색상
        const resultColor =
            data.result.includes("피싱")
            ? "#dc2626"
            : "#16a34a";

        // 위험도 계산
        const riskPercent = data.phishing_prob;

        resultBox.innerHTML = `

            <div style="
                animation:fadeIn 0.4s ease;
            ">

                <h2 style="
                    margin-bottom:20px;
                    color:#111827;
                    font-size:32px;
                    font-weight:700;
                ">
                    분석 결과
                </h2>

                <div style="
                    background:rgba(255,255,255,0.65);
                    border-radius:24px;
                    padding:24px;
                    margin-bottom:22px;
                    box-shadow:
                        0 8px 24px rgba(0,0,0,0.05);
                ">

                    <p style="
                        font-size:28px;
                        font-weight:700;
                        color:${resultColor};
                        margin-bottom:16px;
                    ">
                        ${data.result}
                    </p>

                    <div style="
                        margin-bottom:16px;
                    ">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            margin-bottom:8px;
                        ">
                            <span>피싱 위험도</span>
                            <span>${riskPercent}%</span>
                        </div>

                        <div style="
                            width:100%;
                            height:16px;
                            background:#e5e7eb;
                            border-radius:999px;
                            overflow:hidden;
                        ">

                            <div style="
                                width:${riskPercent}%;
                                height:100%;
                                background:
                                    linear-gradient(
                                        90deg,
                                        #f59e0b,
                                        #dc2626
                                    );
                                border-radius:999px;
                                transition:1s ease;
                            ">
                            </div>

                        </div>

                    </div>

                    <p style="
                        font-size:18px;
                        margin-top:18px;
                        color:#374151;
                    ">
                        정상 확률:
                        <strong>${data.normal_prob}%</strong>
                    </p>

                    <p style="
                        font-size:18px;
                        margin-top:8px;
                        color:#374151;
                    ">
                        피싱 확률:
                        <strong>${data.phishing_prob}%</strong>
                    </p>

                </div>

                <!-- 위험 요소 -->

                <div style="
                    background:rgba(255,255,255,0.6);
                    border-radius:24px;
                    padding:24px;
                    margin-bottom:20px;
                    text-align:left;
                ">

                    <h3 style="
                        color:#dc2626;
                        margin-bottom:14px;
                        font-size:22px;
                    ">
                        위험 요소
                    </h3>

                    <ul style="
                        padding-left:20px;
                        line-height:1.9;
                    ">

                        ${data.danger_reasons.length > 0

                            ? data.danger_reasons.map(item => `
                                <li style="
                                    color:#b91c1c;
                                    font-weight:500;
                                ">
                                    ${item}
                                </li>
                            `).join("")

                            : `
                                <li style="color:#16a34a;">
                                    위험 요소가 발견되지 않았습니다
                                </li>
                            `
                        }

                    </ul>

                </div>

                <!-- 정상 요소 -->

                <div style="
                    background:rgba(255,255,255,0.6);
                    border-radius:24px;
                    padding:24px;
                    margin-bottom:20px;
                    text-align:left;
                ">

                    <h3 style="
                        color:#16a34a;
                        margin-bottom:14px;
                        font-size:22px;
                    ">
                        정상 요소
                    </h3>

                    <ul style="
                        padding-left:20px;
                        line-height:1.9;
                    ">

                        ${data.safe_reasons.map(item => `
                            <li style="
                                color:#15803d;
                                font-weight:500;
                            ">
                                ${item}
                            </li>
                        `).join("")}

                    </ul>

                </div>

                <!-- 그래프 -->

                <div style="
                    background:rgba(255,255,255,0.6);
                    border-radius:24px;
                    padding:24px;
                ">

                    <h3 style="
                        margin-bottom:20px;
                        font-size:22px;
                        color:#111827;
                    ">
                        URL 특징 분석 시각화
                    </h3>

                    <img
                        src="data:image/png;base64,${data.feature_plot}"
                        width="100%"
                        style="
                            border-radius:18px;
                            box-shadow:
                                0 10px 20px rgba(0,0,0,0.06);
                        "
                    >

                </div>

            </div>

        `;

    } catch (error) {

        console.error(error);

        resultBox.innerHTML = `

            <div style="
                padding:24px;
                color:#dc2626;
                font-weight:600;
                line-height:1.8;
            ">

                서버 연결 실패<br>

                Render 무료 서버는 처음 요청 시
                30~60초 정도 걸릴 수 있습니다.

            </div>

        `;
    }
}
