from storage import get_request, save_requests


def approve_request(request_id, approved_by):
    request = get_request(request_id)

    if request["status"] != "requested":
        raise ValueError("Only requested cards can be approved.")

    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver ID cannot be empty.")

    request["approved_by"] = approved_by.strip()
    request["status"] = "approved"
    save_requests() 
    return request


def issue_card(request_id):
    request = get_request(request_id)

    if request["status"] != "approved":
        raise ValueError("Only approved cards can be issued.")

    if not isinstance(request["approved_by"], str):
        raise ValueError("Invalid approver ID.")

    if not request["approved_by"].strip():
        raise ValueError("An approved card must have an approver.")

    request["status"] = "issued"
    save_requests() 
    return request


def return_card(request_id):
    request = get_request(request_id)

    if request["status"] != "issued":
        raise ValueError("Only issued cards can be returned.")

    request["status"] = "returned"
    save_requests() 
    return request