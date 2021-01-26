const useQuantumFriends = () => {
    let friends = [];
      return [
          () => friends.slice(),
          (newFriends) => (friends = newFriends.splice(0))
      ];
  };

const useUserList = () => {
let users = [];
    return [
        () => users.slice(),
        (newUsers) => (users = newUsers.splice(0))
    ];
};


export { useQuantumFriends, useUserList };
