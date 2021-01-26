import { useQuantumFriends } from "./hooks.js";
import { getAllUsersFriends } from "./services.js";

const initUserFriends = async () => {
  const [friendships, setFriendships] = useQuantumFriends();
  const search_input = document.getElementById("friends_search");

  const allFriendships = await getAllUsersFriends();
  setFriendships(allFriendships);

  search_input.addEventListener("input", (e) => {
    const search_term = e.target.value;
    filterSearchQuery(friendships(), search_term);
  });
};

initUserFriends();

function filterSearchQuery(friendships, search_term) {
  const results = document.getElementById("results");
  results.innerHTML = "";

  friendships
    .filter((friend) => friend.user.first_name.toLowerCase().includes(search_term.toLowerCase()))
    .forEach((friend) => {
      let row;
      friend.image ? (row = renderFriendRowWithImage(friend)) : (row = renderFriendRowNoImage(friend));
      results.innerHTML += row;
    });
}

function renderFriendRowWithImage(friend) {
  return `
    <div class="friend_card">
        <div class="friend_profile_pic">
            <img class="friend_card_img" src="${friend.image.image}" />
        </div>
        <div class="friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
        <i id="user-check" class="fas fa-user-check"></i>
        <i id="fa-trash"class="far fa-trash-alt"></i>
    </div>
    `;
}

function renderFriendRowNoImage(friend) {
  const default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png";
  return `
      <div class="friend_card">
          <div class="friend_profile_pic">
              <img class="friend_card_img" src="${default_profile_pic}" />
          </div>
          <div class="friend_name">${friend.user.first_name} ${friend.user.last_name}</div>
          <i id="user-check" class="fas fa-user-check"></i>
          <i id="fa-trash"class="far fa-trash-alt"></i>
      </div>
      `;
}
