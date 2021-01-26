const useQuantumFriends = () => {
    let friends = [];
      return [
          () => friends.slice(),
          (newFriends) => (friends = newFriends.splice(0))
      ];
  };


export { useQuantumFriends };
