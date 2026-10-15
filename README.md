# campus-access

import json
import re
from pathlib import Path


ALLOWED_CARD_TYPES = {"visitor", "student", "staff"}
ALLOWED_STATUSES = {"requested", "approved", "issu ed", "returned"}
REQUEST_ID_PATTERN = re.compile(r"A[0-9]{3}\Z", re.ASCII)

requests = {}
next_id = 1

def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str):
        raise ValueError("Fellow ID must be a string.")

    fellow_id = fellow_id.strip().upper()

    if not fellow_id:
        raise ValueError("Fellow ID cannot be empty.")

    if not re.fullmatch(r"F[0-9]{3}", fellow_id):
        raise ValueError("Invalid fellow ID. Use the format F001.")

    return fellow_id


def validate_card_type(card_type):
    if not isinstance(card_type, str) or card_type not in ALLOWED_CARD_TYPES:
        raise ValueError("card_type must be visitor, student, or staff.")

def validate_request_id(request_id):
    if not isinstance(request_id, str) or not REQUEST_ID_PATTERN.fullmatch(request_id):
        raise ValueError("Request ID must use the format A001 (ASCII digits only).")
    return request_id
def create_request(fellow_id,card_type):
    global next_id
    validate_fellow_id(fellow_id)
    validate_card_type(card_type)
    
    if next_id > 999:
        raise ValueError("Request ID limit reached (A999)")

    request_id = f'A{next_id:03d}'
    if request_id in requests:
        raise RuntimeError(f'refusing to create duplicate request   ID {request_id}')

    request = {
        "id" : request_id,
        "fellow_id":fellow_id.strip(),
        "card_type":card_type,
        "status":"requested",
        "approved_by":None
    }

    requests[request_id] = request
    next_id +=1
    return request.copy()

def get_request(request_id):
    validate_request_id(request_id)
    if request_id not in requests:
        raise KeyError(f"No request found with ID {request_id}.")
    return requests[request_id].copy()
    

def list_requests():
    return [request.copy() for request in requests.values()]
def save_requests(path = "data/requests.json"):
    destination = Path(path)
    payload = {
        "requests" : list_requests(),
        "next_id": next_id
    }
    temp = destination.with_name(destination.name + ".tmp")
    try:
        with temp.open("w",encoding="utf-8") as file:
            json.dump(payload,file,indent= 4)
            temp.replace(destination)
    except OSError:
        if temp.exists():
           temp.unlink()
        raise

def _validate_loaded_payload(payload):
    
    if not isinstance(payload, dict):
        raise ValueError("Invalid save file: top-level JSON value must be an object.")

    if set(payload.keys()) != {"requests", "next_id"}:
        raise ValueError("Invalid save file: expected exactly 'requests' and 'next_id'.")

    records = payload["requests"]
    saved_next_id = payload["next_id"]

    if not isinstance(records, list):
        raise ValueError("Invalid save file: 'requests' must be a list.")

    if type(saved_next_id) is not int or not 1 <= saved_next_id <= 1000:
        raise ValueError("Invalid save file: 'next_id' must be an integer from 1 to 1000.")

    candidate = {}
    highest_id = 0
    required_fields = {"id", "fellow_id", "card_type", "status", "approved_by"}

    for index, record in enumerate(records):
        location = f"request at index {index}"

        if not isinstance(record, dict) or set(record.keys()) != required_fields:
            raise ValueError(f"Invalid save file: {location} must contain exactly {sorted(required_fields)}.")

        request_id = record["id"]
        validate_request_id(request_id)

        if request_id in candidate:
            raise ValueError(f"Invalid save file: duplicate request ID {request_id}.")

        fellow_id = record["fellow_id"]
        validate_fellow_id(fellow_id)
        if fellow_id != fellow_id.strip():
            raise ValueError(f"Invalid save file: {location} has leading or trailing whitespace in fellow_id.")

        validate_card_type(record["card_type"])

        status = record["status"]
        if not isinstance(status, str) or status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid save file: {location} has an invalid status.")

        approved_by = record["approved_by"]
        if status == "requested":
            if approved_by is not None:
                raise ValueError(f"Invalid save file: {location} in requested state must have approved_by null.")
        else:
            if not isinstance(approved_by, str) or not approved_by.strip():
                raise ValueError(f"Invalid save file: {location} must have a nonempty approved_by.")

        # Store a fresh dictionary, not an object taken directly from parsed JSON.
        candidate[request_id] = {
            "id": request_id,
            "fellow_id": fellow_id,
            "card_type": record["card_type"],
            "status": status,
            "approved_by": approved_by,
        }
        highest_id = max(highest_id, int(request_id[1:]))

    # The next ID must not collide with any existing ID.
    if saved_next_id <= highest_id:
        raise ValueError("Invalid save file: next_id would reuse an existing request ID.")

    # Enforce sequential IDs with no gaps in this project's generated history.
    expected_next_id = highest_id + 1
    if saved_next_id != expected_next_id:
        raise ValueError("Invalid save file: next_id does not match the highest saved request ID.")

    return candidate, saved_next_id


def load_requests(path="requests.json"):

    global requests, next_id

    source = Path(path)
    if not source.exists():
        requests = {}
        next_id = 1
        return

    try:
        with source.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Cannot load {source}: invalid JSON at line {error.lineno}, column {error.colno}."
        ) from error

    # Validate into temporary variables. Only replace live data after all checks pass.
    candidate, candidate_next_id = _validate_loaded_payload(payload)
    requests = candidate
    next_id = candidate_next_id


def update_request_status(request_id, new_status, approved_by=None):
    
    global _requests

    validate_request_id(request_id)
    if request_id not in _requests:
        raise KeyError(f"No request found with ID {request_id}.")

    transitions = {
        "requested": "approved",
        "approved": "issued",
        "issued": "returned",
    }

    current = _requests[request_id]
    expected_next = transitions.get(current["status"])

    if new_status != expected_next:
        raise ValueError(
            f"Unsupported transition: {current['status']} -> {new_status}."
        )

    updated = current.copy()

    if new_status == "approved":
        if not isinstance(approved_by, str) or not approved_by.strip():
            raise ValueError("approved_by must be a nonempty staff identifier.")
        updated["approved_by"] = approved_by.strip()

    if new_status == "issued" and (
        not isinstance(updated["approved_by"], str) or not updated["approved_by"].strip()
    ):
        raise ValueError("A request must have a nonempty approver before it can be issued.")

    updated["status"] = new_status
    _requests[request_id] = updated
    return updated.copy()

