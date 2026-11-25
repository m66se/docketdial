const examples = {
  call: {
    state: "Proposed", title: "Discuss purchase agreement with client.",
    duration: "12m 40s", basis: "connected call",
    note: "The call log records the duration. A text identifies the matter. Both support one entry."
  },
  email: {
    state: "Needs input", title: "Send revised indemnity clause to client.",
    duration: "Pending", basis: "lawyer to confirm duration",
    note: "The sent message identifies the clause and matter. Its timestamp cannot show how long drafting took."
  },
  meeting: {
    state: "Already recorded", title: "Attend closing meeting with client.",
    duration: "0m new", basis: "existing entry matched",
    note: "The ledger already includes this meeting on AM-12. The calendar record adds no new fees."
  }
};
const byId = id => document.getElementById(id);
const recordButtons = [...document.querySelectorAll("[data-record]")];
for (const button of recordButtons) {
  button.addEventListener("click", () => {
    const key = button.dataset.record;
    const entry = examples[key];
    for (const item of recordButtons) {
      const selected = item === button;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-pressed", String(selected));
    }
    for (const field of ["state", "title", "duration", "basis", "note"]) {
      byId("entry-" + field).textContent = entry[field];
    }
    byId("entry-state").dataset.state = key;
  });
}

const platformLinks = [...document.querySelectorAll("[data-platform]")];
const panels = [...document.querySelectorAll(".install-panel")];
function showPlatform(name) {
  const selected = panels.find(panel => panel.id === name);
  if (!selected) return;
  for (const panel of panels) panel.hidden = panel !== selected;
  for (const link of platformLinks) {
    const active = link.dataset.platform === name;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "true");
    else link.removeAttribute("aria-current");
  }
}
showPlatform(panels.some(panel => "#" + panel.id === location.hash) ? location.hash.slice(1) : "copilot");
for (const link of platformLinks) {
  link.addEventListener("click", event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    showPlatform(link.dataset.platform);
    history.replaceState(null, "", link.hash);
  });
}
window.addEventListener("hashchange", () => showPlatform(location.hash.slice(1)));

for (const button of document.querySelectorAll(".copy-btn")) {
  button.hidden = false;
  button.addEventListener("click", async () => {
    const box = button.closest(".agent-box");
    const prompt = box.querySelector(".prompt");
    const status = box.querySelector(".status");
    try {
      await navigator.clipboard.writeText(prompt.textContent);
      status.textContent = "Copied. Paste it into your assistant.";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(prompt);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = "Instructions selected. Use your device’s Copy command.";
    }
  });
}

async function loadRepository() {
  try {
    const response = await fetch("https://api.github.com/repos/m66se/docketdial", {
      credentials: "omit", headers: {Accept: "application/vnd.github+json"}
    });
    if (!response.ok) return;
    const repo = await response.json();
    for (const [key, value] of [["stars", repo.stargazers_count], ["forks", repo.forks_count]]) {
      if (Number.isSafeInteger(value) && value >= 0) byId(key).textContent = value.toLocaleString();
    }
  } catch {
    // The direct GitHub links remain usable offline or when the API is rate limited.
  }
}
loadRepository();
