import os
import uuid
from datetime import datetime
from pathlib import Path

class AgentTracker:
    def __init__(self):
        self.track_dir = Path("track")
        self.track_dir.mkdir(exist_ok=True)
    
    def create_request_file(self, request_id: str) -> Path:
        """Create a new tracking file for a request"""
        file_path = self.track_dir / f"request_{request_id}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"=== HUMANA FORM FILLING REQUEST TRACKING ===\n")
            f.write(f"Request ID: {request_id}\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
        return file_path
    
    def log_action(self, request_id: str, action: str, details: str = ""):
        """Log an action to the request's tracking file"""
        file_path = self.track_dir / f"request_{request_id}.txt"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {action}")
            if details:
                f.write(f" - {details}")
            f.write("\n")

# Global instance
agent_tracker = AgentTracker()
