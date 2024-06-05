import os
from pathlib import Path

def apply_patch():
    twikit_streaming_path = Path(os.path.dirname(__file__)) / 'venv/lib/python3.8/site-packages/twikit/streaming.py'
    
    if not twikit_streaming_path.exists():
        print("twikit/streaming.py file not found.")  
        return

    with open(twikit_streaming_path, 'r') as file:
        content = file.read()
    
    content = content.replace('StreamEventType = (ConfigEvent | SubscriptionsEvent |', 'StreamEventType = [ConfigEvent, SubscriptionsEvent,')
    
    with open(twikit_streaming_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    apply_patch()
