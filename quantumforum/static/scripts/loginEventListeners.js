let isLoading = false;
const setIsLoading = (newState) => (isLoading = newState);
const useIsLoading = () => isLoading;

const renderLoading = () => {
  return `
    <main class="modal__content" id="notifications-content">
      <div class="no_notifications_container">
        <div id="loading">
          <div class="loading_text">Loading...</div>
      </div>
    </main>
  `;
};

const showLoading = () => {
  const loadingDiv = document.getElementById("loading_main_container");
  loadingDiv.innerHTML = "";
  const loadingBar = renderLoading();
  loadingDiv.innerHTML += loadingBar;
};

const hideLoading = () => {
  const loadingDiv = document.getElementById("loading_main_container");
  loadingDiv.innerHTML = "";
};

const loading = () => {
  const isLoading = useIsLoading();
  isLoading ? showLoading() : hideLoading();
};

const showHelpModal = () => {
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

const handleNavProfileDropdown = () => {
  const profileDropdownContainer = document.getElementById("profile_dropdown_container");
  const navImage = document.querySelector(".nav_image");
  const close = () => (profileDropdownContainer.style.display = "none");
  const open = () => (profileDropdownContainer.style.display = "block");

  navImage.addEventListener("click", () => {
    const display = profileDropdownContainer.style.display;
    display === "none" && open();
    display === "block" && close();
  });
};

const handleClearSessionStorage = () => {
  const backBtn = document.querySelector(".back_btn");
  const goToProfileBtn = document.getElementById("go_to_profile");
  const goHomeButton = document.getElementById("go_home");

  backBtn.addEventListener("click", () => {
    sessionStorage.clear();
  });
  goToProfileBtn.addEventListener("click", () => {
    sessionStorage.clear();
  });
  goHomeButton.addEventListener("click", () => {
    sessionStorage.clear();
  });
};

const initLogin = () => {
  showHelpModal();
  handleNavProfileDropdown();
  handleClearSessionStorage();
};

initLogin();
