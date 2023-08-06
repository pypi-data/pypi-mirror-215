import datetime

COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_BLUE = "\033[34m"
COLOR_YELLOW = "\033[33m"
COLOR_RESET = "\033[0m"

def log(level, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colored_timestamp = get_colored_timestamp()
    colored_level = get_colored_level(level)
    colored_message = get_colored_message(level, message)
    formatted_message = f"{colored_timestamp} | {colored_level} | {colored_message}"
    print(formatted_message)

def get_colored_timestamp():
    return f"{COLOR_CYAN}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLOR_RESET}"

def get_colored_level(level):
    if level == "success":
        return f"{COLOR_GREEN}{level}{COLOR_RESET}"
    elif level == "error":
        return f"{COLOR_RED}{level}{COLOR_RESET}"
    elif level == "info":
        return f"{COLOR_BLUE}{level}{COLOR_RESET}"
    elif level == "warning":
        return f"{COLOR_YELLOW}{level}{COLOR_RESET}"
    else:
        return level

def get_colored_message(level, message):
    if level == "success":
        return f"{COLOR_GREEN}{message}{COLOR_RESET}"
    elif level == "error":
        return f"{COLOR_RED}{message}{COLOR_RESET}"
    elif level == "info":
        return f"{COLOR_BLUE}{message}{COLOR_RESET}"
    elif level == "warning":
        return f"{COLOR_YELLOW}{message}{COLOR_RESET}"
    else:
        return message

def success(message):
    log("success", message)

def error(message):
    log("error", message)

def info(message):
    log("info", message)

def warning(message):
    log("warning", message)