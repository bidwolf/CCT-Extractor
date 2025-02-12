"""
This script is the main entry point for the application.
"""

from src.cct_assistant import CCTAssistant
from src.config import config
from src.event_handler import CCTEventHandler

if __name__ == "__main__":
    event_handler = CCTEventHandler()
    assistant = CCTAssistant(config=config, event_handler=event_handler)
    assistant.process_ccts()
