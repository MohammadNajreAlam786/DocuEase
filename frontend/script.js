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

    // UI state
    loader.classList.remove("hidden");
    uploadBtn.disabled = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        /* =====================
           SUMMARY
        ===================== */
        const summaryEl = document.getElementById("summary");
        summaryEl.innerText = data.summary || "No summary generated.";

        /* =====================
           KEYWORDS
        ===================== */
        const kwDiv = document.getElementById("keywords");
        kwDiv.innerHTML = "";

        (data.keywords || []).forEach(keyword => {
            const span = document.createElement("span");
            span.innerText = keyword;
            kwDiv.appendChild(span);
        });

        /* =====================
           SECTION-WISE SUMMARY
        ===================== */
        const sectionDiv = document.getElementById("sections");
        sectionDiv.innerHTML = "";

        const sections = data.section_summaries || {};

        for (const title in sections) {
            const item = document.createElement("div");
            item.className = "accordion-item";

            const header = document.createElement("div");
            header.className = "accordion-header";
            header.innerHTML = `${title} <span>+</span>`;

            const content = document.createElement("div");
            content.className = "accordion-content";
            content.innerText = sections[title];

            header.onclick = () => {
                item.classList.toggle("active");
                header.querySelector("span").innerText =
                    item.classList.contains("active") ? "-" : "+";
            };

            item.appendChild(header);
            item.appendChild(content);
            sectionDiv.appendChild(item);
        }

        /* =====================
           VIEW TRANSITION
        ===================== */
        uploadSection.classList.add("hidden");

        summarySection.classList.remove("hidden");
        summarySection.classList.remove("fade-in"); // reset animation
        void summarySection.offsetWidth;             // force reflow
        summarySection.classList.add("fade-in");
        summarySection.style.opacity = "1";

        summarySection.scrollIntoView({ behavior: "smooth" });


    } catch (error) {
        console.error(error);
        alert("❌ Error processing document. Please try again.");
    } finally {
        loader.classList.add("hidden");
        uploadBtn.disabled = false;
    }
}

/* =====================
   THEME TOGGLE
===================== */
function toggleTheme() {
    document.body.classList.toggle("dark");
    const toggle = document.getElementById("themeToggle");
    toggle.innerText = document.body.classList.contains("dark") ? "☀️" : "🌙";
}
