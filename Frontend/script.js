
const API_URL = "http://127.0.0.1:8000";

const body = document.getElementById("applicationsBody");
const feedback = document.getElementById("feedback");
const dialog = document.getElementById("applicationDialog");
const form = document.getElementById("applicationForm");

let applications = [];
let editingId = null;

function showMessage(message) {
    feedback.textContent = message;
}

async function apiRequest(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Request failed: ${response.status}`);
    }

    if (response.status === 204) return null;
    return response.json();
}

async function loadDashboard() {
    try {
        const [records, analytics] = await Promise.all([
            apiRequest("/applications"),
            apiRequest("/analytics")
        ]);

        applications = records;
        document.getElementById("totalCount").textContent = analytics.total_applications;
        document.getElementById("appliedCount").textContent = analytics.applied;
        document.getElementById("interviewCount").textContent = analytics.interviews;
        document.getElementById("offerCount").textContent = analytics.offers;

        renderApplications();
        showMessage("");
    } catch (error) {
        showMessage(`Could not load data: ${error.message}`);
        body.innerHTML = `<tr><td colspan="5">Unable to connect to the API. Check that FastAPI is running.</td></tr>`;
    }
}

function renderApplications() {
    const filter = document.getElementById("statusFilter").value;
    const visible = applications.filter(item =>
        filter === "All" || item.status === filter
    );

    if (!visible.length) {
        body.innerHTML = `<tr><td colspan="5">No applications found.</td></tr>`;
        return;
    }

    body.replaceChildren();

    visible.forEach(item => {
        const row = document.createElement("tr");

        const company = document.createElement("td");
        company.textContent = item.company_name;

        const role = document.createElement("td");
        role.textContent = item.job_role;

        const date = document.createElement("td");
        date.textContent = item.applied_date;

        const statusCell = document.createElement("td");
        const badge = document.createElement("span");
        badge.className = `status-badge status-${item.status}`;
        badge.textContent = item.status;
        statusCell.append(badge);

        const actions = document.createElement("td");
        const edit = document.createElement("button");
        edit.className = "action-button";
        edit.textContent = "Edit";
        edit.addEventListener("click", () => openEditForm(item));

        const remove = document.createElement("button");
        remove.className = "action-button delete-button";
        remove.textContent = "Delete";
        remove.addEventListener("click", () => deleteApplication(item.id));

        actions.append(edit, remove);
        row.append(company, role, date, statusCell, actions);
        body.append(row);
    });
}

function openAddForm() {
    editingId = null;
    form.reset();
    document.getElementById("formTitle").textContent = "Add Application";
    document.getElementById("appliedDate").value =
        new Date().toLocaleDateString("en-CA");
    dialog.showModal();
}

function openEditForm(item) {
    editingId = item.id;
    document.getElementById("formTitle").textContent = "Edit Application";
    document.getElementById("companyName").value = item.company_name;
    document.getElementById("jobRole").value = item.job_role;
    document.getElementById("appliedDate").value = item.applied_date;
    document.getElementById("applicationStatus").value = item.status;
    dialog.showModal();
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    const payload = {
        company_name: document.getElementById("companyName").value.trim(),
        job_role: document.getElementById("jobRole").value.trim(),
        applied_date: document.getElementById("appliedDate").value,
        status: document.getElementById("applicationStatus").value
    };

    try {
        if (editingId === null) {
            await apiRequest("/applications", {
                method: "POST",
                body: JSON.stringify(payload)
            });
            showMessage("Application added successfully.");
        } else {
            await apiRequest(`/applications/${editingId}`, {
                method: "PATCH",
                body: JSON.stringify(payload)
            });
            showMessage("Application updated successfully.");
        }

        dialog.close();
        await loadDashboard();
    } catch (error) {
        showMessage(error.message);
    }
});

async function deleteApplication(id) {
    if (!confirm("Delete this application?")) return;

    try {
        await apiRequest(`/applications/${id}`, { method: "DELETE" });
        showMessage("Application deleted successfully.");
        await loadDashboard();
    } catch (error) {
        showMessage(error.message);
    }
}

document.getElementById("addButton").addEventListener("click", openAddForm);
document.getElementById("cancelButton").addEventListener("click", () => dialog.close());
document.getElementById("statusFilter").addEventListener("change", renderApplications);

loadDashboard();
