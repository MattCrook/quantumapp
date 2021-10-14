import { getAllUsersFriends, retrieveUserProfile, getGroupChat } from "./services.js";
import { useLoading } from "./hooks.js";


let group = [];



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

const initUserFriendData = async () => {
  try {
    const searchInput = document.getElementById("friends_search");
    const results = document.getElementById("results");
    const addedToGroupList = document.querySelector(".edit_group_ul");
    let search_term = "";

    const allFriendships = await getAllUsersFriends();
    const groupChatId = parseInt(window.location.pathname.split("/")[2]);
    const currentGroupChat = await getGroupChat(groupChatId);
    const groupMemberIds = currentGroupChat.group_members.map(member => member.id);
    const friendsExcludingGroup = allFriendships.filter(friend => !groupMemberIds.includes(friend.id));

    initialRenderFriendList(friendsExcludingGroup, results, addedToGroupList);
    handleSearchInput(friendsExcludingGroup, searchInput, search_term, results, addedToGroupList);
  } catch (error) {
    console.log(error);
  }
};

const initialRenderFriendList = (friends, results, addedToGroupList) => {
  results.innerHTML = "";
  friends.forEach((friend) => {
    let row;
    friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
    results.innerHTML += row;
  });
  initSelectUserToAdd(addedToGroupList);
};

const initSelectUserToAdd = (addedToGroupList) => {
  const addUserNodes = document.querySelectorAll(".fas.fa-plus");
  const addUserButtons = [...addUserNodes];
  addUserButtons.forEach((button) => {
    handleAddFriendToGroup(button, addedToGroupList);
  });
};

const handleSearchInput = (friends, searchInput, search_term, results, addedToGroupList) => {
  searchInput.addEventListener("input", (e) => {
    search_term = e.target.value;
    filterSearchQuery(friends, search_term, results);
    initSelectUserToAdd(addedToGroupList);
  });
};

const filterSearchQuery = (friends, search_term, results) => {
  results.innerHTML = "";

  const filteredResults = friends.filter(
    (friend) =>
      friend.user.first_name.toLowerCase().includes(search_term.toLowerCase()) ||
      friend.user.last_name.toLowerCase().includes(search_term.toLowerCase()) ||
      friend.user.username.toLowerCase().includes(search_term.toLowerCase())
  );
  filteredResults.forEach((friend) => {
    let row;
    const isFriendImage = friend && friend.image && friend.image != null;
    const addedFriendToGroup = searchFriendIdInList(participants, friend.id);
    const hasGroupParticipants = Array.isArray(addedFriendToGroup) || addedFriendToGroup.length;
    const isAddedToGroup = hasGroupParticipants ? addedFriendToGroup[0].id === friend.id : false;

    const isImageAndIsAdded = () => (row = renderAddedFriendRowWithImage(friend));
    const isImageAndNotAdded = () => (row = renderFriendRowWithImage(friend));
    const noImageAndIsAdded = () => (row = renderAddedFriendRowNoImage(friend));
    const noImageAndNotAdded = () => (row = renderFriendRowNoImage(friend));

    isFriendImage && isAddedToGroup && isImageAndIsAdded();
    isFriendImage && !isAddedToGroup && isImageAndNotAdded();
    !isFriendImage && isAddedToGroup && noImageAndIsAdded();
    !isFriendImage && !isAddedToGroup && noImageAndNotAdded();

    results.innerHTML += row;
  });
};

const handleAddFriendToGroup = (addUserButton, addedToGroupList) => {
  const [isLoading, setIsLoading] = useLoading(false);
  addUserButton.addEventListener("click", async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const userId = e.target.dataset.id;
    const userProfile = await retrieveUserProfile(parseInt(userId));
    setIsLoading(false);
    renderAddedUserToInviteList(e, userProfile, addedToGroupList);
  });
};

const renderAddedUserToInviteList = (e, user, addedToGroupList) => {
  const newMemberRow = invitedUserToGroup(user);
  addedToGroupList.innerHTML += newMemberRow;
  addCheckIconAfterAddingUser(e);
};

const addCheckIconAfterAddingUser = (e) => {
  e.preventDefault();
  const eventTarget = e.target;
  const uid = eventTarget.dataset.id;
  // Get the event from clicking the add icon, that gives you the icon to toggle to check icon.
  // Replace with check icon.
  const parentContainer = eventTarget.parentNode;
  parentContainer.innerHTML = "";
  const checkIcon = renderCheckIcon(uid);
  parentContainer.innerHTML += checkIcon;
};








function renderFriendRowNoImage(friend) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  return `
      <div class="add_friend_card">
        <div id="add_friend_card_container_1">
          <div class="add_friend_profile_pic">
              <img class="add_friend_card_img" src="${default_profile_pic}" />
          </div>
          <div class="add_friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
        </div>
        <div id="add_friend_card_container_2">
            <i id="fa_plus_add_user" class="fas fa-plus" data-id="${friend.id}"></i>
        </div>
      </div>
      `;
}

function renderAddedFriendRowWithImage(friend) {
  return `
    <div class="add_friend_card">
      <div id="add_friend_card_container_1">
        <div class="add_friend_profile_pic">
          <img class="add_friend_card_img" src="${friend.image.image}" />
        </div>
      <div class="add_friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
    </div>
      <div id="add_friend_card_container_2">
      <i id="fa_check_user_added" class="fas fa-check" data-id="${friend.id}"></i>
      </div>
    </div>
    `;
}

function renderAddedFriendRowNoImage(friend) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  return `
      <div class="add_friend_card">
        <div id="add_friend_card_container_1">
          <div class="add_friend_profile_pic">
              <img class="add_friend_card_img" src="${default_profile_pic}" />
          </div>
          <div class="add_friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
        </div>
        <div id="add_friend_card_container_2">
        <i id="fa_check_user_added" class="fas fa-check" data-id="${friend.id}"></i>
        </div>
      </div>
      `;
}

function invitedUserToGroup(userProfile) {
  return `
    <div class="edit_group_members_list_item">
    <li class="group_members_list_item" data-id="${userProfile.id}">
        ${userProfile.user.first_name} ${userProfile.user.last_name}</li>
    <button class="remove_group_member" data-id="${userProfile.id}"></button>
  </div>
  `;
}


function renderAddIcon(friendId) {
  return `
      <i id="fa_plus_add_user" class="fas fa-plus" data-id="${friendId}"></i>
      `;
}

function renderCheckIcon(uid) {
  return `
      <i id="fa_check_user_added" class="fas fa-check" data-id="${uid}"></i>
      `;
}


const initAddMemberForm = () => {
  showModal();
  initUserFriendData();
};

initAddMemberForm();
