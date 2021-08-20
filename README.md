# water-cooler-talks
Buzz a colleague to join the Jitsi room for water cooler conversations.
Note: We have our own Jitsi server setup, with a room set aside for chit-chat at Qxf2.

Prerequisites
1. Install Python 3.x
2. Add Python 3.x your PATH environment variable
3. If you do not have it already, get pip (NOTE: Most recent Python distributions come with pip)
4. AWS credential files, placed at the right location in your machine

Setup
1. Clone the repo
2. Create and activate the virtual environment with the relevant Python version
3. Run `pip install -r requirements.txt` to install project dependencies
4. Add an environment variable,
    `JITSI_ROOM_SIZE_ENDPOINT` with value as the endpoint that returns the water-cooler-talks Jitsi room's size.

To run the Jitsi listener in your machine:
`python jitsi_listener.py`
