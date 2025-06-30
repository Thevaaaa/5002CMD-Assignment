# person class: represents a user profile on the social media app
class Person:
    def __init__(self, username, name, gender, biography="", privacy="public"):
        self.username = username
        self.name = name
        self.gender = gender
        self.biography = biography
        self.privacy = privacy.lower()

    def displayProfile(self, force_view=False):
        """
        Displays the profile information.
        If force_view is True, privacy settings are ignored.
        """
        if self.privacy == "private" and not force_view:
            return f"Username: {self.username}\nName: {self.name}\nProfile is private."
        return (f"Username: {self.username}\nName: {self.name}\nGender: {self.gender}\n"
                f"Biography: {self.biography}\nPrivacy: {self.privacy.capitalize()}")


# socialgraph class: handles the social network logic using a directed graph
class SocialGraph:
    def __init__(self):
        self.users = {}         # stores person objects, keyed by username
        self.following = {}     # stores who each user is following (adjacency list)

    def addUser(self, person):
        """Adds a new user to the network if max limit not reached."""
        if person.username not in self.users and len(self.users) < 10:
            self.users[person.username] = person
            self.following[person.username] = []
            print(f"User '{person.username}' added successfully.")
        else:
            print("User already exists or maximum limit (10 users) reached.")

    def follow(self, follower, followee):
        """Allows one user to follow another."""
        if follower in self.users and followee in self.users:
            if followee not in self.following[follower]:
                self.following[follower].append(followee)
                print(f"{follower} now follows {followee}.")
            else:
                print(f"{follower} already follows {followee}.")
        else:
            print("One or both users do not exist.")

    def unfollow(self, follower, followee):
        """Allows one user to unfollow another."""
        if follower in self.users and followee in self.following[follower]:
            self.following[follower].remove(followee)
            print(f"{follower} has unfollowed {followee}.")
        else:
            print("Unfollow action failed.")

    def listUsers(self):
        """Displays all users in the network."""
        print("\nAll Users:")
        for user in self.users.values():
            print(f"- {user.name} ({user.username})")

    def viewProfile(self, username):
        """Displays the profile of a user (ignores privacy settings)."""
        if username in self.users:
            print("\nProfile Details:")
            print(self.users[username].displayProfile(force_view=True))
        else:
            print("User not found.")

    def listFollowing(self, username):
        """Lists all accounts a user is following (outgoing edges)."""
        if username in self.following:
            print(f"\n{username} is following:")
            if not self.following[username]:
                print("No accounts followed.")
            for u in self.following[username]:
                print(f"- {self.users[u].name} ({u})")
        else:
            print("User not found.")

    def listFollowers(self, username):
        """Lists all accounts that follow the user (incoming edges)."""
        if username not in self.users:
            print("User not found.")
            return
        print(f"\nFollowers of {username}:")
        found = False
        for user, following_list in self.following.items():
            if username in following_list:
                print(f"- {self.users[user].name} ({user})")
                found = True
        if not found:
            print("No followers found.")


# --- preloaded users and connections ---
graph = SocialGraph()
graph.addUser(Person("theva", "thevadarshini siva kumar", "female", "traveler and soft girl", "public"))
graph.addUser(Person("nishan", "nishanath niruttha", "male", "working and adventurer", "private"))
graph.addUser(Person("athirah", "athirah dyana", "female", "books and foodie", "public"))
graph.addUser(Person("rat", "rathnezsh", "male", "game developer", "public"))
graph.addUser(Person("shaan", "thishaan", "male", "nature lover", "private"))

# sample follow relationships
graph.follow("theva", "nishan")
graph.follow("nishan", "theva")
graph.follow("rat", "shaan")
graph.follow("shaan", "rat")
graph.follow("athirah", "theva")


# --- menu-driven interface ---
def mainMenu():
    while True:
        print("\n--- Social Media App Menu ---")
        print("1. Display all users")
        print("2. View a user's profile (ignore privacy)")
        print("3. View accounts followed by a user")
        print("4. View followers of a user")
        print("5. Add a new user")
        print("6. Follow a user")
        print("7. Unfollow a user")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            graph.listUsers()

        elif choice == '2':
            username = input("Enter username: ")
            graph.viewProfile(username)

        elif choice == '3':
            username = input("Enter username: ")
            graph.listFollowing(username)

        elif choice == '4':
            username = input("Enter username: ")
            graph.listFollowers(username)

        elif choice == '5':
            if len(graph.users) >= 10:
                print("Cannot add more users. Limit reached.")
                continue
            uname = input("Enter new username: ")
            name = input("Enter full name: ")
            gender = input("Enter gender: ")
            bio = input("Enter biography: ")
            privacy = input("Enter privacy (public/private): ")
            graph.addUser(Person(uname, name, gender, bio, privacy))

        elif choice == '6':
            f1 = input("Enter your username: ")
            f2 = input("Enter username to follow: ")
            graph.follow(f1, f2)

        elif choice == '7':
            f1 = input("Enter your username: ")
            f2 = input("Enter username to unfollow: ")
            graph.unfollow(f1, f2)

        elif choice == '8':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


# start the program
if __name__ == "__main__":
    mainMenu()
