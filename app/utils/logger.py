import time
from datetime import datetime

class Logger:
    def __init__(self):
        self.start_time = None
        self.section_count = 0
    
    def header(self, message):
        """Print a header message with formatting"""
        print(f"\n{'='*60}")
        print(f"  {message}")
        print(f"{'='*60}")
    
    def section(self, message):
        """Print a section message with formatting"""
        self.section_count += 1
        print(f"\n{'-'*40}")
        print(f"  {self.section_count}. {message}")
        print(f"{'-'*40}")
    
    def progress(self, message):
        """Print a progress message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🔄 {message}")
    
    def success(self, message):
        """Print a success message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ✅ {message}")
    
    def error(self, message):
        """Print an error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ❌ {message}")
    
    def info(self, message):
        """Print an info message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ℹ️  {message}")
    
    def start_timer(self):
        """Start the timer"""
        self.start_time = time.time()
        print(f"\n⏱️  Timer started at {datetime.now().strftime('%H:%M:%S')}")
    
    def end_timer(self):
        """End the timer and display elapsed time"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            print(f"\n⏱️  Total execution time: {minutes}m {seconds}s")
        else:
            print("\n⏱️  Timer was not started")

# Create a global logger instance
logger = Logger()
