const API_BASE =
  window.location.hostname.includes("vercel")
    ? "https://docuease-backend-7oux.onrender.com"
    : "http://127.0.0.1:8000";

async function uploadDocument() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a document");
        return;
    }

    const loader = document.getElementById("loader");
    const uploadBtn = document.getElementById("uploadBtn");
    const uploadSection = document.getElementById("uploadSection");
    const summarySection = document.getElementById("summarySection");

    loader.classList.remove("hidden");
    uploadBtn.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();

        // Summary
        document.getElementById("summary").innerText =
            data.summary || "No summary generated.";

        // Keywords
        const kwDiv = document.getElementById("keywords");
        kwDiv.innerHTML = "";

        (data.keywords || []).forEach(k => {
            const span = document.createElement("span");
            span.innerText = k;
            kwDiv.appendChild(span);
        });

        // Switch view
        uploadSection.classList.add("hidden");
        summarySection.classList.remove("hidden");
        summarySection.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        console.error(error);
        alert("❌ Error processing document. Please try again.");
    } finally {
        loader.classList.add("hidden");
        uploadBtn.disabled = false;
    }
}

function toggleTheme() {
    document.body.classList.toggle("dark");
}
