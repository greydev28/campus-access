# Learning Log — Campus Access-Card Request Manager

## Project Information

**Project:** Campus Access-Card Request Manager

**Language:** Python

**Storage:** JSON

**Testing framework:** unittest

**Collaboration:** GitHub

---

# Engineer A — Registration and Data Safety

## Learning Cycle 1: Dictionaries and Validation

### Question

Why should input validation happen before a request is added to
the application's dictionary?

### AI Explanation

A dictionary stores information as key-value pairs.

In this project, each request is represented by a dictionary, and the
application stores requests so that they can be retrieved and updated.

Validation checks whether input satisfies the application's rules.

For example, a request must have a nonempty fellow ID and a valid
card type.

If invalid data is inserted before validation, the application may
store an incomplete or invalid record.

Validating first helps prevent incorrect records from entering storage.

### My Experiment

Experiment to perform:

1. Create a valid request.
2. Try creating a request with a blank fellow ID.
3. Try creating a request with an unsupported card type.
4. Inspect the stored requests after each attempt.

Record the actual function calls and results here.

### Verification

Record whether invalid requests were rejected and whether the stored
records remained unchanged.

### Final Decision

Document the validation rules that the implementation successfully
enforces.

Do not mark this cycle complete until the experiment has been run.

---

## Learning Cycle 2: JSON Persistence and ID Generation

### Question

How can the application prevent duplicate request IDs after restarting?

### AI Explanation

JSON allows Python data to be saved to a file and loaded later.

When an application restarts, its in-memory variables are recreated.
Therefore, the application must use saved records to determine which
request IDs already exist.

The loader should validate the saved data before accepting it.

The application must not assume that locally stored JSON is valid:
the file may be corrupted, contain duplicate IDs, or contain records
with missing fields.

### My Experiment

Experiment to perform:

1. Create and save two requests.
2. Restart the application.
3. Load the saved requests.
4. Create another request.
5. Confirm that its ID is not already in use.
6. Test loading a malformed JSON file.

Record the actual results here.

### Verification

Record the IDs generated before and after restarting.

Also record how the application responds to the malformed file and
whether previously loaded records remain intact.

### Final Decision

Document the ID generation and JSON validation strategy adopted
by the team.

Do not mark this cycle complete until the experiment has been run.

---

# Engineer B — Workflow and CLI

## Learning Cycle 1: State Machines and Invariants

### Question

Why must the application check a request's current status before
changing it?

### AI Explanation

A state machine defines the states an object can occupy and the
transitions allowed between those states.

The access-card request workflow has four states:

requested -> approved -> issued -> returned

An invariant is a condition that must remain true throughout the
application's operation.

One important invariant is that a request must not skip a workflow
stage.

For example, a request in the `requested` state cannot move directly
to `issued`.

Checking the current status before changing it prevents illegal
transitions.

### My Experiment

Experiment to perform:

1. Create a request.
2. Record its complete dictionary.
3. Attempt to issue the card before approval.
4. Inspect the dictionary after the operation fails.
5. Compare it with the original dictionary.

Record the actual function calls and results here.

### Verification

Record whether the operation raised the expected error.

Confirm whether every field remained unchanged after the failed
operation.

### Final Decision

Document how the workflow functions enforce legal transitions
and preserve records when operations fail.

Do not mark this cycle complete until the experiment has been run.

---

## Learning Cycle 2: Unit Testing and Error Handling

### Question

How can unit tests prove that an invalid operation does not modify
a request?

### AI Explanation

Python's `unittest` framework provides tools for testing application
behaviour.

`assertEqual` checks whether two values are equal.

`assertRaises` checks whether an operation raises an expected
exception.

A test can copy a request before an operation, attempt an invalid
transition, and compare the request with the saved copy afterward.

This verifies both error handling and data integrity.

### My Experiment

Experiment to perform:

1. Create a request.
2. Copy its complete dictionary.
3. Attempt an illegal transition.
4. Use `assertRaises` to check the exception.
5. Use `assertEqual` to compare the current record with the copy.
6. Run the workflow tests.

Record the actual test command and results here.

### Verification

Record whether the test passed.

If it failed, record the failure message, investigate the cause,
make a correction, and run the test again.

### Final Decision

Document which tests successfully verify the workflow rules and
whether any additional edge cases were identified.

Do not mark this cycle complete until the experiment has been run.

---

# Final Reflection

## Engineer A

What did I learn about dictionaries, validation, JSON persistence,
and unique ID generation?

Answer:

## Engineer B

What did I learn about state machines, workflow validation,
unit testing, and error handling?

Answer:

## Team Reflection

What integration problems did we encounter?

Answer:

How did we resolve differences between the two engineers'
function signatures or storage assumptions?

Answer:

Did the complete test suite pass after merging the branches?

Answer: