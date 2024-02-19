import platform


def check_platform() -> str:
    system = platform.system()
    if system == "Windows":
        return "Windows"
    if system == "Linux":
        if "arm" in platform.machine().lower() or platform.machine().lower() == "aarch64":
            return "Raspberry Pi"
        return "Linux (non-Raspberry Pi)"
    return "Unknown"
