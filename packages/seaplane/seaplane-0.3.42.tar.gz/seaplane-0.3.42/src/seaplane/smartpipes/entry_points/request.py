def is_valid_body(body):
    if isinstance(body, dict):
        if ("batch" in body or "content" in body):
            return True
    return False


def is_batch_processing(body):
    return len(body["input"]) > 1
