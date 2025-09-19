document.getElementById('analyze-btn').addEventListener('click', async () => {
    const text = document.getElementById('text-input').value;
    const resultsDiv = document.getElementById('results');
    const analyzeBtn = document.getElementById('analyze-btn');

    // IMPORTANT: You will replace this placeholder URL in Step 4
    // after you deploy your backend to Cloud Run.
    const API_URL = 'https://misinformation-api-1039291526226.us-central1.run.app'; 

    if (!text) {
        resultsDiv.innerHTML = '<p style="color: red;">Please enter some text to analyze.</p>';
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerText = 'Analyzing...';
    resultsDiv.innerHTML = '<p>Contacting AI analyst... please wait.</p>';

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`The server responded with an error: ${response.status}`);
        }

        const data = await response.json();

        // Build the HTML to display the results
        let flagsHTML = data.flags.map(flag => `<li><strong>${flag.technique}:</strong> ${flag.explanation}</li>`).join('');
        resultsDiv.innerHTML = `
            <h3>Verdict: ${data.verdict} (Confidence: ${Math.round(data.confidence_score * 100)}%)</h3>
            <p>${data.summary}</p>
            <h4>Detected Flags:</h4>
            <ul>${flagsHTML || "<li>No specific flags detected.</li>"}</ul>
        `;
    } catch (error) {
        resultsDiv.innerHTML = `<p style="color: red;">An error occurred. Please check if the API URL is correct and the backend is running. Details: ${error.message}</p>`;
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerText = 'Analyze Text';
    }
});