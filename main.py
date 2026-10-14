from workflow import approve_request, issue_card, return_card


def run_menu():
    while True:
        print("\n=== Campus Access-Card Manager ===")
        print("1. Approve request")
        print("2. Issue card")
        print("3. Return card")
        print("4. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            request_id = input("Request ID: ").strip()
            approved_by = input("Staff ID: ").strip()

            try:
                request = approve_request(request_id, approved_by)
                print("Request approved:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        elif choice == "2":
            request_id = input("Request ID: ").strip()

            try:
                request = issue_card(request_id)
                print("Card issued:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        elif choice == "3":
            request_id = input("Request ID: ").strip()

            try:
                request = return_card(request_id)
                print("Card returned:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_menu()