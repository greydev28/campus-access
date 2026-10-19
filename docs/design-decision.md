# Design Decisions — Campus Access-Card Request Manager

## 1. Project Overview

The Campus Access-Card Request Manager is a Python command-line application
that manages requests for visitor, student, and staff access cards.

The application allows users to create, view, approve, issue, and return
access cards. It also supports listing requests and saving and loading
records using JSON.

The application must reject invalid operations and preserve the original
record when an operation fails.

## 2. Request Data Structure

Each request will be represented by a Python dictionary containing five
required fields:

- `id`: Unique request identifier, such as A001.
- `fellow_id`: Identifier of the person requesting the card.
- `card_type`: Type of card requested.
- `status`: Current state of the request.
- `approved_by`: Identifier of the staff member who approved the request.

Example:

    {
        "id": "A001",
        "fellow_id": "STU100",
        "card_type": "student",
        "status": "requested",
        "approved_by": ""
    }

Allowed card types are `visitor`, `student`, and `staff`.

Every new request must have the initial status `requested`.

A dictionary is appropriate because it stores related information as
key-value pairs, making individual fields easy to access and validate.

## 3. Request Creation and Return Values

The `create_request(fellow_id, card_type)` function will validate its
arguments before creating a request.

If the inputs are valid, it will generate a unique ID, create the
request, store it, and return the created request.

If the inputs are invalid, the function will raise `ValueError` and
will not create a record.

The exact return type and exception contract must be agreed upon by both
engineers before integration.

## 4. Input Validation and Error Handling

The application will validate inputs before modifying stored records.

Validation rules include:

- Fellow IDs must be nonempty strings.
- Card types must be `visitor`, `student`, or `staff`.
- Request IDs must follow the required A001, A002, A003 format.
- Request IDs must use ASCII digits from 0 to 9.
- Approver IDs must be nonempty strings.
- Unknown request IDs must be rejected.
- Unsupported state transitions must be rejected.

Invalid inputs and workflow operations should raise `ValueError`.

The command-line interface will catch expected errors and display
helpful messages so users can retry without restarting the application.

## 5. Request ID Generation

Request IDs will follow this sequence:

    A001
    A002
    A003

The storage component will be responsible for generating IDs.

The next ID must remain unique after the application restarts.

When loading saved requests, the application will validate existing IDs
and determine the next available ID from the stored records.

The implementation must also handle gaps in the sequence without
accidentally reusing an existing ID.

## 6. Workflow and State Transitions

The application will enforce the following state machine:

    requested -> approved -> issued -> returned

Rules:

- A requested card can be approved.
- An approved card can be issued only if `approved_by` is nonempty.
- An issued card can be returned.
- A returned card is final.
- Skipping a state is not allowed.
- An unknown request ID must be rejected.
- Failed operations must leave the request unchanged.

The workflow component will own approval, issuance, and return operations.

The storage component will own request storage and persistence.

Workflow functions must use the agreed storage interface instead of
independently creating or replacing stored records.

The application does not currently implement physical gate access or
identity verification against an external institutional database.

## 7. Storage and Persistence

Requests will be saved in JSON format using Python's standard `json`
module.

The application will support saving records to a file and loading them
when the application starts.

The JSON loader must validate the loaded data before accepting it.

It must reject:

- Corrupted or malformed JSON.
- Missing required fields.
- Unexpected fields.
- Duplicate request IDs.
- Invalid card types.
- Invalid statuses.
- Incorrect field types.
- Invalid request ID formats.
- Records that violate the request data requirements.

An empty file is not a valid JSON document and must not be treated as
an empty database.

A missing file may be handled separately from a malformed file.
The application must never silently replace invalid saved data with
empty records.

Failed loading must not destroy existing in-memory records.

## 8. Handling Failed Operations

The application must preserve the complete request record when an
operation fails.

For example, attempting to issue a card while its status is `requested`
must raise an error without changing the status or any other field.

Functions must validate all relevant conditions before performing
mutations.

Persistence failures must also be handled carefully so that a failed
save does not silently corrupt or overwrite a previously valid file.

The team will agree on the save strategy and rollback responsibilities
during integration.

### 9. Integration Agreement

Engineer A and Engineer B have agreed on the function interfaces
used to connect the workflow component to the storage component.

Engineer A is responsible for request creation, validation, ID generation,
request lookup, and JSON persistence.

Engineer B is responsible for approval, card issuance, card returns,
and command-line interaction.

Engineer B will use the agreed storage functions rather than bypassing
the storage component.

Both engineers will test their components independently and run the
complete test suite after integration.

### Engineer B: Workflow and CLI

Responsibilities:

- Request approval.
- Card issuance.
- Card return.
- Command-line menu.
- User input and error messages.
- Workflow tests.

### Integration Agreement

Both engineers must agree on function signatures, return values,
exception types, and storage ownership.

Engineer B must not bypass the storage interface or directly manipulate
private storage internals.

The final integration must be tested after both branches are merged.

## 10. Testing Strategy

The application will use Python's built-in `unittest` framework.

Tests will cover:

- Successful request creation.
- Invalid inputs.
- Unique IDs.
- Valid and invalid state transitions.
- Approval and approver validation.
- Unknown request IDs.
- JSON persistence and reloading.
- Corrupted files and invalid records.
- Data preservation after failed operations.
- Command-line handling of invalid choices.

The full test suite must pass after integration.

## 11. Decisions Requiring Team Confirmation

The following details must be confirmed by both engineers:

1. Exact function signatures and return values.
2. Whether request lookup returns a stored dictionary or a copy.
3. How workflow mutations and JSON saving are coordinated.
4. How failed saves are prevented from leaving inconsistent data.
5. How a missing JSON file differs from an empty or invalid file.

These decisions must match the actual implementation.