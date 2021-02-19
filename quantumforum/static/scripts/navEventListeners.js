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

// Handles the 'X' button in the search users bar.
const closeOverlaySearchBarButton = () => {
  const closeButton = document.querySelector(".overlay_close");
  const searchQuantumResults = document.getElementById("search_quantum_results_master_container");
  const nav = document.querySelector(".nav");
  const currentGroupChats = document.querySelector(".current_group_chats_container");

  const bodyTag = document.getElementsByTagName("body")[0];
  if (closeButton) {
    closeButton.addEventListener("click", () => {
      searchQuantumResults.style.display = "none";
      bodyTag.classList.toggle("overlay");
      closeButton.style.display = "none";
      nav.style.boxShadow = "0px 6px 4px 0px rgb(190 190 190)";
      currentGroupChats.style.boxShadow = "2px 6px 4px 0px rgb(190 190 190)";
    });
  }
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

const handleShowNotifications = () => {
  const notificationsButton = document.querySelector(".notifications_header");
  const friendsListModalContainer = document.querySelector(".friends_list");
  const friendsButton = document.querySelector(".friends_header");

  notificationsButton.addEventListener("click", () => {
    friendsListModalContainer.style.display = "none";
    notificationsButton.style.display = "none";
    friendsButton.style.display = "block";
    showNotificationsBody();
  });
};

const showNotificationsBody = () => {
  const notificationsContainer = document.querySelector(".notifications");
  notificationsContainer.style.display = "block";
  notificationsContainer.innerHTML = "";
  const render = renderNotifications();
  notificationsContainer.innerHTML += render;
};

const handleShowFriendsList = () => {
  const notificationsButton = document.querySelector(".notifications_header");
  const friendsListModalContainer = document.querySelector(".friends_list");
  const friendsButton = document.querySelector(".friends_header");
  friendsButton.addEventListener("click", () => {
    notificationsButton.style.display = "block";
    friendsListModalContainer.style.display = "block";
    friendsButton.style.display = "none";
  });
};

function renderNotifications() {
  return `
  <div>HELLO</div>
  `;
}

const initNav = () => {
  showModal();
  closeOverlaySearchBarButton();
  handleNavProfileDropdown();
  handleClearSessionStorage();
  handleShowNotifications();
  handleShowFriendsList();
};

initNav();
