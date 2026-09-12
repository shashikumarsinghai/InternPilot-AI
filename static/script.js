// ============================================================
// ELEMENTS
// ============================================================

const searchBtn = document.getElementById("searchBtn");
const resultsSection = document.getElementById("resultsSection");
const resultsContainer = document.getElementById("results");

const roleInput = document.getElementById("role");
const locationInput = document.getElementById("location");
const skillsInput = document.getElementById("skills");
const experienceInput = document.getElementById("experience");

const loadTrackerBtn =
    document.getElementById("loadTrackerBtn");

const trackerResults =
    document.getElementById("trackerResults");


// ============================================================
// FLOATING AI CHAT
// ============================================================

let openChatBtn =
    document.getElementById("openChatBtn");

let chatPanel =
    document.getElementById("chatPanel");

let chatInput = null;
let chatMessages = null;
let chatBtn = null;
let closeChatBtn = null;


// ============================================================
// CREATE FLOATING AI BUTTON
// ============================================================

if (!openChatBtn) {

    openChatBtn =
        document.createElement("button");

    openChatBtn.id =
        "openChatBtn";

    openChatBtn.className =
        "floating-chat-btn";

    openChatBtn.type =
        "button";

    openChatBtn.setAttribute(
        "aria-label",
        "Open InternPilot AI"
    );

    openChatBtn.innerHTML = `
        <span class="floating-chat-icon">
            🤖
        </span>

        <span>
            Ask AI
        </span>
    `;

    document.body.appendChild(
        openChatBtn
    );
}


// ============================================================
// CREATE CHAT PANEL
// ============================================================

if (!chatPanel) {

    chatPanel =
        document.createElement("div");

    chatPanel.id =
        "chatPanel";

    chatPanel.className =
        "chat-panel";

    chatPanel.innerHTML = `
        <div class="chat-panel-header">

            <div>
                <div class="fw-bold">
                    🤖 InternPilot AI
                </div>

                <small>
                    Your internship assistant
                </small>
            </div>

            <button
                id="closeChatBtn"
                class="chat-close-btn"
                type="button"
                aria-label="Close chat"
            >
                ✕
            </button>

        </div>

        <div
            id="chatMessages"
            class="chat-box"
        >

            <div class="bot-message">
                Hi! 👋 I'm InternPilot AI.
                Ask me anything about internships.
            </div>

        </div>

        <div class="chat-input-area">

            <div class="input-group">

                <input
                    type="text"
                    id="chatInput"
                    class="form-control"
                    placeholder="Ask me about internships..."
                    autocomplete="off"
                >

                <button
                    id="chatBtn"
                    class="btn btn-primary"
                    type="button"
                >
                    Send
                </button>

            </div>

        </div>
    `;

    document.body.appendChild(
        chatPanel
    );
}


// ============================================================
// GET CHAT ELEMENTS
// ============================================================

chatInput =
    document.getElementById("chatInput");

chatMessages =
    document.getElementById("chatMessages");

chatBtn =
    document.getElementById("chatBtn");

closeChatBtn =
    document.getElementById("closeChatBtn");


// ============================================================
// OPEN CHAT
// ============================================================

if (openChatBtn) {

    openChatBtn.addEventListener(
        "click",
        () => {

            if (!chatPanel) {
                return;
            }

            chatPanel.classList.add(
                "open"
            );

            openChatBtn.style.display =
                "none";

            setTimeout(
                () => {

                    if (chatInput) {
                        chatInput.focus();
                    }

                },
                200
            );
        }
    );
}


// ============================================================
// CLOSE CHAT
// ============================================================

if (closeChatBtn) {

    closeChatBtn.addEventListener(
        "click",
        () => {

            if (chatPanel) {

                chatPanel.classList.remove(
                    "open"
                );
            }

            if (openChatBtn) {

                openChatBtn.style.display =
                    "flex";
            }
        }
    );
}


// ============================================================
// GLOBAL ROLE OPTIONS
// ============================================================

const roleOptions = [
    "Software Engineering",
    "Data Science",
    "Artificial Intelligence",
    "Machine Learning",
    "Cybersecurity",
    "Web Development",
    "Mobile App Development",
    "UI/UX Design",
    "Cloud Engineering",
    "DevOps Engineering"
];


// ============================================================
// GLOBAL LOCATION OPTIONS
// ============================================================

const locationOptions = [
    "India",
    "United States",
    "United Kingdom",
    "Canada",
    "Germany",
    "Australia",
    "Singapore",
    "Netherlands",
    "France",
    "Japan"
];


// ============================================================
// INPUT HELPERS
// ============================================================

function selectInputValue(input) {

    if (!input) {
        return;
    }

    input.addEventListener(
        "focus",
        () => {

            setTimeout(
                () => {
                    input.select();
                },
                0
            );

        }
    );
}

selectInputValue(roleInput);
selectInputValue(locationInput);


// ============================================================
// KEYBOARD SEARCH
// ============================================================

if (roleInput) {

    roleInput.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                event.preventDefault();

                if (searchBtn) {
                    searchBtn.click();
                }
            }
        }
    );
}


if (locationInput) {

    locationInput.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                event.preventDefault();

                if (searchBtn) {
                    searchBtn.click();
                }
            }
        }
    );
}


// ============================================================
// SEARCH + RECOMMEND
// ============================================================

if (searchBtn) {

    searchBtn.addEventListener(
        "click",
        async () => {

            const role =
                roleInput.value.trim() ||
                "software engineering";

            const location =
                locationInput.value.trim() ||
                "India";

            const skillsText =
                skillsInput.value.trim();

            const skills =
                skillsText
                    ? skillsText
                        .split(",")
                        .map(
                            skill =>
                                skill.trim()
                        )
                        .filter(
                            skill =>
                                skill.length > 0
                        )
                    : [];

            const experience =
                experienceInput.value;

            searchBtn.disabled =
                true;

            searchBtn.textContent =
                "Searching...";

            resultsSection.classList.remove(
                "d-none"
            );

            resultsContainer.innerHTML = `
                <div class="text-center py-4">

                    <div
                        class="spinner-border"
                        role="status"
                    ></div>

                    <p class="mt-2 text-muted">
                        Finding and evaluating internships...
                    </p>

                </div>
            `;

            try {

                const response =
                    await fetch(
                        "/api/recommend",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    role: role,

                                    location:
                                        location,

                                    student_profile: {

                                        skills:
                                            skills,

                                        location:
                                            location,

                                        experience:
                                            experience
                                    }
                                })
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Something went wrong."
                    );
                }

                if (
                    !data.results ||
                    data.results.length === 0
                ) {

                    resultsContainer.innerHTML = `
                        <div class="alert alert-warning">

                            No internship opportunities were found
                            for this search.

                        </div>
                    `;

                    return;
                }

                displayResults(
                    data.results
                );

            } catch (error) {

                console.error(
                    "Search error:",
                    error
                );

                resultsContainer.innerHTML = `
                    <div class="alert alert-danger">

                        <strong>Error:</strong>

                        ${escapeHtml(
                            error.message
                        )}

                    </div>
                `;

            } finally {

                searchBtn.disabled =
                    false;

                searchBtn.textContent =
                    "Search Internships";
            }
        }
    );
}


// ============================================================
// DISPLAY RESULTS
// ============================================================

function displayResults(
    internships
) {

    resultsContainer.innerHTML =
        "";

    internships.forEach(
        internship => {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "card shadow-sm mb-3";

            const matchedSkills =
                internship.matched_skills ||
                [];

            const missingSkills =
                internship.missing_skills ||
                [];

            const matchedHtml =
                matchedSkills.length > 0
                    ? matchedSkills
                        .map(
                            skill => `
                                <span
                                    class="badge bg-success me-1 mb-1"
                                >
                                    ${escapeHtml(
                                        skill
                                    )}
                                </span>
                            `
                        )
                        .join("")
                    : `
                        <span class="text-muted">
                            None
                        </span>
                    `;

            const missingHtml =
                missingSkills.length > 0
                    ? missingSkills
                        .map(
                            skill => `
                                <span
                                    class="badge bg-warning text-dark me-1 mb-1"
                                >
                                    ${escapeHtml(
                                        skill
                                    )}
                                </span>
                            `
                        )
                        .join("")
                    : `
                        <span class="text-muted">
                            None
                        </span>
                    `;

            card.innerHTML = `
                <div class="card-body">

                    <div class="d-flex
                                justify-content-between
                                align-items-start
                                gap-3">

                        <div>

                            <span
                                class="badge bg-dark mb-2"
                            >
                                Rank #${
                                    internship.rank || "-"
                                }
                            </span>

                            <h4 class="card-title">

                                ${escapeHtml(
                                    internship.title ||
                                    "Unknown Internship"
                                )}

                            </h4>

                        </div>

                        <div class="text-end">

                            <div
                                class="display-6 fw-bold"
                            >
                                ${
                                    internship.match_score ??
                                    0
                                }%
                            </div>

                            <small class="text-muted">
                                Match Score
                            </small>

                        </div>

                    </div>

                    <div class="mb-3">

                        <span
                            class="badge bg-primary"
                        >
                            ${escapeHtml(
                                internship.recommendation ||
                                "Match"
                            )}
                        </span>

                    </div>

                    <div class="row mb-3">

                        <div class="col-md-4">

                            <strong>
                                Matched Skills
                            </strong>

                            <div class="mt-1">
                                ${matchedHtml}
                            </div>

                        </div>

                        <div class="col-md-4">

                            <strong>
                                Missing Skills
                            </strong>

                            <div class="mt-1">
                                ${missingHtml}
                            </div>

                        </div>

                        <div class="col-md-4">

                            <strong>
                                Location Score
                            </strong>

                            <div class="mt-1">

                                ${
                                    internship.location_score ??
                                    0
                                }%

                            </div>

                        </div>

                    </div>

                    <div
                        class="d-flex gap-2 flex-wrap"
                    >

                        <a
                            href="${escapeAttribute(
                                internship.url || "#"
                            )}"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="btn btn-primary"
                        >
                            View Internship
                        </a>

                        <button
                            class="btn btn-outline-success save-btn"
                        >
                            Save Internship
                        </button>

                    </div>

                </div>
            `;

            const saveBtn =
                card.querySelector(
                    ".save-btn"
                );

            saveBtn.addEventListener(
                "click",
                () =>
                    saveInternship(
                        internship,
                        saveBtn
                    )
            );

            resultsContainer.appendChild(
                card
            );
        }
    );
}


// ============================================================
// SAVE INTERNSHIP
// ============================================================

async function saveInternship(
    internship,
    button
) {

    button.disabled =
        true;

    button.textContent =
        "Saving...";

    try {

        const response =
            await fetch(
                "/api/tracker",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            internship:
                                internship
                        })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                data.message ||
                "Could not save internship."
            );
        }

        if (data.success) {

            button.textContent =
                "✓ Saved";

            button.classList.remove(
                "btn-outline-success"
            );

            button.classList.add(
                "btn-success"
            );

            loadTracker();

        } else {

            button.textContent =
                data.message ||
                "Already Saved";

            button.disabled =
                false;
        }

    } catch (error) {

        console.error(
            "Save error:",
            error
        );

        button.disabled =
            false;

        button.textContent =
            "Save Internship";

        alert(
            error.message
        );
    }
}


// ============================================================
// LOAD TRACKER
// ============================================================

if (loadTrackerBtn) {

    loadTrackerBtn.addEventListener(
        "click",
        loadTracker
    );
}


async function loadTracker() {

    if (!loadTrackerBtn) {
        return;
    }

    loadTrackerBtn.disabled =
        true;

    loadTrackerBtn.textContent =
        "Loading...";

    try {

        const response =
            await fetch(
                "/api/tracker"
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not load tracker."
            );
        }

        displayTracker(
            data.results || []
        );

    } catch (error) {

        console.error(
            "Tracker error:",
            error
        );

        trackerResults.innerHTML = `
            <div class="alert alert-danger">

                ${escapeHtml(
                    error.message
                )}

            </div>
        `;

    } finally {

        loadTrackerBtn.disabled =
            false;

        loadTrackerBtn.textContent =
            "Refresh";
    }
}


// ============================================================
// DISPLAY TRACKER
// ============================================================

function displayTracker(
    internships
) {

    if (
        internships.length === 0
    ) {

        trackerResults.innerHTML = `
            <p class="text-muted">
                No tracked internships yet.
            </p>
        `;

        return;
    }

    trackerResults.innerHTML =
        "";

    internships.forEach(
        internship => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "border rounded p-3 mb-3";

            // IMPORTANT:
            // Get the current status for THIS internship.
            const currentStatus =
                internship.status ||
                "Saved";

            item.innerHTML = `
                <div class="d-flex
                            justify-content-between
                            align-items-start
                            gap-3">

                    <div>

                        <h5>
                            ${escapeHtml(
                                internship.title ||
                                "Unknown Internship"
                            )}
                        </h5>

                        <div class="text-muted">

                            Match:
                            ${
                                internship.match_score ??
                                0
                            }%

                        </div>

                    </div>

                    <button
                        class="btn btn-sm
                               btn-outline-danger
                               remove-btn"
                    >
                        Remove
                    </button>

                </div>

                <div class="mt-3">

                    <label class="form-label">
                        Application Status
                    </label>

                    <select
                        class="form-select status-select"
                    >

                        <option value="Saved">
                            Saved
                        </option>

                        <option value="Applied">
                            Applied
                        </option>

                        <option value="Interview">
                            Interview
                        </option>

                        <option value="Rejected">
                            Rejected
                        </option>

                        <option value="Offer">
                            Offer
                        </option>

                    </select>

                    <div class="mt-2">

                        <span class="text-muted">
                            Current status:
                        </span>

                        <span
                            class="badge status-badge"
                        >
                            ${escapeHtml(
                                currentStatus
                            )}
                        </span>

                    </div>

                </div>

                <a
                    href="${escapeAttribute(
                        internship.url || "#"
                    )}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="btn btn-sm btn-primary mt-3"
                >
                    Open Internship
                </a>
            `;

            const statusSelect =
                item.querySelector(
                    ".status-select"
                );

            const statusBadge =
                item.querySelector(
                    ".status-badge"
                );

            // Set dropdown to current status.
            statusSelect.value =
                currentStatus;

            // Set badge to current status.
            updateStatusBadge(
                statusBadge,
                currentStatus
            );

            // ====================================================
            // CHANGE STATUS
            // ====================================================

            statusSelect.addEventListener(
                "change",
                async () => {

                    const newStatus =
                        statusSelect.value;

                    // Update UI immediately.
                    statusBadge.textContent =
                        newStatus;

                    updateStatusBadge(
                        statusBadge,
                        newStatus
                    );

                    await updateStatus(
                        internship.url,
                        newStatus
                    );
                }
            );

            // ====================================================
            // REMOVE
            // ====================================================

            const removeBtn =
                item.querySelector(
                    ".remove-btn"
                );

            removeBtn.addEventListener(
                "click",
                () =>
                    removeInternship(
                        internship.url
                    )
            );

            trackerResults.appendChild(
                item
            );
        }
    );
}


// ============================================================
// STATUS BADGE
// ============================================================

function updateStatusBadge(
    badge,
    status
) {

    if (!badge) {
        return;
    }

    badge.className =
        "badge status-badge";

    if (status === "Saved") {

        badge.classList.add(
            "bg-secondary"
        );

    } else if (status === "Applied") {

        badge.classList.add(
            "bg-primary"
        );

    } else if (status === "Interview") {

        badge.classList.add(
            "bg-warning",
            "text-dark"
        );

    } else if (status === "Rejected") {

        badge.classList.add(
            "bg-danger"
        );

    } else if (status === "Offer") {

        badge.classList.add(
            "bg-success"
        );

    } else {

        badge.classList.add(
            "bg-secondary"
        );
    }

    badge.textContent =
        status;
}


// ============================================================
// UPDATE TRACKER STATUS
// ============================================================

async function updateStatus(
    url,
    status
) {

    try {

        const response =
            await fetch(
                "/api/tracker/status",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            url: url,
                            status: status
                        })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not update status."
            );
        }

        console.log(
            "Status updated:",
            status
        );

        // Reload tracker from backend
        // so saved status stays synchronized.
        await loadTracker();

    } catch (error) {

        console.error(
            "Status update error:",
            error
        );

        alert(
            error.message
        );

        // Reload tracker if update failed.
        await loadTracker();
    }
}


// ============================================================
// REMOVE TRACKED INTERNSHIP
// ============================================================

async function removeInternship(
    url
) {

    if (
        !confirm(
            "Remove this internship from tracker?"
        )
    ) {

        return;
    }

    try {

        const response =
            await fetch(
                "/api/tracker",
                {
                    method: "DELETE",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            url: url
                        })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not remove internship."
            );
        }

        loadTracker();

    } catch (error) {

        console.error(
            "Remove error:",
            error
        );

        alert(
            error.message
        );
    }
}


// ============================================================
// CHAT SEND BUTTON
// ============================================================

if (chatBtn) {

    chatBtn.addEventListener(
        "click",
        sendChat
    );
}


// ============================================================
// CHAT ENTER KEY
// ============================================================

if (chatInput) {

    chatInput.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();

                sendChat();
            }
        }
    );
}


// ============================================================
// SEND CHAT
// ============================================================

async function sendChat() {

    if (!chatInput || !chatMessages) {
        return;
    }

    const message =
        chatInput.value.trim();

    if (!message) {
        return;
    }

    addChatMessage(
        message,
        "user"
    );

    chatInput.value =
        "";

    if (chatBtn) {
        chatBtn.disabled =
            true;
    }

    chatInput.disabled =
        true;

    const loadingElement =
        addChatMessage(
            "Thinking...",
            "bot"
        );

    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message:
                                message
                        })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Chat request failed."
            );
        }

        loadingElement.textContent =
            data.response ||
            "No response received.";

    } catch (error) {

        console.error(
            "Chat error:",
            error
        );

        loadingElement.textContent =
            "Sorry, I could not process your request.";

    } finally {

        if (chatBtn) {
            chatBtn.disabled =
                false;
        }

        chatInput.disabled =
            false;

        chatInput.focus();
    }
}


// ============================================================
// ADD CHAT MESSAGE
// ============================================================

function addChatMessage(
    message,
    sender
) {

    const element =
        document.createElement(
            "div"
        );

    if (
        sender === "user"
    ) {

        element.className =
            "user-message";

    } else {

        element.className =
            "bot-message";
    }

    element.textContent =
        message;

    chatMessages.appendChild(
        element
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

    return element;
}


// ============================================================
// SECURITY - HTML
// ============================================================

function escapeHtml(
    value
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        String(value ?? "");

    return div.innerHTML;
}


// ============================================================
// SECURITY - ATTRIBUTE
// ============================================================

function escapeAttribute(
    value
) {

    return String(value ?? "")
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        );
}


// ============================================================
// INITIAL LOAD
// ============================================================

loadTracker();