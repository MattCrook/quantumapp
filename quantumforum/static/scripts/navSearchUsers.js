import { useQuantumFriends, useUserList, useAuthUser } from "./hooks.js";
import { getAllUsersFriends, getUserList, getUser, sendFriendRequest} from "./services.js";

const [friends, setFriends] = useQuantumFriends();
const [users, setUsers] = useUserList();
const [currentAuthUser, setCurrentAuthUser] = useAuthUser();
let userSearchResultRows = [];

const handleUserSearchInput = (userList, friendList) => {
  const search_input = document.getElementById("user_search");
  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    renderSearchResults(userList, friendList, search_term);
  });
};

// initial load of the dropdown. Shows paginated results, then user can type to filter/ search.
const loadUsersAndFriends = async () => {
  try {
    const allFriendships = await getAllUsersFriends();
    setFriends(allFriendships);
    const allUsers = await getUserList();
    const currentUser = await getUser();

    setCurrentAuthUser([currentUser]);
    const authUser = currentAuthUser();
    const allUsersExcludingCurrentUser = allUsers.filter((profile) => profile.id !== authUser[0].user_profile.id);
    setUsers(allUsersExcludingCurrentUser);

    initNavSearchInput(users(), friends());
    handleUserSearchInput(users(), friends());
  } catch (error) {
    console.log(error);
  }
};

function initNavSearchInput(userList, friendsList) {
  const searchResults = document.getElementById("search_quantum_results");
  searchResults.innerHTML = "";
  userList.forEach((profile) => {
    let row;
    const isFriend = filterUserFriends(profile.id, friendsList);
    profile.image ? (row = renderRowWithImage(isFriend, profile)) : (row = renderRowNoImage(isFriend, profile));
    userSearchResultRows.push(row);
    searchResults.innerHTML += row;
  });
}

// Finding the user ID of the current friend in the loop, and return where the Ids match.
// To render either check or add friend icon.
// Want to return is the current user in loop is a friend or not.
function filterUserFriends(profileId, friendsList) {
  const userFriendProfileIds = friendsList.map((friend) => {
    return friend.id;
  });
  return userFriendProfileIds.includes(profileId);
}

function renderRowNoImage(isFriend, userProfile) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  const endRowIcon = renderWhichIcon(isFriend, userProfile.id);
  return `
    <div class="search_result_wrapper">
        <div class="search_result_container_1">
            <img class="search_result_image" src="${default_profile_pic}"/>
            <div class="search_result_name">${userProfile.user.first_name}</div>
            <div class="search_result_name">${userProfile.user.last_name}</div>
        </div>
    <div class="search_result_container_2">
        ${endRowIcon}
    </div>
    </div>
    `;
}

function renderRowWithImage(isFriend, userProfile) {
  const endRowIcon = renderWhichIcon(isFriend, userProfile.id);
  return `
    <div class="search_result_wrapper">
        <div class="search_result_container_1">
            <img class="search_result_image" src="${userProfile.image.image}"/>
            <div class="search_result_name">${userProfile.user.first_name}</div>
            <div class="search_result_name">${userProfile.user.last_name}</div>
        </div>
    <div class="search_result_container_2">
        ${endRowIcon}
    </div>
    </div>
    `;
}

function renderPendingApproval(userProfile_id) {
  return `
    <div class="search_result_container_2">
      <div class="pending_approval_button"><i class="fas fa-user-check" data-id="${userProfile_id}"></i></div>
    </div>
  `;
}

// After determining if user is a friend or not, this function then Determines which icon to render, the check or the friend icon.
function renderWhichIcon(isFriend, userProfile_id) {
  let icon;
  !isFriend ? (icon = renderAddFriendIcon(userProfile_id)) : (icon = renderCheckIcon(userProfile_id));
  return icon;
}

function renderAddFriendIcon(userProfile_id) {
  return `
      <div class="send_friend_request_btn"><i class="fas fa-user-plus" data-id="${userProfile_id}"></i></div>
      `;
}

function renderCheckIcon(userProfile_id) {
  return `
      <i id="fa_check_friend_request" class="fas fa-check" data-id="${userProfile_id}"></i>
      `;
}

function renderSearchResults(userList, friendsList, searchQuery) {
  const searchResults = document.getElementById("search_quantum_results");
  searchResults.innerHTML = "";
  userList
    .filter(
      (userProfile) =>
        userProfile.user.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        userProfile.user.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        userProfile.user.username.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .forEach((userProfile) => {
      let row;
      const isFriend = filterUserFriends(userProfile.id, friendsList);
      userProfile.image
        ? (row = renderRowWithImage(userProfile, isFriend))
        : (row = renderRowNoImage(userProfile, isFriend));
      searchResults.innerHTML += row;
    });
}

const toggleOverlay = () => {
  const bodyTag = document.getElementsByTagName("body")[0];
  const closeOverlay = document.querySelector(".overlay_close");
  const nav = document.querySelector(".nav");
  const currentGroupChats = document.querySelector(".current_group_chats_container");

  bodyTag.classList.toggle("overlay");
  if (closeOverlay.style.display === "none") {
    closeOverlay.style.display = "block";
    nav.style.boxShadow = "none";
    currentGroupChats.style.boxShadow = "none";
  } else if (closeOverlay.style.display === "block") {
    closeOverlay.style.display = "none";
    nav.style.boxShadow = "0px 6px 4px 0px rgb(190 190 190)";
    currentGroupChats.style.boxShadow = "2px 6px 4px 0px rgb(190 190 190)";
  }
};

// Handler for search bar in nav.
const handleClickInInput = () => {
  const searchQuantumInput = document.querySelector(".search_quantum_input");
  const searchQuantumResults = document.getElementById("search_quantum_results");
  const toggleNone = () => (searchQuantumResults.style.display = "none");
  const toggleBlock = () => (searchQuantumResults.style.display = "block");

  if (searchQuantumInput != null) {
    searchQuantumInput.addEventListener("click", () => {
      const display = searchQuantumResults.style.display;
      display === "none" && toggleBlock();
      display === "block" && toggleNone();
      toggleOverlay();
      handleSendFriendRequest();
    });
  }
};


const handleSendFriendRequest = () => {
  const addFriendButtonNodes = document.querySelectorAll(".send_friend_request_btn");
  const addFriendButtons = Array.from(addFriendButtonNodes);

  addFriendButtons.forEach(addButton => {
    addButton.firstChild.addEventListener("click", async (e) => {
      e.preventDefault();
      const userProfileId = parseInt(e.target.dataset.id);
      const currentUser = await getUser();

      const friendRequestPayload = {
        receiver: userProfileId,
        lastUpdatedBy: currentUser.id,
        statusCode: 0,
      };

      const submitFriendRequest = await sendFriendRequest(friendRequestPayload);
      console.log({submitFriendRequest});

      const buttonContainer = e.target.parentNode;
      buttonContainer.innerHTML = '';
      const checkIcon = renderPendingApproval(userProfileId);
      buttonContainer.innerHTML += checkIcon;
    })
  })
};




const init = () => {
  loadUsersAndFriends();
  handleClickInInput();
};

init();
