# Crazyflie AI-deck — Camera-Only Viewer

**Version:** 1.0.0 · **Build:** 001

Minimal Python 3.10+ viewer for the **JPEG** camera stream from a Crazyflie AI-deck over Wi-Fi. The script **does not fly, arm, or control the Crazyflie**. It does not save or record images.

## Getting started (macOS)

### 1. Install the dependencies (while connected to the internet)

Open Terminal in this folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Do this **before** joining the AI-deck's Wi-Fi hotspot, which normally has no internet access.

### 2. Power the Crazyflie and connect to the AI-deck hotspot

1. Turn on the Crazyflie with the AI-deck installed and its JPEG streamer running.
2. On your Mac, open **System Settings → Wi-Fi**.
3. Connect to **`Bitcraze AI-deck example`**.
4. If macOS says the Wi-Fi network has no internet connection, remain connected to that network.

### 3. Start the camera viewer

In the same Terminal window, run:

```bash
python ai_deck_camera.py
```

The viewer connects to **`192.168.4.1:5000`** and opens an OpenCV camera window. Press **Q** or **Esc** in that window to exit, or **Ctrl+C** in Terminal.

### Optional: override the network address

```bash
python ai_deck_camera.py --camera-host 192.168.4.1 --camera-port 5000
```

## Troubleshooting

- **Cannot connect:** Check that the Mac is connected to `Bitcraze AI-deck example`, that the AI-deck is powered, and that its streamer is running.
- **Connected but black window:** The program is waiting for valid JPEG frames. Confirm the deck is running a **JPEG-over-TCP** streamer, not a raw-image or NanoCockpit stream. The original source code used JPEG markers, and this version deliberately retains that protocol.
- **No internet warning on macOS:** Expected for the AI-deck hotspot.
- **`ModuleNotFoundError: cv2`:** Activate `.venv` and install `requirements.txt` again (on an internet-connected network).

## Files

- `ai_deck_camera.py` — complete camera-only viewer
- `requirements.txt` — Python packages
- `README.md` — setup and operation

## Changes from the original script

Removed Crazyradio/cflib, flight and arming commands, MotionCommander, Multi-ranger collision handling, landmark detection, image file writing, and unrelated dependencies. Kept TCP JPEG reception and live OpenCV display, with support for JPEGs split across TCP reads and Q/Esc exit.

## Compatibility note

This viewer is specifically for a JPEG stream like the one parsed by the supplied script. Bitcraze's newer AI-deck demos may use different Wi-Fi names and/or raw/CPX image protocols; those require the corresponding viewer or firmware configuration.

Official references:
- [Bitcraze Wi-Fi Video Streamer](https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/examples/wifi-streamer/)
- [Bitcraze Getting started with the AI-deck](https://www.bitcraze.io/documentation/tutorials/getting-started-with-aideck/)
