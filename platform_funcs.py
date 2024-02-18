import platform


def check_platform():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        if "arm" in platform.machine().lower() or platform.machine().lower() == "aarch64":
            return "Raspberry Pi"
        else:
            return "Linux (non-Raspberry Pi)"
    else:
        return "Unknown"
