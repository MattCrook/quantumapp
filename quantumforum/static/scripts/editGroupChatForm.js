let isLoading = false;
const setIsLoading = (newState) => (isLoading = newState);
const useIsLoading = () => isLoading;

let groupMembers = [];
const setGroup = (newGroup) => (groupMembers = newGroup);
const useGroup = () => groupMembers;

const renderLoadingScreen = () => {
  return `
    <div class="loading fade_in">
    <div class="loading-text">
        <span class="loading-text-words">L</span>
        <span class="loading-text-words">O</span>
        <span class="loading-text-words">A</span>
        <span class="loading-text-words">D</span>
        <span class="loading-text-words">I</span>
        <span class="loading-text-words">N</span>
        <span class="loading-text-words">G</span>
    </div>
    </div>
    `;
};

const displayLoadingScreen = () => {
  const mainContainer = document.querySelector(".group_edit_master_container");
  const loadingDiv = document.getElementById("loading");
  mainContainer.style.display = "none";
  const loadingGraphic = renderLoadingScreen();
  loadingDiv.innerHTML += loadingGraphic;
};

const loading = () => {
  const isLoading = useIsLoading();
  isLoading ? displayLoadingScreen() : null;
};

const exitEditForm = () => {
  const exitEditFormButton = document.querySelector(".group_chat_edit_back_to_previous");
  exitEditFormButton.addEventListener("click", (e) => {
    e.preventDefault();
    setIsLoading(true);
    loading();
    const path = window.location.pathname;
    const groupId = parseInt(path.split("/")[2]);
    setIsLoading(false);
    loading();
    setTimeout(() => {
      window.location.pathname = `group_chat/${groupId}/confirm`;
    }, 1800);
  });
};

const back = () => {
  const backButton = document.querySelector(".back_edit_group");
  backButton.addEventListener("click", (e) => {
    e.preventDefault();
    setIsLoading(true);
    loading();
    const path = window.location.pathname;
    const groupId = parseInt(path.split("/")[2]);
    console.log(path);
    console.log(groupId);
    setIsLoading(false);
    loading();
    setTimeout(() => {
      window.location.pathname = `group_chat/${groupId}/confirm`;
    }, 1800);
  });
};

const clearInputOnFocus = () => {
  const inputNodes = document.querySelectorAll(".form_input");
  const inputs = Array.from(inputNodes);
  inputs.forEach((input) => {
    input.addEventListener("focus", (e) => {
      e.target.style.color = "transparent";
    });
  });
};

const showInputs = () => {
  const form = document.querySelector(".group_edit_master_container");

  form.addEventListener("mouseout", (e) => {
    const inputNodes = document.querySelectorAll(".form_input");
    const inputs = Array.from(inputNodes);
    inputs.forEach((input) => {
      input.style.color === "transparent" ? (input.style.color = "black") : (input.style.color = "black");
    });
  });
};

const handleRemoveMemberFromGroup = () => {
  let membersCurrentlyInGroup = [];
  const removeButtonNodes = document.querySelectorAll(".remove_group_member");
  const removeButtons = [...removeButtonNodes];
  const membersListNodes = document.querySelectorAll(".group_members_list_item");
  const memberListElements = [...membersListNodes];

  memberListElements.forEach((member) => membersCurrentlyInGroup.push(member.dataset.id));
  setGroup(membersCurrentlyInGroup);
  const removedUserProfileId = new Set();

  removeButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const dataId = e.target.dataset.id;
      removedUserProfileId.add(dataId);
      const memberToRemove = memberListElements.filter((member) => member.dataset.id === dataId);
      e.target.remove();
      memberToRemove[0].remove();

      const memberToRemoveFromGroup = [...removedUserProfileId];
      const groupExcludingRemovedMember = groupMembers.filter((memberId) => memberId !== memberToRemoveFromGroup.pop());
      setGroup(groupExcludingRemovedMember);
    });
  });
};

const initGroupEditFormEvents = () => {
  exitEditForm();
  clearInputOnFocus();
  showInputs();
  back();
  handleRemoveMemberFromGroup();
};

initGroupEditFormEvents();
