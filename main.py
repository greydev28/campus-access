from storage import (
    create_request,
    get_request,
    list_requests,
    save_requests,
    load_requests,
)

from workflow import approve_request, issue_card, return_card


def run_menu():
    while True:
        print("\n=== Campus Access-Card Manager ===")
        print("1. Create request")
        print("2. View request")
        print("3. Approve request")
        print("4. Issue card")
        print("5. Return card")
        print("6. List all requests")
        print("7. Save requests")
        print("8. Load requests")
        print("9. Quit")

        choice = input("Choose an option: ").strip()

        # Create a new request
        if choice == "1":
            fellow_id = input("Fellow ID (e.g., F001): ").strip()
            card_type = input(
                "Card type (visitor, student, staff): "
            ).strip()

            try:
                request = create_request(fellow_id, card_type)
                print("Request created successfully!")
                print(request)
            except (ValueError, KeyError, TypeError, RuntimeError) as error:
                print("Error:", error)

        # View one request
        elif choice == "2":
            request_id = input("Request ID (e.g., A001): ").strip()

            try:
                request = get_request(request_id)
                print(request)
            except (ValueError, KeyError) as error:
                print("Error:", error)

        # Approve a request
        elif choice == "3":
            request_id = input("Request ID: ").strip()
            approved_by = input("Staff name: ").strip()

            try:
                request = approve_request(request_id, approved_by)
                print("Request approved:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        # Issue a card
        elif choice == "4":
            request_id = input("Request ID: ").strip()

            try:
                request = issue_card(request_id)
                print("Card issued:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        # Return a card
        elif choice == "5":
            request_id = input("Request ID: ").strip()

            try:
                request = return_card(request_id)
                print("Card returned:", request["id"])
            except (ValueError, KeyError, TypeError) as error:
                print("Error:", error)

        # List all requests
        elif choice == "6":
            all_requests = list_requests()

            if not all_requests:
                print("No requests found.")
            else:
                for request in all_requests:
                    print(request)

        # Save requests to JSON
        elif choice == "7":
            try:
                save_requests()
                print("Requests saved successfully.")
            except (OSError, ValueError, TypeError) as error:
                print("Error saving requests:", error)

        # Load requests from JSON
        elif choice == "8":
            try:
                load_requests()
                print("Requests loaded successfully.")
            except (OSError, ValueError, KeyError, TypeError) as error:
                print("Error loading requests:", error)

        # Quit the application
        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 9.")


if __name__ == "__main__":
    run_menu()