async function predictDisease() {
    const symptoms = document.getElementById("symptoms").value;
    const resultsDiv = document.getElementById("results");
    const loading = document.getElementById("loading");

    if (!symptoms.trim()) {
        resultsDiv.innerHTML = `
            <div class="result-card">
                <h2>⚠️ Input Required</h2>
                <p>Please enter symptoms before prediction.</p>
            </div>
        `;
        return;
    }

    resultsDiv.innerHTML = "";
    loading.style.display = "block";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict-disease", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symptoms: symptoms.trim()   // ✅ Trimmed before sending
            })
        });

        const data = await response.json();
        loading.style.display = "none";

        loadHistory();
        loadAnalytics();

        // ✅ Protect against empty predictions
        if (!data.predictions || data.predictions.length === 0) {
            resultsDiv.innerHTML = `
                <div class="result-card">
                    <h2>⚠️ No Prediction Found</h2>
                    <p>Unable to predict disease from the entered symptoms.</p>
                </div>
            `;
            return;
        }

        const topPrediction = data.predictions[0];
        const otherPredictions = data.predictions.slice(1);

        // 🟢 Risk Banner
        let riskBanner = "";
        if ((topPrediction.severity || "low").toLowerCase() === "high") {
            riskBanner = `
                <div class="risk-banner high-risk">
                    🔴 HIGH RISK DETECTED
                    <br>Consult a doctor immediately.
                </div>`;
        } else if ((topPrediction.severity || "low").toLowerCase() === "medium") {
            riskBanner = `
                <div class="risk-banner medium-risk">
                    🟡 MEDIUM RISK
                    <br>Monitor symptoms carefully.
                </div>`;
        } else {
            riskBanner = `
                <div class="risk-banner low-risk">
                    🟢 LOW RISK
                    <br>Basic precautions recommended.
                </div>`;
        }

        resultsDiv.innerHTML = riskBanner;

        const icons = {
            flu: "🤒", covid19: "🦠", dengue: "🦟", malaria: "🩸",
            diabetes: "🩺", hypertension: "❤️", asthma: "🫁", migraine: "🤕",
            bronchitis: "😮‍💨", heart_disease: "❤️", food_poisoning: "🤢",
            stress: "😓", common_cold: "🤧"
        };

        // 🏆 Top Prediction FIRST
        resultsDiv.innerHTML += `
            <div class="top-prediction">
                <h1>🏆 Top Prediction</h1>
                <h2>${icons[topPrediction.disease] || "🩺"} ${topPrediction.disease.toUpperCase()}</h2>
                <p>Confidence: <strong>${Number(topPrediction.confidence || 0).toFixed(2)}%</strong></p>
                <div class="progress"><div class="progress-fill" style="width:${Math.min(topPrediction.confidence || 0, 100)}%"></div></div>
                <span class="badge ${(topPrediction.severity || "Low").toLowerCase()}">${topPrediction.severity || "Low"}</span>
                <div class="section"><strong>Description:</strong><p>${topPrediction.description || "N/A"}</p></div>
                <div class="section"><strong>Recommended Doctor:</strong><p>${topPrediction.doctor || "General Physician"}</p></div>
                <div class="section"><strong>Medicines:</strong>
                    <ul>${
                        (topPrediction.medicines?.length)
                        ? topPrediction.medicines.map(m => `<li>${m}</li>`).join("")
                        : "<li>No medicines available</li>"
                    }</ul>
                </div>
                <div class="section"><strong>Precautions:</strong>
                    <ul>${
                        (topPrediction.precautions?.length)
                        ? topPrediction.precautions.map(p => `<li>${p}</li>`).join("")
                        : "<li>No precautions available</li>"
                    }</ul>
                </div>
            </div>
        `;

        // Other Predictions (safe handling)
        if (otherPredictions.length > 0) {
            resultsDiv.innerHTML += `<h2 class="other-title">Other Possible Diseases</h2>`;
            otherPredictions.forEach(prediction => {
                const severity = prediction.severity || "Low";
                let severityClass = "low";

                if (severity.toLowerCase() === "high") severityClass = "high";
                else if (severity.toLowerCase() === "medium") severityClass = "medium";

                resultsDiv.innerHTML += `
                    <div class="result-card">
                        <h2>${icons[prediction.disease] || "🩺"} ${prediction.disease.toUpperCase()}</h2>
                        <p>Confidence: <strong>${Number(prediction.confidence || 0).toFixed(2)}%</strong></p>
                        <div class="progress"><div class="progress-fill" style="width:${Math.min(prediction.confidence || 0, 100)}%"></div></div>
                        <span class="badge ${severityClass}">${severity}</span>
                        <div class="section"><strong>Description:</strong><p>${prediction.description || "N/A"}</p></div>
                        <div class="section"><strong>Recommended Doctor:</strong><p>${prediction.doctor || "General Physician"}</p></div>
                    </div>`;
            });
        }

        // 📄 Download Button ALWAYS
        resultsDiv.innerHTML += `
            <div style="text-align:center; margin-top:20px;">
                <a href="http://127.0.0.1:8000/download-report" target="_blank">
                    <button>📄 Download Medical Report</button>
                </a>
            </div>`;
    } catch (error) {
        loading.style.display = "none";
        resultsDiv.innerHTML = `
            <div class="result-card">
                <h2>❌ Connection Error</h2>
                <p>Unable to connect to backend API. Please retry or check server status.</p>
            </div>`;
        console.error(error);
    }
}

async function loadHistory() {
    const historyDiv = document.getElementById("history");
    if (!historyDiv) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/symptom-history");
        const data = await response.json();

        historyDiv.innerHTML = "";
        data.reverse().slice(0, 5).forEach(item => {
            historyDiv.innerHTML += `
                <div class="history-card">
                    <p><strong>Symptoms:</strong> ${item.symptom}</p>
                    <p><strong>Prediction:</strong> ${item.predicted_disease || "N/A"}</p>
                    <p><strong>Confidence:</strong> ${Number(item.confidence || 0).toFixed(2)}%</p>
                    <div class="history-date">${new Date(item.created_at).toLocaleString("en-IN")}</div>
                </div>`;
        });
    } catch (error) {
        console.error("History Error:", error);
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch("http://127.0.0.1:8000/analytics");
        const data = await response.json();

        console.log("Analytics Data:", data);

        const totalPredictions = document.getElementById("totalPredictions");
        const totalRecords = document.getElementById("totalRecords");

        if (totalPredictions) totalPredictions.innerText = data.total_predictions || 0;
        if (totalRecords) totalRecords.innerText = data.total_records || 0;
    } catch (error) {
        console.error("Analytics Error:", error);
    }
}

window.onload = function () {
    loadHistory();
    loadAnalytics();
};
