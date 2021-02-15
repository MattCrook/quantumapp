const showModal = () => {
  MicroModal.init({
    openTrigger: "data-micromodal-trigger",
    closeTrigger: "data-micromodal-close",
    openClass: "is-open",
    disableScroll: true,
    disableFocus: false,
    awaitOpenAnimation: true,
    awaitCloseAnimation: false,
    debugMode: true,
  });
};

const closeOverlaySearchBar = () => {
  const closeButton = document.querySelector(".overlay_close");
  const searchQuantumResults = document.getElementById("search_quantum_results");
  const bodyTag = document.getElementsByTagName("body")[0];
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      searchQuantumResults.style.display = "none";
      bodyTag.classList.toggle("overlay");
      closeButton.style.display = "none";
    });
  }
};

showModal();
closeOverlaySearchBar();
