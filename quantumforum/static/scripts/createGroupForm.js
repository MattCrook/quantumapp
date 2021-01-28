import { useQuantumFriends, useLoading, useGroupChatParticipants } from "./hooks.js";
import { getAllUsersFriends, retrieveUserProfile } from "./services.js";

const [participants, setParticipants] = useGroupChatParticipants();

const initFriendsSearchAndForm = async () => {
  const [friendships, setFriendships] = useQuantumFriends();
  const search_input = document.getElementById("friends_search");
  const results = document.getElementById("results");

  const allFriendships = await getAllUsersFriends();
  setFriendships(allFriendships);
  defaultRenderFriendData(friendships(), results);
  handleSearchInput(search_input);

  const addUserNodes = document.querySelectorAll(".fas.fa-plus");
  const addUserButtons = [...addUserNodes];
  addUserButtons.forEach((button) => {
    handleAddFriendToGroup(button);
  });
  handleClearAllEvent();
};


const filterSearchQuery = (friendships, search_term) => {
  const results = document.getElementById("results");
  results.innerHTML = "";

  friendships
    .filter(
      (friend) =>
        friend.user.first_name.toLowerCase().includes(search_term.toLowerCase()) ||
        friend.user.last_name.toLowerCase().includes(search_term.toLowerCase()) ||
        friend.user.username.toLowerCase().includes(search_term.toLowerCase())
    )
    .forEach((friend) => {
      let row;
      friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
      results.innerHTML += row;
    });
};


const handleSearchInput = (search_input) => {
  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    filterSearchQuery(friendships(), search_term);
  });
};


const handleAddFriendToGroup = (addUserButton) => {
  const [isLoading, setIsLoading] = useLoading(false);
  const inviteList = document.querySelector(".invitee_list");

  addUserButton.addEventListener("click", async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const userId = e.target.dataset.id;
    const user = await retrieveUserProfile(parseInt(userId));
    setParticipants([user]);

    const newParticipantRow = invitedUserToGroup(user);
    inviteList.innerHTML += newParticipantRow;
    setIsLoading(false);
    // alert(`${user.user.first_name} ${user.user.last_name} added to group chat.`);

    toggleAddCheckIcon(e.target, true);
    handleRemoveUserFromList(e.target);
  });
};


const defaultRenderFriendData = (friendshipList, results) => {
  friendshipList.forEach((friend) => {
    let row;
    friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
    results.innerHTML += row;
  });
};


const toggleAddCheckIcon = (eventTarget, isToggle) => {
  const uid = eventTarget.dataset.id;
  if (isToggle) {
    const parentContainer = eventTarget.parentNode;
    parentContainer.innerHTML = "";
    const checkIcon = renderCheckIcon(uid);
    parentContainer.innerHTML += checkIcon;
  } else {
    console.log({eventTarget})
    const addIcon = renderAddIcon(uid);
    const checkIconNodes = document.querySelectorAll(".fas.fa-plus");
    const checkIcons = Array.from(checkIconNodes);
    const iconToChange = checkIcons.filter(icon => icon.dataset.id === uid)
    const parentContainer = iconToChange.parentNode;
    parentContainer.innerHTML = "";
    parentContainer.inner += addIcon;
  }
};


/*
const hideCheckShowUserAddIcon = (eventTarget) => {
  const uid = eventTarget.dataset.id;
  const parentContainer = eventTarget.parentNode;
  parentContainer.innerHTML = "";

  console.log({eventTarget});
  // eventTarget.remove();
  const addIcon = renderAddIcon(uid);
  parentContainer.innerHTML += addIcon;
};
*/


const handleClearAllEvent = () => {
  const clearAllBtn = document.querySelector(".clear_all_button");
  const inviteList = document.querySelector(".invitee_list");
  clearAllBtn.addEventListener("click", () => {
    inviteList.innerHTML = "";
  });
};


const handleRemoveUserFromList = (eventTarget) => {
  const removeInviteeNodes = document.querySelectorAll(".remove_participant");
  const removeInviteeButtons = [...removeInviteeNodes];

  const allParticipantsNodes = document.querySelectorAll(".participant_item_container");
  const allParticipantContainers = Array.from(allParticipantsNodes);

  removeInviteeButtons.forEach((removeButton) => {
    removeButton.addEventListener("click", (e) => {
      e.preventDefault();
      const key = e.target.dataset.id;
      const parentNode = e.target.parentNode;
      const nodeKeys = allParticipantContainers.map((node) => node.dataset.key);
      const match = nodeKeys.includes(key);

      if (match) {
        const containerToRemove = allParticipantContainers.filter((element) => element.dataset.key === key);
        containerToRemove[0].remove();
        toggleAddCheckIcon(eventTarget, false);
      }
    });
  });
};


function renderFriendRowWithImage(friend) {
  return `
    <div class="add_friend_card">
      <div id="add_friend_card_container_1">
        <div class="add_friend_profile_pic">
          <img class="add_friend_card_img" src="${friend.image.image}" />
        </div>
      <div class="add_friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
    </div>
      <div id="add_friend_card_container_2">
        <i d="fa_plus_add_user" class="fas fa-plus"></i>
      </div>
    </div>
    `;
}

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

function invitedUserToGroup(user) {
  return `
    <div class="participant_item_container" data-key="${user.id}">
      <div class="participant_item_wrapper_1">
        <li class="participant_item"> ${user.user.first_name} ${user.user.last_name}</li>
      </div>
      <div class="participant_item_wrapper_2">
        <button class="remove_participant" data-id="${user.id}"></button>
      </div>
    </div>
  `;
}

function renderAddIcon() {
  return `
      <div class="send_friend_request_btn"><i class="fas fa-user-plus"></i></div>
      `;
}

function renderCheckIcon(uid) {
  return `
      <i id="fa_check_user_added" class="fas fa-check" data-id="${uid}"></i>
      `;
}

function renderClearAllButton() {
  return `
      <div class="clear_all_button">Clear All</div>
  `;
}

initFriendsSearchAndForm();
