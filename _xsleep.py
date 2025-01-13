# _xsleep.py
import ctypes
import sys
import platform
import random
import os

def _get_sleep_func():
    """
    Gets the appropriate sleep function based on the operating system.
    """
    if sys.platform.startswith("win32"):
        # Windows
        sleep_func = ctypes.windll.kernel32.Sleep
        sleep_func.argtypes = [ctypes.c_ulong]  # DWORD
        sleep_unit = 1000  # Sleep takes milliseconds
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Linux and macOS
        libc_name = "libc.so.6"
        if sys.platform.startswith("darwin"):
            libc_name = "libc.dylib"
        try:
            libc = ctypes.CDLL(libc_name)
        except OSError:
            libc = ctypes.CDLL("/usr/lib/libc.dylib")

        usleep_func = libc.usleep
        usleep_func.argtypes = [ctypes.c_uint]  # unsigned int
        sleep_func = lambda t: usleep_func(int(t))  # usleep takes microseconds
        sleep_unit = 1000000
    else:
        raise OSError("Unsupported operating system.")

    return sleep_func, sleep_unit

class XSleep:
    def __init__(self):
        self.sleep_func, self.sleep_unit = _get_sleep_func()

    def milliseconds(self, ms):
        """Sleeps for the specified number of milliseconds."""
        self._sleep(ms / 1000)

    def seconds(self, secs):
        """Sleeps for the specified number of seconds."""
        self._sleep(secs)

    def minutes(self, mins):
        """Sleeps for the specified number of minutes."""
        self._sleep(mins * 60)

    def hours(self, hrs):
        """Sleeps for the specified number of hours."""
        self._sleep(hrs * 3600)

    def _sleep(self, seconds):
        """Internal sleep function."""
        time_to_sleep = int(seconds * self.sleep_unit)
        print(f"Sleeping for {seconds} seconds ({time_to_sleep} {'milliseconds' if self.sleep_unit == 1000 else 'microseconds'})...")
        self.sleep_func(time_to_sleep)
        print("Awake!")

    # 10 additional features that the 'time' module doesn't have:

    def get_pid(self):
        """Gets the current process ID."""
        if sys.platform.startswith("win32"):
            return ctypes.windll.kernel32.GetCurrentProcessId()
        else:
            return os.getpid()

    def get_cpu_count(self):
        """Gets the number of CPUs/cores in the system."""
        if sys.platform.startswith("win32"):
            return int(os.environ.get('NUMBER_OF_PROCESSORS', 1))
        elif sys.platform.startswith("linux"):
            cpu_count = 0
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.strip().startswith('processor'):
                        cpu_count += 1
            return cpu_count
        elif sys.platform.startswith("darwin"):
            libc = ctypes.CDLL("libc.dylib")
            num_cpu = ctypes.c_int(0)
            size = ctypes.c_size_t(ctypes.sizeof(num_cpu))
            libc.sysctlbyname(ctypes.c_char_p(b"hw.ncpu"), ctypes.byref(num_cpu), ctypes.byref(size), None, 0)
            return num_cpu.value
        else:
            return 1

    def get_random_delay(self, min_seconds, max_seconds):
        """Sleeps for a random time between min_seconds and max_seconds."""
        random_delay = random.uniform(min_seconds, max_seconds)
        self._sleep(random_delay)

    def is_interactive(self):
        """Checks if the current session is interactive (run by a user in a terminal)."""
        return sys.stdin.isatty()

    def get_platform(self):
        """Returns a string identifying the current platform."""
        return sys.platform

    def get_uptime(self):
        """Returns the system uptime in seconds (time since the last boot)."""
        if sys.platform.startswith("linux"):
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            return uptime_seconds
        elif sys.platform.startswith("darwin"):
            libc = ctypes.CDLL("libc.dylib")
            boottime = ctypes.c_int64(0)
            size = ctypes.c_size_t(ctypes.sizeof(boottime))
            if libc.sysctlbyname(ctypes.c_char_p(b"kern.boottime"), ctypes.byref(boottime), ctypes.byref(size), None, 0) != -1:
                now = int(time.time())
                return now - boottime.value
            else:
                return None        
        elif sys.platform.startswith("win32"):
            return int(time.time() - psutil.boot_time())
        else:
            return None  # Implement for other platforms if needed

    def get_free_memory(self):
        """Returns the amount of free memory in bytes."""
        if sys.platform.startswith("linux"):
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemAvailable:'):
                        return int(line.split()[1]) * 1024  # Convert from kB to bytes
        elif sys.platform.startswith("darwin"):
            libc = ctypes.CDLL("libc.dylib")
            vm_stats = vm_statistics()
            size = ctypes.c_size_t(ctypes.sizeof(vm_stats))
            if libc.host_statistics(libc.mach_host_self(), 0, ctypes.byref(vm_stats), ctypes.byref(size)) == 0:
                page_size = 4096  # Default page size for macOS
                return vm_stats.free_count * page_size
            else:
                return None
        elif sys.platform.startswith("win32"):
            kernel32 = ctypes.windll.kernel32
            GlobalMemoryStatusEx = kernel32.GlobalMemoryStatusEx
            GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MEMORYSTATUSEX)]
            GlobalMemoryStatusEx.restype = ctypes.c_int

            memorystatus = MEMORYSTATUSEX()
            memorystatus.dwLength = ctypes.sizeof(memorystatus)
            if GlobalMemoryStatusEx(ctypes.byref(memorystatus)):
                return memorystatus.ullAvailPhys
            else:
                return None
        else:
            return None  # Implement for other platforms

    def get_username(self):
        """Returns the current username."""
        if sys.platform.startswith("win32"):
            return os.environ.get("USERNAME")
        else:
            return os.environ.get("USER")
   
    def get_current_time_ms(self):
        """Returns the current time in milliseconds since the epoch."""
        if sys.platform.startswith("win32"):
            # On Windows, use GetTickCount64 for milliseconds since system startup
            return ctypes.windll.kernel32.GetTickCount64()
        else:
            # For Linux/macOS, use clock_gettime with CLOCK_MONOTONIC
            CLOCK_MONOTONIC = 1  # Use 1 for Linux, might need adjustment for macOS
            class timespec(ctypes.Structure):
                _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]

            libc = ctypes.CDLL("libc.so.6")
            if sys.platform.startswith("darwin"):
                libc = ctypes.CDLL("libc.dylib")
            
            ts = timespec()
            libc.clock_gettime(CLOCK_MONOTONIC, ctypes.byref(ts))
            return ts.tv_sec * 1000 + ts.tv_nsec // 1000000

    def execute_command(self, command):
        """Executes a shell command and returns the output."""
        return os.popen(command).read()

    def print_message_with_delay(self, message, delay_seconds):
        """Prints a message with a delay before each character."""
        for char in message:
            print(char, end='', flush=True)
            self._sleep(delay_seconds)
        print()

def xsleep(seconds):
    """
    Multi-platform sleep function with additional logic.
    """
    sleep_func, sleep_unit = _get_sleep_func()

    time_to_sleep = int(seconds * sleep_unit)
    print(f"Sleeping for {seconds} seconds ({time_to_sleep} {'milliseconds' if sleep_unit == 1000 else 'microseconds'})...")

    sleep_func(time_to_sleep)
    print("Awake!")