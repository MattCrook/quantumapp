// import { useQuantumFriends, useUserList, useAuthUser } from "./hooks.js";
import {
  getAllUsersFriends,
  getUserList,
  getUser,
  sendFriendRequest,
  getFriendships,
  getFriendRequests,
  postActivityLogError,
} from "./services.js";

// const [friends, setFriends] = useQuantumFriends();
// const [users, setUsers] = useUserList();
// const [currentAuthUser, setCurrentAuthUser] = useAuthUser();
let userSearchResultRows = [];



// Initial load of the dropdown. Shows paginated results, then user can type to filter/ search.
// Gets current logged in user.
// Gets all friendships, and all friends, then maps the friendships join to the users friend requests on sender and receiver id to get
// all friend requests tied to the current user.
// Filtering all friendships on sender and receiver id to later user the status code on the friend request object.
const loadUsersAndFriends = async () => {
  try {
    const data = await Promise.all([getUser(), getUserList(), getAllUsersFriends(), getFriendships(), getFriendRequests()]);
    const currentUser = data[0];
    const allUsers = data[1];
    const allFriendshipProfiles = data[2];
    const allSenderAndReceiver = data[3];
    const allFriendRequests = data[4];

    const friendRequestsUserHasSent = allSenderAndReceiver.filter((request) => request.requester.id === currentUser.id);
    const friendRequestsUserHasReceived = allSenderAndReceiver.filter(
      (request) => request.addressee.id === currentUser.id
    );
    const allSentAndReceivedFriendships = [...friendRequestsUserHasSent, ...friendRequestsUserHasReceived];
    const senderAndReceiverIds = allSentAndReceivedFriendships.map((friendship) => friendship.id);
    const allUsersFriendRequests = allFriendRequests.filter(
      (friendRequest) => !senderAndReceiverIds.includes(friendRequest.sender_and_receiver_id)
    );

    const allUsersExcludingCurrentUser = allUsers.filter((profile) => profile.id !== currentUser.user_profile.id);
    // setUsers(allUsersExcludingCurrentUser);
    // setFriends(allUsersFriendRequests);
    console.log("Friends", allUsersFriendRequests);

    initNavSearchInput(allUsersExcludingCurrentUser, allUsersFriendRequests, allFriendshipProfiles);
    handleUserSearchInput(allUsersExcludingCurrentUser, allUsersFriendRequests);
  } catch (error) {
    console.log(error);
    await postActivityLogError(error, "QuantumForum", "navSearchUsers.js", "loadUsersAndFriends", currentUser.id);
  }
};


function handleUserSearchInput(userList, friendList) {
  const search_input = document.getElementById("user_search");
  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    renderSearchResults(userList, friendList, search_term);
  });
};

function initNavSearchInput(userList, friendRequestList, allFriendshipProfiles) {
  const searchResults = document.getElementById("search_quantum_results");
  searchResults.innerHTML = "";
  userList.forEach((userProfile) => {
    let row;
    const friendRequestStatusData = filterUserFriends(userProfile, friendRequestList, allFriendshipProfiles);
    userProfile.image
      ? (row = renderRowWithImage(friendRequestStatusData, userProfile))
      : (row = renderRowNoImage(friendRequestStatusData, userProfile));
    userSearchResultRows.push(row);
    searchResults.innerHTML += row;
  });
}

// Finding the user ID of the current friend in the loop, and return where the Ids match.
// To render either check or add friend icon.
// Want to return is the current user in loop is a friend or not.
// userProfile.id is current userProfile id of user's friend in for each loop  in initNavSearchInput().
// friendRequestList is filtered list of friend request objects that hold the friendships join to the user's friends.
function filterUserFriends(userProfile, friendRequestList, allFriendshipProfiles) {
  const authUserId = userProfile.user.id;
  const friendships = friendRequestList.map((request) => {
    let sent = [];
    let received = [];
    if (request.sender_and_receiver.requester.id === authUserId) {
      sent.push(request);
    } else if (request.sender_and_receiver.addressee.id === authUserId) {
      received.push(request);
    }
    const data = {
      sent: sent,
      received: received,
      all: [...sent, ...received],
    };
    return data;
  });
  const friendUserProfileIds = allFriendshipProfiles.map((userProfile) => {
    return userProfile.id;
  });
  const friendAuthUser = userProfile.user;
  const friendRequestForCurrentFriend = friendRequestList.filter(
    (friendRequest) =>
      friendRequest.sender_and_receiver.addressee.id === friendAuthUser.id ||
      friendRequest.sender_and_receiver.requester.id === friendAuthUser.id
  );

  const friendRequestStatusData = {
    isFriend: friendUserProfileIds.includes(userProfile.id),
    friendships: friendships.filter((friendship) => friendship.all.length > 0),
    friendRequest: friendRequestForCurrentFriend,
    friendUserProfile: userProfile,
    friendAuthUser: friendAuthUser,
  };
  return friendRequestStatusData;
}

function renderRowNoImage(friendRequestStatusData, userProfile) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  const endRowIcon = renderWhichIcon(friendRequestStatusData, userProfile.id);
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

function renderRowWithImage(friendRequestStatusData, userProfile) {
  const endRowIcon = renderWhichIcon(friendRequestStatusData, userProfile.id);
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

// After determining if user is a friend or not, this function then Determines which icon to render,
// for status of friend request: pending, approved, denied, or not friend.
// Also handles whether to show the alert next to "Your Quantum Friends" or not,
// based on the status code of friend requests.
function renderWhichIcon(friendRequestStatusData, userProfileId) {
  let icon;
  const { isFriend, friendRequest } = friendRequestStatusData;
  console.log(friendRequest);
  let statusCode;
  friendRequest && Array.isArray(friendRequest) && friendRequest.length > 0 && friendRequest[0].status_code
    ? (statusCode = friendRequest[0].status_code)
    : (statusCode = false);

  console.log({ statusCode });
  isFriend && statusCode && statusCode.id === 1 && (icon = renderSentRequestPendingApproval(userProfileId));
  isFriend && statusCode && statusCode.id === 2 && (icon = renderCheckIcon(userProfileId));
  isFriend && statusCode && statusCode.id === 3 && (icon = renderBlockedIcon(userProfileId));
  isFriend && statusCode && statusCode.id === 4 && (icon = renderDeniedIcon(userProfileId));
  !isFriend && !statusCode && (icon = renderAddFriendIcon(userProfileId));

  handleAlert(statusCode);
  return icon;
}

function renderAddFriendIcon(userProfileId) {
  return `
      <div class="send_friend_request_btn"><i id="fa_user_plus" class="fas fa-user-plus" data-id="${userProfileId}"></i></div>
      `;
}

function renderCheckIcon(userProfileId) {
  return `
      <i id="fa_check_friend_request" class="fas fa-check" data-id="${userProfileId}"></i>
      `;
}

function renderSentRequestPendingApproval(userProfileId) {
  return `
      <i id="fa_pending_friend_request" class="fas fa-user-check" data-id="${userProfileId}"></i>
      `;
}

function renderPendingApproval(userProfileId) {
  return `
    <div class="search_result_container_2">
      <div class="pending_approval_button"><i class="fas fa-user-check" data-id="${userProfileId}"></i></div>
    </div>
  `;
}

function renderDeniedIcon(userProfileId) {
  return `
      <i id="fa_denied_friend_request" class="fas fa-user-alt-slash" data-id="${userProfileId}"></i>
    `;
}

function renderBlockedIcon(userProfileId) {
  return `
    <i id="fa_blocked_friend_request" class="fas fa-ban" data-id="${userProfileId}"></i>
  `;
}

function renderSearchResults(userList, friendRequestList, searchQuery) {
  const searchResults = document.getElementById("search_quantum_results");
  searchResults.innerHTML = "";
  userList
    .filter(
      (userProfile) =>
        userProfile.user.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        userProfile.user.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        userProfile.user.username.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .forEach(async (userProfile) => {
      let row;
      const friendRequestStatusData = filterUserFriends(userProfile.id, friendRequestList);
      console.log("friendRequest2", friendRequestStatusData);
      userProfile.image
        ? (row = renderRowWithImage(friendRequestStatusData, userProfile))
        : (row = renderRowNoImage(friendRequestStatusData, userProfile));
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
  // const searchQuantumResults = document.getElementById("search_quantum_results");
  const searchResultsMasterContainer = document.getElementById("search_quantum_results_master_container");

  const toggleNone = () => (searchResultsMasterContainer.style.display = "none");
  const toggleBlock = () => (searchResultsMasterContainer.style.display = "block");

  if (searchQuantumInput != null) {
    searchQuantumInput.addEventListener("click", () => {
      const display = searchResultsMasterContainer.style.display;
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

  addFriendButtons.forEach((addButton) => {
    addButton.firstChild.addEventListener("click", async (e) => {
      e.preventDefault();
      const userProfileId = parseInt(e.target.dataset.id);
      const currentUser = await getUser();

      const friendRequestPayload = {
        receiver: userProfileId,
        lastUpdatedBy: currentUser.id,
        statusCode: 0,
      };
      try {
        const submitFriendRequest = await sendFriendRequest(friendRequestPayload);
        console.log({ submitFriendRequest });
      } catch (error) {
        console.log(error)
      }
      const buttonContainer = e.target.parentNode;
      buttonContainer.innerHTML = "";
      const checkIcon = renderPendingApproval(userProfileId);
      buttonContainer.innerHTML += checkIcon;
    });
  });
};

function showAlert() {
  const alert = document.getElementById("quantum_friend_alert");
  alert.style.display = "block";
}

function hideAlert() {
  const alert = document.getElementById("quantum_friend_alert");
  alert.style.display = "none";
}

function handleAlert(statusCode) {
  if (statusCode.id === 1) {
    showAlert();
  }
}

const init = () => {
  loadUsersAndFriends();
  handleClickInInput();
};

init();
