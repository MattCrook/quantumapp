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

const useLoading = (initialState) => {
    let isLoading = initialState;
        return [
            () => isLoading,
            (newState) => (isLoading = newState)
        ];
    };


const useGroupChatParticipants = () => {
    let participants = [];
        return [
            () => participants.slice(),
            (newInvitee) => (participants = newInvitee.splice(0))
        ];
    };

export { useQuantumFriends, useUserList, useLoading, useGroupChatParticipants };
