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

const initEventListeners = () => {
  showCreateGroupForm();
  closeCreateGroupForm();
  showModal();
};

initEventListeners();
