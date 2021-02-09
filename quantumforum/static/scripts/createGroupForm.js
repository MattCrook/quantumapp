import {
  useQuantumFriends,
  useLoading,
  useGroupChatParticipants,
  useUserList,
  useGroup,
  useAddedToGroup,
} from "./hooks.js";
import { getAllUsersFriends, retrieveUserProfile } from "./services.js";


// const [addedToGroup, addedToGroup] = useAddedToGroup();
// const [participants, setParticipants] = useGroupChatParticipants();
// const [friendships, setFriendships] = useQuantumFriends();
// const [group, setGroup] = useGroup([...participants()]);

let participants = [];
let addedToGroup = [];
let friendShips = new Set();
let group = new Set()


const initFriendsSearchAndCreateGroupForm = async () => {
  try {
    const searchInput = document.getElementById("friends_search");
    const results = document.getElementById("results");
    const addedToGroupList = document.querySelector(".invitee_list");
    let search_term = '';

    const allFriendships = await getAllUsersFriends();
    friendShips.add(allFriendships);
    setFormState(friendShips, searchInput, search_term, results, addedToGroupList);
  } catch (error) {
    console.log(error)
  }
};


const setFormState = (friendShips, searchInput, search_term, results, addedToGroupList) => {
  const friendShipEntries = friendShips.values()
  const allUserFriendships = friendShipEntries.next().value;
  initialRenderFriendShipData(allUserFriendships, results, searchInput, addedToGroupList);
  handleSearchInput(allUserFriendships, searchInput, search_term, results, addedToGroupList);
};


const initSelectUserToAdd = (results, searchInput, addedToGroupList) => {
  const addUserNodes = document.querySelectorAll(".fas.fa-plus");
  const addUserButtons = [...addUserNodes];
  addUserButtons.forEach((button) => {
    handleAddFriendToGroup(button, results, addedToGroupList);
  });
  handleClearAllEvent(results, searchInput, addedToGroupList);
};


const initialRenderFriendShipData = (friendshipList, results, searchInput, addedToGroupList) => {
  results.innerHTML = '';
  friendshipList.forEach((friend) => {
    let row;
    friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
    results.innerHTML += row;
  });
  initSelectUserToAdd(results, searchInput, addedToGroupList);
};


const handleSearchInput = (friendShips, searchInput, search_term, results, addedToGroupList) => {
  searchInput.addEventListener("input", (e) => {
    search_term = e.target.value;
    filterSearchQuery(friendShips, search_term, results, addedToGroupList, searchInput);
    initSelectUserToAdd(results, searchInput, addedToGroupList);
  });
};


const filterSearchQuery = (friendships, search_term, results) => {
  results.innerHTML = "";

  const filteredResults = friendships.filter((friend) =>
        friend.user.first_name.toLowerCase().includes(search_term.toLowerCase()) ||
        friend.user.last_name.toLowerCase().includes(search_term.toLowerCase()) ||
        friend.user.username.toLowerCase().includes(search_term.toLowerCase())
    )
    filteredResults.forEach((friend) => {
      let row;
      const isFriendImage = friend && friend.image && friend.image != null;
      const addedFriendToGroup = searchFriendIdInList(participants, friend.id);
      const hasGroupParticipants = Array.isArray(addedFriendToGroup) || addedFriendToGroup.length
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


const handleAddFriendToGroup = (addUserButton, results, addedToGroupList) => {
  const [isLoading, setIsLoading] = useLoading(false);
  addUserButton.addEventListener("click", async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const userId = e.target.dataset.id;
    const user = await retrieveUserProfile(parseInt(userId));
    addedToGroup.push(user);
    participants.push (user)
    group.add(participants);
    setIsLoading(false);
    renderAddedUserToInviteList(e, user, addedToGroupList);
    handleRemoveUserFromList(results, addedToGroupList);
  });
};


const renderAddedUserToInviteList = (e, user, addedToGroupList) => {
  const newParticipantRow = invitedUserToGroup(user);
  addedToGroupList.innerHTML += newParticipantRow;
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

const toggleAddPlusIcon = (e) => {
  e.preventDefault();
  const eventTarget = e.target;
  const uid = eventTarget.dataset.id;
  const allCheckButtonNodes = document.querySelectorAll(".fas.fa-check");
  const allCheckButtons = Array.from(allCheckButtonNodes);
  const buttonToToggle = allCheckButtons.filter((button) => parseInt(button.dataset.id) === parseInt(uid));
  const parentContainer = buttonToToggle[0].parentNode;
  parentContainer.innerHTML = "";
  const plusIcon = renderAddIcon(uid);
  parentContainer.innerHTML += plusIcon;
};


const handleClearAllEvent = (results, searchInput, addedToGroupList) => {
  const clearAllBtn = document.querySelector(".clear_all_button");
  clearAllBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addedToGroupList.innerHTML = "";
    results.innerHTML = "";
    participants = [];
    addedToGroup = [];
    group.clear();
    let search_term = '';
    setFormState(friendShips, searchInput, search_term, results, addedToGroupList)
  });
};


const handleRemoveUserFromList = (results, addedToGroupList) => {
  const removeInviteeNodes = document.querySelectorAll(".remove_participant");
  const removeInviteeButtons = [...removeInviteeNodes];

  const allParticipantsNodes = document.querySelectorAll(".participant_item_container");
  const allParticipantContainers = Array.from(allParticipantsNodes);

  removeInviteeButtons.forEach((removeButton) => {
    removeButton.addEventListener("click", (e) => {
      e.preventDefault();
      const key = e.target.dataset.id;
      const nodeKeys = allParticipantContainers.map((node) => node.dataset.key);
      const match = nodeKeys.includes(key);

      if (match != null) {
        const participantToRemove = participants.filter((userProfile) => userProfile.id === parseInt(key));
        const updatedParticipantsList = participants.filter((participant) => participant.id !== [...participantToRemove][0].id);
        participants = updatedParticipantsList;
        addedToGroup = updatedParticipantsList;
        group.clear()
        group.add(participants)
        toggleAddPlusIcon(e, participants);

        const allPlusIconsInResults = document.querySelectorAll(".fas.fa-plus");
        const addUserPlusIcons = [...allPlusIconsInResults];
        const containerToRemove = allParticipantContainers.filter((element) => element.dataset.key === key);
        containerToRemove[0].remove();

        const iconToAddEventListener = addUserPlusIcons.filter(icon => parseInt(icon.dataset.id) === participantToRemove[0].id);
        handleAddFriendToGroup(iconToAddEventListener[0], results, addedToGroupList);
      }
    });
  });
};


function searchFriendIdInList(array, valueToFind) {
  let matchingValues = []
  for (let item in array) {
    let index = item;
    let value = array[index];
    const values = Object.values(value);
    if (values.includes(valueToFind)) {
      matchingValues.push(value)
    }
  }
  if (Array.isArray(matchingValues) && matchingValues.length > 0) {
    return matchingValues.splice(0);
  } else {
    return false;
  }
}


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
        <i id="fa_plus_add_user" class="fas fa-plus" data-id="${friend.id}"></i>
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
    <div class="participant_item_container" data-key="${userProfile.id}">
      <div class="participant_item_wrapper_1">
        <li class="participant_item"> ${userProfile.user.first_name} ${userProfile.user.last_name}</li>
        <input type="hidden" id="participant-${userProfile.id}" name="participant-${userProfile.id}" value="${userProfile.id}"/>
      </div>
      <div class="participant_item_wrapper_2">
        <button class="remove_participant" data-id="${userProfile.id}"></button>
      </div>
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

function renderClearAllButton() {
  return `
      <div class="clear_all_button">Clear All</div>
  `;
}


initFriendsSearchAndCreateGroupForm();
