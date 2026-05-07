const iconPaths = {
  agave: '<path d="M12 3l1.5 6 4-4-2.2 6.3L22 10l-5.8 3.4 3.8 2.6-5.7-.6L12 22l-2.3-6.6-5.7.6 3.8-2.6L2 10l6.7 1.3L6.5 5l4 4L12 3z"/>',
  bottle: '<path d="M10 2h4v4l1 2v12a2 2 0 0 1-2 2h-2a2 2 0 0 1-2-2V8l1-2V2z"/><path d="M9 12h6"/>',
  calendar: '<path d="M7 2v4M17 2v4M4 8h16M5 4h14a1 1 0 0 1 1 1v15a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a1 1 0 0 1 1-1z"/>',
  chart: '<path d="M4 20V8M10 20V4M16 20v-7M22 20H2"/>',
  chat: '<path d="M4 5h16v11H7l-3 3V5z"/>',
  chef: '<path d="M7 10a4 4 0 1 1 7-3 3 3 0 1 1 3 5H7a3 3 0 0 1 0-6"/><path d="M7 12v7h10v-7"/>',
  compass: '<path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7z"/><path d="M12 9v6M9 12h6"/>',
  concierge: '<path d="M3 19h18M5 19a7 7 0 0 1 14 0M12 6v3"/><path d="M9 6h6"/>',
  crown: '<path d="M4 18h16l1-10-5 4-4-7-4 7-5-4 1 10z"/><path d="M4 22h16"/>',
  doc: '<path d="M7 2h7l5 5v15H7z"/><path d="M14 2v6h5M10 13h6M10 17h6"/>',
  gear: '<path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/><path d="M4 12h2M18 12h2M12 4v2M12 18v2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M17.7 6.3l-1.4 1.4M7.7 16.3l-1.4 1.4"/>',
  handshake: '<path d="M7 12l3-3 4 4 3-3 4 4-5 5-4-4-4 4-5-5 4-2z"/><path d="M10 9L8 7H4v7"/>',
  image: '<path d="M4 5h16v14H4z"/><path d="M7 16l4-4 3 3 2-2 3 3M8 9h.01"/>',
  martini: '<path d="M5 3h14l-7 8-7-8zM12 11v8M8 21h8"/><path d="M16 4l3-2"/>',
  pin: '<path d="M12 22s7-6.2 7-13A7 7 0 0 0 5 9c0 6.8 7 13 7 13z"/><circle cx="12" cy="9" r="2"/>',
  qr: '<path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 14h2v6h-6v-2h4z"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  slides: '<path d="M4 5h16v12H4zM12 17v4M8 21h8"/><path d="M8 9h8M8 12h5"/>',
  ticket: '<path d="M4 8a2 2 0 0 0 0 4v4h16v-4a2 2 0 0 0 0-4V4H4v4z"/><path d="M9 5v14"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 22a8 8 0 0 1 16 0"/>',
  video: '<path d="M4 6h12v12H4z"/><path d="M16 10l5-3v10l-5-3z"/>',
};

const $ = (selector) => document.querySelector(selector);
let currentState = null;

function icon(name) {
  return `<svg viewBox="0 0 24 24" aria-hidden="true">${iconPaths[name] || iconPaths.agave}</svg>`;
}

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("tt-theme", theme);
  $("#themeLabel").textContent = theme === "dark" ? "Dark" : "Light";
}

function buildAgentCard(agent) {
  return `
    <article class="agent-card tone-${agent.tone}" data-agent-card data-search="${[
      agent.name,
      agent.group,
      agent.description,
      agent.metric,
    ].join(" ").toLowerCase()}">
      <div class="agent-topline">
        <span class="agent-icon">${icon(agent.icon)}</span>
        <span class="agent-status"><i></i>${agent.status}</span>
      </div>
      <h3>${agent.name}</h3>
      <p>${agent.description}</p>
      <div class="agent-metric">${agent.metric}</div>
    </article>
  `;
}

function buildActivityItem(item) {
  return `
    <li class="activity-item tone-${item.tone}">
      <span>${icon(item.tone === "gold" ? "image" : item.tone === "teal" ? "chart" : item.tone === "green" ? "doc" : "search")}</span>
      <div>
        <strong>${item.agent}</strong>
        <p>${item.event}</p>
      </div>
      <time>${item.time}</time>
    </li>
  `;
}

function buildQuickAction(action) {
  return `
    <button class="quick-action tone-${action.tone}" type="button" data-action="${action.label}" data-prompt="${action.prompt}">
      <span>
        <strong>${action.label}</strong>
        <small>${action.description}</small>
      </span>
      <b>+</b>
    </button>
  `;
}

function renderState(state) {
  currentState = state;
  $("#eventTime").textContent = state.event.localTime;
  $("#heroTagline").textContent = state.event.tagline;
  $("#performance").textContent = `${state.health.performance}%`;
  $("#tasksToday").textContent = state.health.tasksToday;
  $("#completed").textContent = state.health.completed;
  $("#timeSaved").textContent = state.health.timeSaved;
  $("#activeAgents").textContent = state.health.activeAgents;
  $("#sentiment").textContent = state.health.sentiment;
  $("#sponsorLeads").textContent = state.health.sponsorLeads;
  $("#ticketRevenue").textContent = state.health.ticketRevenue;

  $("#agentGrid").innerHTML = state.agents.map(buildAgentCard).join("");
  $("#activityFeed").innerHTML = state.activity.map(buildActivityItem).join("");
  $("#quickActions").innerHTML = state.quickActions.map(buildQuickAction).join("");
  bindQuickActions();
}

async function loadState() {
  const response = await fetch("/api/dashboard/state", { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error("Dashboard state unavailable");
  renderState(await response.json());
}

async function loadSystemStatus() {
  const response = await fetch("/api/system/status", { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error("System status unavailable");
  renderSystemStatus(await response.json());
}

function renderSystemStatus(status) {
  const label = $("#systemStatusLabel");
  const levelClass = status.level === "blocked" ? "is-blocked" : status.level === "warning" ? "is-warning" : "";
  label.className = levelClass;
  label.innerHTML = `<i></i> ${status.level === "ready" ? "Ready" : status.level === "warning" ? "Needs Token" : "Needs Keys"}`;
  $("#systemSummary").textContent = status.summary;
  $("#diagnosticsList").innerHTML = status.checks
    .slice(0, 6)
    .map((check) => `
      <li>
        <strong>${check.name}</strong>
        <span class="${check.configured ? "" : "is-missing"}">${check.configured ? "Configured" : "Missing"}</span>
      </li>
    `)
    .join("");
}

function bindSearch() {
  const input = $("#globalSearch");
  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll("[data-agent-card]").forEach((card) => {
      card.hidden = query.length > 0 && !card.dataset.search.includes(query);
    });
  });

  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      input.focus();
    }
  });
}

function bindQuickActions() {
  document.querySelectorAll(".quick-action").forEach((button) => {
    button.addEventListener("click", () => {
      $("#missionTitle").value = button.dataset.action || "New Mission";
      $("#missionType").value = button.dataset.action || "New Mission";
      $("#missionDescription").value = button.dataset.prompt || "";
      document.getElementById("missionPanel").scrollIntoView({ behavior: "smooth", block: "start" });
      $("#missionDescription").focus();
    });
  });
}

function bindMissionForm() {
  $("#missionForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const result = $("#missionResult");
    const payload = {
      title: $("#missionTitle").value,
      missionType: $("#missionType").value,
      description: $("#missionDescription").value,
    };
    result.classList.add("is-visible");
    result.textContent = "Routing mission...";

    try {
      const response = await fetch("/api/missions/route", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Mission routing failed");
      const route = await response.json();
      result.innerHTML = `
        <strong>${route.recommendedAgent}</strong> is the recommended lead.
        <br>${route.nextSteps.join(" ")}
        <br><span class="mission-endpoint">Endpoint: ${route.streamEndpoint}</span>
      `;
    } catch (error) {
      console.error(error);
      result.textContent = "Mission routing is unavailable. Check the local server and try again.";
    }
  });
}

function bindNav() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-button").forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");
      const target = button.dataset.target;
      const section = document.getElementById(target);
      if (section) section.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setTheme(localStorage.getItem("tt-theme") || "dark");
  $("#themeToggle").addEventListener("click", () => {
    setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  });
  bindNav();
  bindSearch();
  bindMissionForm();
  loadState().catch((error) => {
    console.error(error);
    document.body.classList.add("state-error");
  });
  loadSystemStatus().catch((error) => {
    console.error(error);
    $("#systemSummary").textContent = "System diagnostics are unavailable.";
  });
});
