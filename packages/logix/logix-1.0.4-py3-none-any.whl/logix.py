import datetime

COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_BLUE = "\033[34m"
COLOR_YELLOW = "\033[33m"
COLOR_RESET = "\033[0m"

class SaveLog:
    enabled = False
    filepath = "logix.log"

    @staticmethod
    def log(level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} | {level} | {message}"
        colored_message = SaveLog.get_colored_message(level, formatted_message)
        print(colored_message)

        if SaveLog.enabled:
            with open(SaveLog.filepath, "a", encoding="utf-8") as file:
                file.write(formatted_message + "\n")

    @staticmethod
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
    SaveLog.log("success", message)

def error(message):
    SaveLog.log("error", message)

def info(message):
    SaveLog.log("info", message)

def warning(message):
    SaveLog.log("warning", message)

def LogSave(enabled=False, file="logix.log"):
    SaveLog.enabled = enabled
    SaveLog.filepath = file