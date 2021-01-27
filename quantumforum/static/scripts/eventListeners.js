const showCreateGroupForm = () => {
  const createNewGroupContainer = document.getElementById("new_group_create_form_container");
  const createNewGroupBtn = document.querySelector(".create_new_group_chat_btn");

  if (createNewGroupBtn) {
    createNewGroupBtn.addEventListener("click", () => {
      createNewGroupContainer.style.display = "block";
    });
  }
};

const closeCreateGroupForm = () => {
  const closeButton = document.querySelector(".close_form");
  const createNewGroupContainer = document.getElementById("new_group_create_form_container");

  closeButton.addEventListener("click", () => {
    createNewGroupContainer.style.display = "none";
  });
};

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

const handleProfileDropdown = () => {
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



const initEventListeners = () => {
  showCreateGroupForm();
  closeCreateGroupForm();
  showModal();
  handleProfileDropdown();
};

initEventListeners();
