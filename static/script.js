const API_URL = "https://phishing-api-6xwr.onrender.com";

async function checkPhishing() {
    const url = document.getElementById("urlInput").value;
    const resultBox = document.getElementById("result");

    resultBox.innerHTML = "분석 중입니다...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        resultBox.innerHTML = `
            <h3>분석 결과</h3>
            <p><strong>판단:</strong> ${data.result}</p>
            <p>정상 확률: ${data.normal_prob}%</p>
            <p>피싱 확률: ${data.phishing_prob}%</p>
            <img src="data:image/png;base64,${data.feature_plot}" width="100%">
        `;
    } catch (error) {
        resultBox.innerHTML = "서버 연결 실패";
    }
}
