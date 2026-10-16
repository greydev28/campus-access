# campus-access
Campus Access-Card Request Manager
A command-line application built with Python to manage campus access-card requests. It allows users to create and view requests, approve requests, issue cards, record returned cards, and save or load request data using JSON.
Features
- Create requests for visitor, student, and staff access cards.
- Validate input such as fellow IDs, request IDs, and card types.
- View a request using its unique request ID.
- Approve requests and record the staff member who approved them.
- Issue cards only after a request has been approved.
- Record returned cards only after they have been issued.
- List all requests stored by the application.
- Save and load data using a JSON file.
- Handle invalid input with readable error messages.
Workflow
Each request follows this sequence:
requested -> approved -> issued -> returned
The application enforces these rules:
- A request must be in the requested state before it can be approved.
- A request must be approved and have a recorded approver before a card can be issued.
- A card must be issued before it can be marked as returned.
- A returned request cannot move to another state.
Requirements
- Python 3.10 or later is recommended.
- No third-party packages are required; the project uses Python's standard library.
Project Structure
Campus-Access-Card-Manager/
├── main.py
├── storage.py
├── workflow.py
├── test_workflow.py
├── README.md
└── data/
    └── requests.json
The data/ directory and JSON file may be created when data is saved. 

Input Formats
- Fellow ID: F001 (the letter F followed by three digits)
- Request ID: A001 (the letter A followed by three digits)
- Card type: visitor, student, or staff
Example request:
{
    "id": "A001",
    "fellow_id": "F001",
    "card_type": "student",
    "status": "requested",
    "approved_by": ""
}
Saving and Loading Data
The application stores request data in JSON format so it can be reused between runs.
- Choose Save requests from the menu to save the current data.
- Choose Load requests to load data from the configured JSON file.
Make sure the save and load functions use the same file path. The current code should consistently use one path, for example data/requests.json.
Running Tests
Error Handling and Validation
The application validates user input and request transitions. Invalid IDs, unsupported card types, unknown requests, and invalid workflow transitions should produce readable error messages rather than silently changing request data.
Contributing
Contributions are welcome.
1. Fork the repository.
2. Create a branch for your change.
3. Make your changes and add or update tests.
4. Run the test suite.
5. Open a pull request describing your changes.
Future Improvements
Possible improvements include:
- Add more automated tests for storage and workflow validation.
- Improve the display of request details.
- Add configurable storage locations.
- Add stronger safeguards against data loss when saving fails.