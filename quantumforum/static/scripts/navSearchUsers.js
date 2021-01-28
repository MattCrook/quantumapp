import { useQuantumFriends, useUserList } from "./hooks.js";
import { getAllUsersFriends, getUserList } from "./services.js";

const [friends, setFriends] = useQuantumFriends();
const [users, setUsers] = useUserList();
let userSearchResultRows = [];

// initial load of the dropdown. Shows paginated results, then user can type to filter/ search.
const loadUsersAndFriends = async () => {
  const allFriendships = await getAllUsersFriends();
  setFriends(allFriendships);
  const allUsers = await getUserList();
  setUsers(allUsers);
  initNavSearchInput(users(), friends());
  handleSearchInput(users(), friends());
};

function initNavSearchInput(userList, friendsList) {
  const searchResults = document.getElementById("search_quantum_results");
  searchResults.innerHTML = "";
  userList.forEach((profile) => {
    let row;
    const isFriend = filterUserFriends(profile.id, friendsList);
    profile.image ? (row = renderRowWithImage(profile, isFriend)) : (row = renderRowNoImage(profile, isFriend));
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

function renderRowNoImage(user_profile, isFriend) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  const endRowIcon = renderWhichIcon(isFriend);
  return `
    <div class="search_result_wrapper">
        <div class="search_result_container_1">
            <img class="search_result_image" src="${default_profile_pic}"/>
            <div class="search_result_name">${user_profile.user.first_name}</div>
            <div class="search_result_name">${user_profile.user.last_name}</div>
        </div>
    <div class="search_result_container_2">
        ${endRowIcon}
    </div>
    </div>
    `;
}

function renderRowWithImage(user_profile, isFriend) {
  const endRowIcon = renderWhichIcon(isFriend);
  return `
    <div class="search_result_wrapper">
        <div class="search_result_container_1">
            <img class="search_result_image" src="${user_profile.image.image}"/>
            <div class="search_result_name">${user_profile.user.first_name}</div>
            <div class="search_result_name">${user_profile.user.last_name}</div>
        </div>
    <div class="search_result_container_2">
        ${endRowIcon}
    </div>
    </div>
    `;
}

function renderWhichIcon(isFriend) {
  let icon;
  !isFriend ? (icon = renderAddFriendIcon()) : (icon = renderCheckIcon());
  return icon;
}

function renderAddFriendIcon() {
  return `
      <div class="send_friend_request_btn"><i class="fas fa-user-plus"></i></div>
      `;
}

function renderCheckIcon() {
  return `
      <i id="fa_check_friend_request" class="fas fa-check"></i>
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
    const bodyTag = document.getElementsByTagName("body")[0]
    const closeOverlay = document.querySelector(".overlay_close")
    bodyTag.classList.toggle("overlay");
    if (closeOverlay.style.display === "none") {
        closeOverlay.style.display = "block"
    } else if (closeOverlay.style.display === "block") {
        closeOverlay.style.display = "none";
    }
    // var tabIndex = document.createAttribute("tabindex");
    // tabIndex.value = '-1';
    // bodyTag.setAttributeNode(tabIndex);
}

const handleClickInInput = () => {
  const searchQuantumInput = document.querySelector(".search_quantum_input");
  const searchQuantumResults = document.getElementById("search_quantum_results");
  const toggleNone = () => (searchQuantumResults.style.display = "none");
  const toggleBlock = () => (searchQuantumResults.style.display = "block");

  searchQuantumInput.addEventListener("click", () => {
    const display = searchQuantumResults.style.display;
    display === "none" && toggleBlock();
    display === "block" && toggleNone();
    toggleOverlay();
  });
};

const handleSearchInput = (userList, friendList) => {
  const search_input = document.getElementById("user_search");
  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    renderSearchResults(userList, friendList, search_term);
  });
};

const init = () => {
  loadUsersAndFriends();
  handleClickInInput();
};

init();
