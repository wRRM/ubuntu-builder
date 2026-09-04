const state = { project: null, selectedGrub: null, grubDirty: false, pollTimer: null };

const $ = (selector) => document.querySelector(selector);
const formatBytes = (bytes) => {
  if (!Number.isFinite(bytes)) return "";
  const units = ["B", "KiB", "MiB", "GiB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit += 1; }
  return `${value.toFixed(unit ? 1 : 0)} ${units[unit]}`;
};
const shortHash = (hash) => hash ? `${hash.slice(0, 12)}…` : "";

function toast(message, error = false) {
  const element = $("#toast");
  element.textContent = message;
  element.className = `toast show${error ? " error" : ""}`;
  clearTimeout(element.timer);
  element.timer = setTimeout(() => { element.className = "toast"; }, 4000);
}

async function api(url, options = {}) {
  const response = await fetch(url, options);
  const body = response.status === 204 ? null : await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(body?.error || `Request failed (${response.status})`);
    error.details = body;
    throw error;
  }
  return body;
}

function renderBase() {
  const base = state.project.baseIso;
  const buildBusy = ["queued", "running"].includes(state.project.build.status);
  $("#base-badge").textContent = base ? "Loaded" : "Not loaded";
  $("#base-badge").className = `badge ${base ? "ready" : "muted"}`;
  $("#iso-dropzone").classList.toggle("hidden", Boolean(base));
  const summary = $("#base-summary");
  summary.classList.toggle("hidden", !base);
  if (base) {
    summary.replaceChildren();
    const details = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = base.name;
    const meta = document.createElement("span");
    meta.textContent = `${formatBytes(base.size)} · SHA-256 ${shortHash(base.sha256)}`;
    details.append(name, meta);
    const replace = document.createElement("button");
    replace.type = "button";
    replace.textContent = "Replace";
    replace.addEventListener("click", () => $("#iso-input").click());
    summary.append(details, replace);
  }
  $("#add-files-button").disabled = !base || buildBusy;
  $("#build-button").disabled = !base || buildBusy;
}

function fileDetails(item) {
  const wrapper = document.createElement("div");
  wrapper.className = "file-name";
  const strong = document.createElement("strong");
  strong.textContent = item.name;
  const small = document.createElement("span");
  small.textContent = `${formatBytes(item.size)}${item.sha256 ? ` · ${shortHash(item.sha256)}` : ""}`;
  wrapper.append(strong, small);
  return wrapper;
}

function renderFiles() {
  const container = $("#staged-files");
  const files = state.project.files;
  container.replaceChildren();
  container.classList.toggle("empty-state", files.length === 0);
  if (!files.length) {
    container.textContent = "No files staged yet.";
    return;
  }
  files.forEach((item) => {
    const row = document.createElement("div");
    row.className = "file-row";
    row.append(fileDetails(item));
    const path = document.createElement("code");
    path.className = "file-path";
    path.textContent = item.destination;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "icon-button";
    remove.textContent = "×";
    remove.disabled = ["queued", "running"].includes(state.project.build.status);
    remove.setAttribute("aria-label", `Delete ${item.name}`);
    remove.addEventListener("click", async () => {
      try {
        await api(`/api/files/${encodeURIComponent(item.id)}`, { method: "DELETE" });
        state.project.files = state.project.files.filter((file) => file.id !== item.id);
        renderFiles();
      } catch (error) { toast(error.message, true); }
    });
    row.append(path, remove);
    container.append(row);
  });
}

function renderGrub(preserveSelection = true) {
  const files = state.project.grubFiles;
  const buildBusy = ["queued", "running"].includes(state.project.build.status);
  const select = $("#grub-select");
  const editor = $("#grub-editor");
  const prior = preserveSelection ? state.selectedGrub : null;
  select.replaceChildren();
  if (!files.length) {
    const option = document.createElement("option");
    option.textContent = state.project.baseIso ? "No GRUB configuration found" : "No GRUB file loaded";
    select.append(option);
    select.disabled = true;
    editor.disabled = true;
    editor.value = "";
    $("#grub-status").textContent = state.project.baseIso ? "No grub.cfg or loopback.cfg was found." : "Upload an ISO to inspect GRUB.";
    $("#save-grub-button").disabled = true;
    return;
  }
  files.forEach((file) => {
    const option = document.createElement("option");
    option.value = file.path;
    option.textContent = file.path;
    select.append(option);
  });
  state.selectedGrub = files.some((file) => file.path === prior) ? prior : files[0].path;
  select.value = state.selectedGrub;
  select.disabled = false;
  editor.disabled = buildBusy;
  editor.value = files.find((file) => file.path === state.selectedGrub).content;
  state.grubDirty = false;
  $("#save-grub-button").disabled = true;
  $("#grub-status").className = "";
  $("#grub-status").textContent = `${files.length} configuration file${files.length === 1 ? "" : "s"} found`;
}

function renderBuild() {
  const build = state.project.build;
  const result = $("#build-result");
  const log = $("#build-log");
  result.className = `build-result ${build.status === "idle" ? "hidden" : build.status}`;
  result.replaceChildren();
  if (["queued", "running"].includes(build.status)) {
    result.textContent = build.status === "queued" ? "Build queued…" : "Building your ISO. This can take several minutes…";
  } else if (build.status === "failed") {
    result.textContent = `Build failed: ${build.error || "Unknown error"}`;
  } else if (build.status === "complete" && build.output) {
    const message = document.createElement("div");
    message.textContent = `Build complete · ${formatBytes(build.output.size)}`;
    const link = document.createElement("a");
    link.className = "download-link";
    link.href = `/api/output/${encodeURIComponent(build.output.name)}`;
    link.textContent = `Download ${build.output.name}`;
    const arrow = document.createElement("span");
    arrow.textContent = "↓";
    link.append(arrow);
    result.append(message, link);
  }
  log.classList.toggle("hidden", !build.log?.length);
  log.querySelector("pre").textContent = (build.log || []).join("\n");
  $("#build-button").disabled = !state.project.baseIso || ["queued", "running"].includes(build.status);
  if (["queued", "running"].includes(build.status)) schedulePoll();
}

function render() {
  renderBase();
  renderFiles();
  renderGrub();
  renderBuild();
}

function uploadIso(file) {
  if (!file || !file.name.toLowerCase().endsWith(".iso")) return toast("Choose a file ending in .iso", true);
  const data = new FormData();
  data.append("iso", file);
  const request = new XMLHttpRequest();
  const progress = $("#iso-progress");
  progress.classList.remove("hidden");
  request.upload.addEventListener("progress", (event) => {
    if (!event.lengthComputable) return;
    const percent = Math.round((event.loaded / event.total) * 100);
    progress.querySelector("span").style.width = `${percent}%`;
    $("#iso-progress-label").textContent = `${percent}%`;
  });
  request.addEventListener("load", () => {
    progress.classList.add("hidden");
    try {
      let body = {};
      try { body = JSON.parse(request.responseText || "{}"); } catch { /* non-JSON server failure */ }
      if (request.status < 200 || request.status >= 300) throw new Error(body.error || "Upload failed");
      state.project = body;
      state.selectedGrub = null;
      render();
      toast("Base ISO loaded and inspected");
    } catch (error) { toast(error.message, true); }
  });
  request.addEventListener("error", () => { progress.classList.add("hidden"); toast("Upload failed", true); });
  request.open("POST", "/api/base-iso");
  request.send(data);
}

async function stageFiles(files) {
  if (!files.length) return;
  const data = new FormData();
  for (const file of files) {
    const relative = file.webkitRelativePath || file.name;
    data.append("files", file);
    data.append("destinations", `/${relative.replaceAll("\\", "/")}`);
  }
  const button = $("#add-files-button");
  button.disabled = true;
  button.textContent = "Staging…";
  try {
    const body = await api("/api/files", { method: "POST", body: data });
    state.project.files.push(...body.files);
    renderFiles();
    toast(`${body.files.length} file${body.files.length === 1 ? "" : "s"} staged`);
  } catch (error) {
    toast(error.message, true);
  } finally {
    button.textContent = "+ Add files";
    renderBase();
  }
}

function schedulePoll() {
  clearTimeout(state.pollTimer);
  state.pollTimer = setTimeout(async () => {
    try {
      state.project = await api("/api/state");
      render();
    } catch (error) { toast(error.message, true); }
  }, 1500);
}

async function initialize() {
  try {
    state.project = await api("/api/state");
    render();
  } catch (error) {
    $("#health-pill").innerHTML = "<span></span> Unavailable";
    toast(error.message, true);
  }
}

$("#iso-input").addEventListener("change", (event) => uploadIso(event.target.files[0]));
$("#iso-dropzone").addEventListener("dragover", (event) => { event.preventDefault(); event.currentTarget.classList.add("dragging"); });
$("#iso-dropzone").addEventListener("dragleave", (event) => event.currentTarget.classList.remove("dragging"));
$("#iso-dropzone").addEventListener("drop", (event) => {
  event.preventDefault();
  event.currentTarget.classList.remove("dragging");
  uploadIso(event.dataTransfer.files[0]);
});
$("#add-files-button").addEventListener("click", () => $("#files-input").click());
$("#files-input").addEventListener("change", (event) => {
  stageFiles([...event.target.files]);
  event.target.value = "";
});
$("#grub-select").addEventListener("change", (event) => {
  if (state.grubDirty && !confirm("Discard unsaved changes to this GRUB file?")) {
    event.target.value = state.selectedGrub;
    return;
  }
  state.selectedGrub = event.target.value;
  $("#grub-editor").value = state.project.grubFiles.find((file) => file.path === state.selectedGrub).content;
  state.grubDirty = false;
  $("#save-grub-button").disabled = true;
});
$("#grub-editor").addEventListener("input", () => {
  state.grubDirty = true;
  $("#save-grub-button").disabled = false;
  $("#grub-status").className = "";
  $("#grub-status").textContent = "Unsaved changes";
});
$("#grub-editor").addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    event.preventDefault();
    const editor = event.currentTarget;
    const start = editor.selectionStart;
    editor.setRangeText("  ", start, editor.selectionEnd, "end");
    editor.dispatchEvent(new Event("input"));
  }
});
$("#save-grub-button").addEventListener("click", async () => {
  try {
    const result = await api("/api/grub", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: state.selectedGrub, content: $("#grub-editor").value }),
    });
    const index = state.project.grubFiles.findIndex((file) => file.path === result.file.path);
    state.project.grubFiles[index] = result.file;
    state.grubDirty = false;
    $("#save-grub-button").disabled = true;
    $("#grub-status").className = "valid";
    $("#grub-status").textContent = result.validation.message;
    toast("GRUB syntax valid and changes saved");
  } catch (error) {
    const validation = error.details?.validation;
    $("#grub-status").className = validation ? "invalid" : "";
    $("#grub-status").textContent = validation?.message || error.message;
    toast(error.message, true);
  }
});
$("#build-button").addEventListener("click", async () => {
  if (state.grubDirty) return toast("Save your GRUB changes before building", true);
  try {
    state.project.build = await api("/api/build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: $("#output-name").value }),
    });
    render();
  } catch (error) { toast(error.message, true); }
});

initialize();
