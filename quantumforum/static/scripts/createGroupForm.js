import {
  useQuantumFriends,
  useLoading,
  useGroupChatParticipants,
  useUserList,
  useGroup,
  useAddedToGroup,
} from "./hooks.js";
import { getAllUsersFriends, retrieveUserProfile } from "./services.js";

const [participants, setParticipants] = useGroupChatParticipants();
// const [addedToGroup, addedToGroup] = useAddedToGroup();
const [friendships, setFriendships] = useQuantumFriends();
const [group, setGroup] = useGroup([...participants()]);

let addedToGroup = [];
let addedParticipantsList = [];

const initFriendsSearchAndCreateGroupForm = async () => {
  const search_input = document.getElementById("friends_search");
  const results = document.getElementById("results");
  const allFriendships = await getAllUsersFriends();
  setFriendships(allFriendships);
  setFormState(friendships(), search_input, results);
};

const setFormState = (friendShips, search_input, results) => {
  initialRenderFriendShipData(friendShips, results);
  handleSearchInput([...friendships()], search_input);
  initAddGroupForm();
};

const initAddGroupForm = () => {
  const addUserNodes = document.querySelectorAll(".fas.fa-plus");
  const addUserButtons = [...addUserNodes];
  addUserButtons.forEach((button) => {
    handleAddFriendToGroup(button);
  });
  handleClearAllEvent();
};

const initialRenderFriendShipData = (friendshipList, results) => {
  friendshipList.forEach((friend) => {
    let row;
    friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
    results.innerHTML += row;
  });
};

const handleSearchInput = (friendShips, search_input) => {
  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    filterSearchQuery(friendShips, search_term);
    initAddGroupForm();
  });
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
      const isFriendImage = friend && friend.image && friend.image != null;
      // const participantIds = [...participants()].map(user => user.id)
      const addedFriendToGroup = searchFriendIdInList([...participants()], friend.id);
      const hasGroupParticipants = true ? addedFriendToGroup != null : false;
      const isAddedToGroup = hasGroupParticipants ? addedFriendToGroup.id === friend.id : false;

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

const handleAddFriendToGroup = (addUserButton) => {
  const [isLoading, setIsLoading] = useLoading(false);
  const inviteList = document.querySelector(".invitee_list");

  addUserButton.addEventListener("click", async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const userId = e.target.dataset.id;
    const user = await retrieveUserProfile(parseInt(userId));
    addedParticipantsList.push(user);

    // setAddedToGroup([user]);
    addedToGroup.push([user]);
    setParticipants([...addedParticipantsList]);

    const newParticipantRow = invitedUserToGroup(user);
    inviteList.innerHTML += newParticipantRow;
    setIsLoading(false);
    // alert(`${user.user.first_name} ${user.user.last_name} added to group chat.`);

    toggleAddCheckIcon(e, participants());
    handleRemoveUserFromList();
    setGroup(participants());
  });
};

const toggleAddCheckIcon = (e, participantList) => {
  e.preventDefault();
  const eventTarget = e.target;
  const uid = eventTarget.dataset.id;
  const parentContainer = eventTarget.parentNode;
  parentContainer.innerHTML = "";
  const checkIcon = renderCheckIcon(uid);
  parentContainer.innerHTML += checkIcon;
};

const toggleAddPlusIcon = (e, friendsList) => {
  e.preventDefault();
  const eventTarget = e.target;
  const uid = eventTarget.dataset.id;
  // const parentContainer = eventTarget.parentNode;
  // parentContainer.innerHTML = "";
  // const checkIcon = renderAddIcon(uid);
  // parentContainer.innerHTML += checkIcon;

  const allCheckButtonNodes = document.querySelectorAll(".fas.fa-check");
  const allCheckButtons = Array.from(allCheckButtonNodes);
  const buttonToToggle = allCheckButtons.filter((button) => parseInt(button.dataset.id) === parseInt(uid));
  const parentContainer = buttonToToggle[0].parentNode;
  parentContainer.innerHTML = "";
  const plusIcon = renderAddIcon(uid);
  parentContainer.innerHTML += plusIcon;
};

const handleClearAllEvent = () => {
  const clearAllBtn = document.querySelector(".clear_all_button");
  const inviteList = document.querySelector(".invitee_list");
  const results = document.getElementById("results");
  clearAllBtn.addEventListener("click", (e) => {
    e.preventDefault();
    inviteList.innerHTML = "";
    results.innerHTML = "";
    initFriendsSearchAndCreateGroupForm();
  });
};

const handleRemoveUserFromList = () => {
  const removeInviteeNodes = document.querySelectorAll(".remove_participant");
  const removeInviteeButtons = [...removeInviteeNodes];

  const allParticipantsNodes = document.querySelectorAll(".participant_item_container");
  const allParticipantContainers = Array.from(allParticipantsNodes);

  removeInviteeButtons.forEach((removeButton) => {
    removeButton.addEventListener("click", (e) => {
      e.preventDefault();
      const key = e.target.dataset.id;
      // const parentNode = e.target.parentNode;
      const nodeKeys = allParticipantContainers.map((node) => node.dataset.key);
      const match = nodeKeys.includes(key);

      if (match != null) {
        console.log("HERE3");
        const containerToRemove = allParticipantContainers.filter((element) => element.dataset.key === key);
        containerToRemove[0].remove();
        const participantToRemove = [...participants()].filter((userProfile) => userProfile.id === parseInt(key));
        const updatedParticipantsList = [...addedParticipantsList].filter(
          (participant) => participant.id !== [...participantToRemove][0].id
        );
        setParticipants([...updatedParticipantsList]);
        toggleAddPlusIcon(e, [...updatedParticipantsList]);
        setGroup([...updatedParticipantsList]);
      }
    });
  });
};

function searchFriendIdInList(array, valueToFind) {
  for (let item in array) {
    let index = item;
    let value = array[index];
    const values = Object.values(value);
    console.log(valueToFind);
    if (values.includes(valueToFind)) {
      return value;
    } else {
      return false;
    }
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

/*
  const addedFriendToGroup = searchFriendIdInList(participantList, parseInt(uid));
  console.log('addedFriendToGroup', addedFriendToGroup)
  const hasGroupParticipants = true ? addedFriendToGroup != null : false;
  console.log('hasGroupParticipants', hasGroupParticipants)

  const isAddedToGroup = hasGroupParticipants ? addedFriendToGroup.id === parseInt(uid) : false;
  console.log('isAddedToGroup', isAddedToGroup)
  // isAddedToGroup ? renderCheckIcon(uid) : renderAddIcon(uid);



  if (isAddedToGroup) {
    console.log({eventTarget})
    const parentContainer = eventTarget.parentNode;
    parentContainer.innerHTML = "";
    const checkIcon = renderCheckIcon(uid);
    parentContainer.innerHTML += checkIcon;
  } else {
    // const addIcon = renderAddIcon(uid);
    const checkIconNodes = document.querySelectorAll(".fas.fa-check");
    const checkIcons = Array.from(checkIconNodes);
    // const iconToChange = checkIcons.filter((icon) => parseInt(icon.dataset.id) === parseInt(uid));
    // console.log({iconToChange})
    // const isIcon = iconToChange != null;
    // const parentContainer = iconToChange.parentNode;
    const parentContainer = eventTarget.parentNode;
    console.log(parentContainer)

    parentContainer.innerHTML = "";
    const addIcon = renderCheckIcon(uid);
    parentContainer.innerHTML += addIcon

    // const tempContainer = document.createElement("div");
    // tempContainer.innerHTML = addIcon;
    // const addIconElement = tempContainer.firstChild.nextSibling;
    // parentContainer.appendChild(addIconElement);
  }
  */

// if (isCheck) {
//   console.log("here")
//   const parentContainer = eventTarget.parentNode;
//   parentContainer.innerHTML = "";
//   const checkIcon = renderCheckIcon(uid);
//   parentContainer.innerHTML += checkIcon;
// } else {
//   console.log("here2")
//   const addIcon = renderAddIcon(uid);
//   const checkIconNodes = document.querySelectorAll(".fas.fa-check");
//   const checkIcons = Array.from(checkIconNodes);
//   const iconToChange = checkIcons.filter((icon) => icon.dataset.id === uid);
//   console.log(iconToChange)
//   const isIcon = iconToChange != null;

//   if (isIcon) {
//     console.log("here4")
//     console.log(participants());
//     console.log({ addedParticipantsList })
//     setParticipants([...participants()])
//     setGroup([...participants()])
//     console.log('h4part', participants());

// const parentContainer = iconToChange[0].parentNode;
// parentContainer.innerHTML = "";
// const tempContainer = document.createElement("div");
// tempContainer.innerHTML = addIcon;
// const addIconElement = tempContainer.firstChild.nextSibling;
// parentContainer.appendChild(addIconElement);
// handleAddFriendToGroup(addIconElement);
// }
// }
// };
