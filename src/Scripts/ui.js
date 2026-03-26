
document.addEventListener("DOMContentLoaded", () => {
// UI switching
const buttons = document.querySelectorAll(".sidebar button");
const panels = document.querySelectorAll(".panel");

buttons.forEach(btn => {
  btn.onclick = () => {
    const id = btn.dataset.panel;
    panels.forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");

    // Reset projects if leaving
    if(id !== "projects") {
      document.querySelector(".folder-panel").classList.remove("active");
      document.querySelector(".base-projects").style.display = "grid";
    }
  };
});

const folderButtons = document.querySelectorAll(".folder-btn");
const folderPanel = document.querySelector(".folder-panel");
const backButton = document.querySelector(".back-btn");
const baseProjects = document.querySelector(".base-projects");
const projectFolders = document.querySelector(".project-folders");
const folders = document.querySelectorAll(".folder");

function showBase() {
  // Show base + folder buttons
  baseProjects.style.display = "grid";
  projectFolders.style.display = "grid";
  folderPanel.classList.remove("active");

  // Hide everything other than pinned
  backButton.style.display = "none";
  folders.forEach(f => f.style.display = "none");
}

function showFolder(folderId) {
  // Hide pinned
  baseProjects.style.display = "none";
  projectFolders.style.display = "none";

  // Show selected page
  folderPanel.classList.add("active");
  backButton.style.display = "inline-block";

  folders.forEach(f => {
	f.style.display = (f.dataset.folder === folderId) ? "grid" : "none";
  });
}

// Folder button click
folderButtons.forEach(btn => {
  btn.onclick = () => showFolder(btn.dataset.folder);
});

// Back button click
backButton.onclick = showBase;

// Initial state
showBase();
});