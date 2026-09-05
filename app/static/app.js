const translations = {
  sv: {
    documentTitle: "Ubuntu ISO Builder",
    homeLabel: "Ubuntu ISO Builder startsida",
    ready: "Redo",
    unavailable: "Otillgänglig",
    languageToggle: "English",
    languageToggleLabel: "Byt till engelska",
    buildProgress: "Byggsteg",
    baseImage: "Basavbild",
    addFilesStep: "Lägg till filer",
    bootConfig: "Startkonfiguration",
    buildStep: "Bygg",
    baseImageLabel: "01 / BASAVBILD",
    sourceIso: "Käll-ISO",
    loaded: "Inläst",
    notLoaded: "Inte inläst",
    latestUbuntu: "Hämta senaste Ubuntu",
    canonicalHint: "Hämtas från Canonical och verifieras med SHA-256.",
    ubuntuEdition: "Ubuntu-utgåva",
    desktopEdition: "Desktop (AMD64)",
    serverEdition: "Server (AMD64)",
    downloadIso: "Hämta ISO",
    downloadingIso: "Hämtar ISO…",
    downloadingDesktop: "Hämtar senaste Ubuntu Desktop. Det kan ta flera minuter…",
    downloadingServer: "Hämtar senaste Ubuntu Server. Det kan ta flera minuter…",
    latestLoaded: "Senaste Ubuntu-ISO:n har hämtats och verifierats",
    downloadOutputFirst: "Ladda ned den färdiga ISO:n innan du startar ett nytt bygge.",
    or: "eller",
    dropIso: "Släpp en Ubuntu-ISO här",
    chooseFile: "eller klicka för att välja en fil",
    streamingHint: "Stora filer strömmas direkt till containerns lagring",
    uploadingInspecting: "Laddar upp och granskar avbilden…",
    replace: "Byt ut",
    filesLabel: "02 / FILER",
    filesToInject: "Filer att lägga till",
    addFiles: "+ Lägg till filer",
    staging: "Lägger till…",
    filesHint: "Valda filer placeras direkt i ISO-avbildens rot.",
    noFiles: "Inga filer har lagts till ännu.",
    bootConfigLabel: "03 / STARTKONFIGURATION",
    grubSettings: "GRUB-inställningar",
    saveChanges: "Spara ändringar",
    autoinstall: "Autoinstall",
    enablingAutoinstall: "Aktiverar…",
    autoinstallEnabled: "Autoinstall har aktiverats med direktstart · GRUB-ändringarna har sparats",
    autoinstallAlreadyEnabled: "Autoinstall och direktstart var redan aktiverade · GRUB-syntaxen är giltig",
    configurationFile: "Konfigurationsfil",
    noGrubLoaded: "Ingen GRUB-fil inläst",
    noGrubFound: "Ingen GRUB-konfiguration hittades",
    noGrubPathsFound: "Ingen grub.cfg eller loopback.cfg hittades.",
    uploadToInspectGrub: "Ladda upp eller hämta en ISO för att granska GRUB.",
    grubContents: "GRUB-konfigurationens innehåll",
    grubPlaceholder: "# GRUB-konfigurationen visas här",
    unsavedChanges: "Osparade ändringar",
    grubSaved: "GRUB-syntaxen är giltig · Ändringarna har sparats",
    grubSavedToast: "GRUB-syntaxen är giltig och ändringarna har sparats",
    outputLabel: "04 / UTDATA",
    buildImage: "Bygg avbilden",
    buildHint: "Startmetadata från källan återanvänds i den nya avbilden. Käll-ISO:n ändras aldrig.",
    outputFilename: "Filnamn för utdata",
    buildIso: "Bygg ISO",
    buildLog: "Bygglogg",
    buildQueued: "Bygget väntar…",
    buildRunning: "Din ISO byggs. Det kan ta flera minuter…",
    buildFailed: "Bygget misslyckades",
    unknownError: "Okänt fel",
    buildComplete: "Bygget är klart",
    download: "Ladda ned",
    localTool: "Lokalt verktyg.",
    securityNoticeBefore: "Tjänsten har ingen autentisering. Behåll den på",
    securityNoticeAfter: "eller placera den bakom egen åtkomstkontroll.",
    chooseIso: "Välj en fil som slutar med .iso",
    uploadFailed: "Uppladdningen misslyckades",
    baseLoaded: "Käll-ISO:n lästes in och granskades",
    discardGrub: "Kassera osparade ändringar i den här GRUB-filen?",
    saveBeforeBuild: "Spara GRUB-ändringarna innan du bygger",
    requestFailed: "Begäran misslyckades",
    deleteFile: "Ta bort",
  },
  en: {
    documentTitle: "Ubuntu ISO Builder",
    homeLabel: "Ubuntu ISO Builder home",
    ready: "Ready",
    unavailable: "Unavailable",
    languageToggle: "Svenska",
    languageToggleLabel: "Switch to Swedish",
    buildProgress: "Build progress",
    baseImage: "Base image",
    addFilesStep: "Add files",
    bootConfig: "Boot config",
    buildStep: "Build",
    baseImageLabel: "01 / BASE IMAGE",
    sourceIso: "Source ISO",
    loaded: "Loaded",
    notLoaded: "Not loaded",
    latestUbuntu: "Download latest Ubuntu",
    canonicalHint: "Downloaded from Canonical and verified with SHA-256.",
    ubuntuEdition: "Ubuntu edition",
    desktopEdition: "Desktop (AMD64)",
    serverEdition: "Server (AMD64)",
    downloadIso: "Download ISO",
    downloadingIso: "Downloading…",
    downloadingDesktop: "Downloading the latest Ubuntu Desktop. This can take several minutes…",
    downloadingServer: "Downloading the latest Ubuntu Server. This can take several minutes…",
    latestLoaded: "The latest Ubuntu ISO was downloaded and verified",
    downloadOutputFirst: "Download the completed ISO before starting a new build.",
    or: "or",
    dropIso: "Drop an Ubuntu ISO here",
    chooseFile: "or click to choose a file",
    streamingHint: "Large files are streamed directly to container storage",
    uploadingInspecting: "Uploading and inspecting the image…",
    replace: "Replace",
    filesLabel: "02 / FILES",
    filesToInject: "Files to inject",
    addFiles: "+ Add files",
    staging: "Staging…",
    filesHint: "Selected files are staged immediately at the root of the ISO.",
    noFiles: "No files staged yet.",
    bootConfigLabel: "03 / BOOT CONFIG",
    grubSettings: "GRUB settings",
    saveChanges: "Save changes",
    autoinstall: "Autoinstall",
    enablingAutoinstall: "Enabling…",
    autoinstallEnabled: "Autoinstall enabled with direct boot · GRUB changes saved",
    autoinstallAlreadyEnabled: "Autoinstall and direct boot were already enabled · GRUB syntax valid",
    configurationFile: "Configuration file",
    noGrubLoaded: "No GRUB file loaded",
    noGrubFound: "No GRUB configuration found",
    noGrubPathsFound: "No grub.cfg or loopback.cfg was found.",
    uploadToInspectGrub: "Upload or download an ISO to inspect GRUB.",
    grubContents: "GRUB configuration contents",
    grubPlaceholder: "# GRUB configuration will appear here",
    unsavedChanges: "Unsaved changes",
    grubSaved: "GRUB syntax valid · Changes saved",
    grubSavedToast: "GRUB syntax valid and changes saved",
    outputLabel: "04 / OUTPUT",
    buildImage: "Build the image",
    buildHint: "Boot metadata from the source is replayed into the new image. The source ISO is never modified.",
    outputFilename: "Output filename",
    buildIso: "Build ISO",
    buildLog: "Build log",
    buildQueued: "Build queued…",
    buildRunning: "Building your ISO. This can take several minutes…",
    buildFailed: "Build failed",
    unknownError: "Unknown error",
    buildComplete: "Build complete",
    download: "Download",
    localTool: "Local tool.",
    securityNoticeBefore: "This service has no authentication. Keep it on",
    securityNoticeAfter: "or place it behind your own access control.",
    chooseIso: "Choose a file ending in .iso",
    uploadFailed: "Upload failed",
    baseLoaded: "Base ISO loaded and inspected",
    discardGrub: "Discard unsaved changes to this GRUB file?",
    saveBeforeBuild: "Save your GRUB changes before building",
    requestFailed: "Request failed",
    deleteFile: "Delete",
  },
};

function storedLanguage() {
  try { return localStorage.getItem("ubuntu-builder-language") === "en" ? "en" : "sv"; }
  catch { return "sv"; }
}

const state = {
  project: null,
  selectedGrub: null,
  grubDirty: false,
  pollTimer: null,
  language: storedLanguage(),
  healthAvailable: true,
  sourceBusy: false,
  sourceMode: null,
  sourceError: null,
  staging: false,
  replacing: false,
  autoinstallBusy: false,
  outputDownloadPending: false,
};

const $ = (selector) => document.querySelector(selector);
const t = (key) => translations[state.language][key] || key;

const formatBytes = (bytes) => {
  if (!Number.isFinite(bytes)) return "";
  const units = ["B", "KiB", "MiB", "GiB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit += 1; }
  const formatted = new Intl.NumberFormat(state.language === "sv" ? "sv-SE" : "en", {
    maximumFractionDigits: unit ? 1 : 0,
  }).format(value);
  return `${formatted} ${units[unit]}`;
};
const shortHash = (hash) => hash ? `${hash.slice(0, 12)}…` : "";

const swedishErrors = {
  "Choose an Ubuntu ISO to upload": "Välj en Ubuntu-ISO att ladda upp",
  "The base image must have an .iso extension": "Basavbilden måste ha filändelsen .iso",
  "Each uploaded file needs an ISO destination": "Varje uppladdad fil behöver en plats i ISO-avbilden",
  "Staged file not found": "Den tillagda filen hittades inte",
  "Path and content are required": "Sökväg och innehåll krävs",
  "GRUB validation failed": "GRUB-valideringen misslyckades",
  "GRUB file not found in the base ISO": "GRUB-filen hittades inte i basavbilden",
  "Output ISO not found": "ISO-filen med utdata hittades inte",
  "Upload exceeds MAX_UPLOAD_BYTES": "Uppladdningen överskrider MAX_UPLOAD_BYTES",
  "Not enough Docker storage to receive this ISO": "Det finns inte tillräckligt med Docker-lagring för ISO-filen",
  "A storage error interrupted the upload": "Ett lagringsfel avbröt uppladdningen",
  "Edition must be desktop or server": "Utgåvan måste vara Desktop eller Server",
  "The latest Ubuntu ISO exceeds MAX_UPLOAD_BYTES": "Den senaste Ubuntu-ISO:n överskrider MAX_UPLOAD_BYTES",
  "Downloaded ISO exceeds MAX_UPLOAD_BYTES": "Den hämtade ISO-filen överskrider MAX_UPLOAD_BYTES",
  "The downloaded ISO does not match Canonical's SHA256SUMS": "Den hämtade ISO-filen stämmer inte med Canonicals SHA256SUMS",
  "The uploaded ISO is empty": "Den uppladdade ISO-filen är tom",
  "The uploaded file is not an ISO 9660 image": "Den uppladdade filen är inte en ISO 9660-avbild",
  "Upload a base ISO before staging files": "Ladda upp eller hämta en bas-ISO innan du lägger till filer",
  "Upload a base ISO before building": "Ladda upp eller hämta en bas-ISO innan du bygger",
  "A build is already running": "Ett bygge körs redan",
  "Wait for the current build before replacing the base ISO": "Vänta tills det pågående bygget är klart innan du byter bas-ISO",
  "Wait for the current build before changing staged files": "Vänta tills det pågående bygget är klart innan du ändrar tillagda filer",
  "Wait for the current build before changing GRUB": "Vänta tills det pågående bygget är klart innan du ändrar GRUB",
  "GRUB configuration cannot exceed 2 MiB": "GRUB-konfigurationen får inte överstiga 2 MiB",
  "GRUB validator is unavailable in this container": "GRUB-valideraren är inte tillgänglig i containern",
  "GRUB validation timed out": "GRUB-valideringen tog för lång tid",
  "Select a grub.cfg file to enable autoinstall": "Välj en grub.cfg-fil för att aktivera autoinstall",
  "No Ubuntu installer boot directives were found in this grub.cfg": "Inga startdirektiv för Ubuntu-installationen hittades i denna grub.cfg",
  "No Install Ubuntu menu entry was found in this grub.cfg": "Ingen Install Ubuntu-startpost hittades i denna grub.cfg",
  "The Install Ubuntu menu entry title cannot be safely selected": "Namnet på Install Ubuntu-startposten kan inte väljas säkert",
  "xorriso is not installed in the container": "xorriso är inte installerat i containern",
  "ISO operation timed out": "ISO-åtgärden tog för lång tid",
  "xorriso did not create an output ISO": "xorriso skapade ingen ISO-fil",
};

function localizeMessage(message) {
  if (!message || state.language === "en") return message;
  if (swedishErrors[message]) return swedishErrors[message];
  return message
    .replace(/^GRUB configuration/, "GRUB-konfiguration")
    .replace(/^Build failed: /, "Bygget misslyckades: ")
    .replace(/^A staged file already uses (.+)$/, "En tillagd fil använder redan $1")
    .replace(/^Edit (.+) in the GRUB editor instead$/, "Redigera $1 i GRUB-redigeraren i stället");
}

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
    const error = new Error(body?.error || `${t("requestFailed")} (${response.status})`);
    error.details = body;
    throw error;
  }
  return body;
}

function applyLanguage({ persist = true } = {}) {
  const dirtyGrubContent = state.grubDirty ? $("#grub-editor").value : null;
  document.documentElement.lang = state.language;
  document.title = t("documentTitle");
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
  });
  const toggle = $("#language-toggle");
  toggle.textContent = t("languageToggle");
  toggle.setAttribute("aria-label", t("languageToggleLabel"));
  toggle.setAttribute("lang", state.language === "sv" ? "en" : "sv");
  $("#health-text").textContent = state.healthAvailable ? t("ready") : t("unavailable");
  if (persist) {
    try { localStorage.setItem("ubuntu-builder-language", state.language); } catch { /* storage unavailable */ }
  }
  if (state.project) {
    render();
    if (dirtyGrubContent !== null) {
      $("#grub-editor").value = dirtyGrubContent;
      state.grubDirty = true;
      $("#save-grub-button").disabled = false;
      $("#grub-status").textContent = t("unsavedChanges");
    }
  }
}

function renderBase() {
  const base = state.project.baseIso;
  const buildBusy = ["queued", "running"].includes(state.project.build.status);
  const outputWaiting = state.project.build.status === "complete" && state.project.build.output;
  const sourceLocked = state.sourceBusy || buildBusy || outputWaiting;
  const choosingSource = !base || state.replacing;
  $("#base-badge").textContent = base ? t("loaded") : t("notLoaded");
  $("#base-badge").className = `badge ${base ? "ready" : "muted"}`;
  $("#source-options").classList.toggle("hidden", !choosingSource);
  $("#iso-input").disabled = sourceLocked;
  $("#iso-dropzone").classList.toggle("is-disabled", sourceLocked);
  $("#ubuntu-edition").disabled = sourceLocked;
  const downloadButton = $("#download-ubuntu-button");
  downloadButton.disabled = sourceLocked;
  downloadButton.textContent = state.sourceBusy ? t("downloadingIso") : t("downloadIso");
  const sourceStatus = $("#source-status");
  if (outputWaiting && choosingSource) {
    sourceStatus.className = "source-status";
    sourceStatus.textContent = t("downloadOutputFirst");
  } else if (state.sourceMode === "download") {
    sourceStatus.className = "source-status";
    sourceStatus.textContent = t($("#ubuntu-edition").value === "server" ? "downloadingServer" : "downloadingDesktop");
  } else if (state.sourceMode === "error") {
    sourceStatus.className = "source-status error";
    sourceStatus.textContent = localizeMessage(state.sourceError);
  } else if (state.sourceMode !== "error") {
    sourceStatus.classList.add("hidden");
  }
  const summary = $("#base-summary");
  summary.classList.toggle("hidden", !base || state.replacing);
  if (base && !state.replacing) {
    summary.replaceChildren();
    const details = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = base.name;
    const meta = document.createElement("span");
    meta.textContent = `${formatBytes(base.size)} · SHA-256 ${shortHash(base.sha256)}`;
    details.append(name, meta);
    const replace = document.createElement("button");
    replace.type = "button";
    replace.textContent = t("replace");
    replace.disabled = buildBusy;
    replace.addEventListener("click", () => {
      state.replacing = true;
      renderBase();
    });
    summary.append(details, replace);
  }
  const addButton = $("#add-files-button");
  addButton.disabled = !base || buildBusy || state.staging || state.replacing;
  addButton.textContent = state.staging ? t("staging") : t("addFiles");
  $("#build-button").disabled = !base || buildBusy || state.replacing;
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
    container.textContent = t("noFiles");
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
    remove.setAttribute("aria-label", `${t("deleteFile")} ${item.name}`);
    remove.addEventListener("click", async () => {
      try {
        await api(`/api/files/${encodeURIComponent(item.id)}`, { method: "DELETE" });
        state.project.files = state.project.files.filter((file) => file.id !== item.id);
        renderFiles();
      } catch (error) { toast(localizeMessage(error.message), true); }
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
  $("#grub-status").className = "";
  if (!files.length) {
    const option = document.createElement("option");
    option.textContent = state.project.baseIso ? t("noGrubFound") : t("noGrubLoaded");
    select.append(option);
    select.disabled = true;
    editor.disabled = true;
    editor.value = "";
    $("#grub-status").textContent = state.project.baseIso ? t("noGrubPathsFound") : t("uploadToInspectGrub");
    $("#save-grub-button").disabled = true;
    renderAutoinstallButton();
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
  renderAutoinstallButton();
  $("#grub-status").textContent = state.language === "sv"
    ? `${files.length} ${files.length === 1 ? "konfigurationsfil hittad" : "konfigurationsfiler hittade"}`
    : `${files.length} configuration file${files.length === 1 ? "" : "s"} found`;
}

function renderAutoinstallButton() {
  const button = $("#autoinstall-button");
  const buildBusy = state.project && ["queued", "running"].includes(state.project.build.status);
  const hasGrubCfg = state.selectedGrub?.split("/").pop() === "grub.cfg";
  button.disabled = !hasGrubCfg || buildBusy || state.autoinstallBusy;
  button.textContent = t(state.autoinstallBusy ? "enablingAutoinstall" : "autoinstall");
}

async function enableGrubAutoinstall() {
  state.autoinstallBusy = true;
  renderAutoinstallButton();
  try {
    const result = await api("/api/grub/autoinstall", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: state.selectedGrub, content: $("#grub-editor").value }),
    });
    const index = state.project.grubFiles.findIndex((file) => file.path === result.file.path);
    state.project.grubFiles[index] = result.file;
    $("#grub-editor").value = result.file.content;
    state.grubDirty = false;
    $("#save-grub-button").disabled = true;
    $("#grub-status").className = "valid";
    const messageKey = result.autoinstall.added || result.autoinstall.bootChanged
      ? "autoinstallEnabled"
      : "autoinstallAlreadyEnabled";
    $("#grub-status").textContent = t(messageKey);
    toast(t(messageKey));
  } catch (error) {
    const validation = error.details?.validation;
    $("#grub-status").className = validation ? "invalid" : "";
    $("#grub-status").textContent = localizeMessage(validation?.message || error.message);
    toast(localizeMessage(error.message), true);
  } finally {
    state.autoinstallBusy = false;
    renderAutoinstallButton();
  }
}

function renderBuild() {
  const build = state.project.build;
  const result = $("#build-result");
  const log = $("#build-log");
  result.className = `build-result ${build.status === "idle" ? "hidden" : build.status}`;
  result.replaceChildren();
  if (["queued", "running"].includes(build.status)) {
    result.textContent = build.status === "queued" ? t("buildQueued") : t("buildRunning");
  } else if (build.status === "failed") {
    result.textContent = `${t("buildFailed")}: ${localizeMessage(build.error) || t("unknownError")}`;
  } else if (build.status === "complete" && build.output) {
    const message = document.createElement("div");
    message.textContent = `${t("buildComplete")} · ${formatBytes(build.output.size)}`;
    const link = document.createElement("a");
    link.className = "download-link";
    link.href = `/api/output/${encodeURIComponent(build.output.name)}`;
    link.textContent = `${t("download")} ${build.output.name}`;
    const arrow = document.createElement("span");
    arrow.textContent = "↓";
    link.append(arrow);
    link.addEventListener("click", () => {
      state.outputDownloadPending = true;
      schedulePoll();
    });
    result.append(message, link);
  }
  log.classList.toggle("hidden", !build.log?.length);
  log.querySelector("pre").textContent = (build.log || []).join("\n");
  $("#build-button").disabled = !state.project.baseIso || ["queued", "running"].includes(build.status) || state.replacing;
  if (build.status === "idle") state.outputDownloadPending = false;
  if (["queued", "running"].includes(build.status) || (state.outputDownloadPending && build.status === "complete")) {
    schedulePoll();
  }
}

function render() {
  renderBase();
  renderFiles();
  renderGrub();
  renderBuild();
}

function uploadIso(file) {
  if (!file || !file.name.toLowerCase().endsWith(".iso")) return toast(t("chooseIso"), true);
  const data = new FormData();
  data.append("iso", file);
  const request = new XMLHttpRequest();
  const progress = $("#iso-progress");
  state.sourceBusy = true;
  state.sourceMode = "upload";
  state.sourceError = null;
  renderBase();
  progress.classList.remove("hidden");
  request.upload.addEventListener("progress", (event) => {
    if (!event.lengthComputable) return;
    const percent = Math.round((event.loaded / event.total) * 100);
    progress.querySelector(".progress-track span").style.width = `${percent}%`;
    $("#iso-progress-label").textContent = `${percent}%`;
  });
  request.addEventListener("load", () => {
    progress.classList.add("hidden");
    state.sourceBusy = false;
    state.sourceMode = null;
    try {
      let body = {};
      try { body = JSON.parse(request.responseText || "{}"); } catch { /* non-JSON server failure */ }
      if (request.status < 200 || request.status >= 300) throw new Error(body.error || t("uploadFailed"));
      state.project = body;
      state.selectedGrub = null;
      state.replacing = false;
      render();
      toast(t("baseLoaded"));
    } catch (error) {
      renderBase();
      toast(localizeMessage(error.message), true);
    }
  });
  request.addEventListener("error", () => {
    progress.classList.add("hidden");
    state.sourceBusy = false;
    state.sourceMode = null;
    renderBase();
    toast(t("uploadFailed"), true);
  });
  request.open("POST", "/api/base-iso");
  request.send(data);
}

async function downloadLatestUbuntu() {
  const status = $("#source-status");
  const edition = $("#ubuntu-edition").value;
  state.sourceBusy = true;
  state.sourceMode = "download";
  state.sourceError = null;
  status.className = "source-status";
  status.textContent = t(edition === "server" ? "downloadingServer" : "downloadingDesktop");
  renderBase();
  try {
    state.project = await api("/api/base-iso/latest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ edition }),
    });
    state.selectedGrub = null;
    state.replacing = false;
    toast(t("latestLoaded"));
  } catch (error) {
    state.sourceMode = "error";
    state.sourceError = error.message;
    status.className = "source-status error";
    status.textContent = localizeMessage(error.message);
    toast(localizeMessage(error.message), true);
  } finally {
    state.sourceBusy = false;
    render();
    if (state.sourceMode !== "error") state.sourceMode = null;
    if (state.project.baseIso) status.classList.add("hidden");
  }
}

async function stageFiles(files) {
  if (!files.length) return;
  const data = new FormData();
  for (const file of files) {
    const relative = file.webkitRelativePath || file.name;
    data.append("files", file);
    data.append("destinations", `/${relative.replaceAll("\\", "/")}`);
  }
  state.staging = true;
  renderBase();
  try {
    const body = await api("/api/files", { method: "POST", body: data });
    state.project.files.push(...body.files);
    renderFiles();
    const message = state.language === "sv"
      ? `${body.files.length} ${body.files.length === 1 ? "fil tillagd" : "filer tillagda"}`
      : `${body.files.length} file${body.files.length === 1 ? "" : "s"} staged`;
    toast(message);
  } catch (error) {
    toast(localizeMessage(error.message), true);
  } finally {
    state.staging = false;
    renderBase();
  }
}

function schedulePoll() {
  clearTimeout(state.pollTimer);
  state.pollTimer = setTimeout(async () => {
    try {
      state.project = await api("/api/state");
      render();
    } catch (error) { toast(localizeMessage(error.message), true); }
  }, 1500);
}

async function initialize() {
  try {
    state.project = await api("/api/state");
    render();
  } catch (error) {
    state.healthAvailable = false;
    $("#health-text").textContent = t("unavailable");
    toast(localizeMessage(error.message), true);
  }
}

$("#language-toggle").addEventListener("click", () => {
  state.language = state.language === "sv" ? "en" : "sv";
  applyLanguage();
});
$("#download-ubuntu-button").addEventListener("click", downloadLatestUbuntu);
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
  if (state.grubDirty && !confirm(t("discardGrub"))) {
    event.target.value = state.selectedGrub;
    return;
  }
  state.selectedGrub = event.target.value;
  $("#grub-editor").value = state.project.grubFiles.find((file) => file.path === state.selectedGrub).content;
  state.grubDirty = false;
  $("#save-grub-button").disabled = true;
  renderAutoinstallButton();
});
$("#grub-editor").addEventListener("input", () => {
  state.grubDirty = true;
  $("#save-grub-button").disabled = false;
  $("#grub-status").className = "";
  $("#grub-status").textContent = t("unsavedChanges");
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
    $("#grub-status").textContent = t("grubSaved");
    toast(t("grubSavedToast"));
  } catch (error) {
    const validation = error.details?.validation;
    $("#grub-status").className = validation ? "invalid" : "";
    $("#grub-status").textContent = localizeMessage(validation?.message || error.message);
    toast(localizeMessage(error.message), true);
  }
});
$("#autoinstall-button").addEventListener("click", enableGrubAutoinstall);
$("#build-button").addEventListener("click", async () => {
  if (state.grubDirty) return toast(t("saveBeforeBuild"), true);
  try {
    state.project.build = await api("/api/build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: $("#output-name").value }),
    });
    render();
  } catch (error) { toast(localizeMessage(error.message), true); }
});

applyLanguage({ persist: false });
initialize();
