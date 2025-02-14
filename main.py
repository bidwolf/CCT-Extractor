"""
This script is the main entry point for the application.
"""

import asyncio
from src.cct_assistant import CCTAssistant
from src.config import config
from src.event_handler import CCTEventHandler
from src.webscrapper import WebscrapperCCT


async def main():
    # event_handler = CCTEventHandler()
    # assistant = CCTAssistant(config=config, event_handler=event_handler)
    # await assistant.process_ccts()
    await WebscrapperCCT().get_json_data()


if __name__ == "__main__":
    # event_handler = CCTEventHandler()
    # assistant = CCTAssistant(config=config, event_handler=event_handler)
    # assistant.process_ccts()
    asyncio.run(main())
