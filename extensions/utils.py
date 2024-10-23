import time

def is_string_correct(lambda_string: str) -> bool:
    if lambda_string.isspace():
        return False
    if lambda_string == "":
        return False
    return True

def shutdown(message: str) -> None:
    print(message)
    for countdown in range(10, 0, -1):
        print(f"Closing in {countdown} ", end="\r")
        time.sleep(1)
    exit()