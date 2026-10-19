# Changelog

## v1.0.0 — Build 001 (2026-10-19)

- Extracted the AI-deck JPEG-over-TCP camera viewer from `multiranger_push_camera.py`.
- Removed all Crazyflie radio, arming, flying, obstacle avoidance, and detection code.
- Removed automatic writing of frames to disk.
- Preserved default host `192.168.4.1` and port `5000` and existing camera address CLI options.
- Kept the OpenCV window responsive during network pauses; added connection and decode diagnostics.
- Added macOS quick-start instructions for Wi-Fi hotspot `Bitcraze AI-deck example`.
