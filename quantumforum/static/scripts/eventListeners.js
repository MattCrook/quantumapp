const showCreateGroupForm = () => {
  // const createNewGroupContainer = document.querySelector(".new_group_create_form_container");

  const createNewGroupContainer = document.getElementById("new_group_create_form_container");
  const createNewGroupBtn = document.querySelector(".create_new_group_chat_btn");

  if (createNewGroupBtn) {
    createNewGroupBtn.addEventListener("click", () => {
      createNewGroupContainer.style.display = "block";
    });
  }
};

const initEventListeners = () => {
  showCreateGroupForm();
};

initEventListeners();
