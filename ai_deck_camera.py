#!/usr/bin/env python3
"""AI-deck JPEG camera viewer over Wi-Fi.

Version: 1.0.0 | Build: 001
Requires the AI-deck to stream JPEG images over TCP.
No Crazyradio, cflib, flight control, or frame recording is used.
"""

import argparse
import socket

import cv2
import numpy as np

VERSION = "1.0.0"
BUILD = "001"
DEFAULT_HOST = "192.168.4.1"
DEFAULT_PORT = 5000
WINDOW_NAME = "Crazyflie AI-deck Camera"
MAX_BUFFER_BYTES = 8 * 1024 * 1024
JPEG_START = b"\xff\xd8"
JPEG_END = b"\xff\xd9"


def get_latest_jpeg(buffer: bytearray) -> bytes | None:
    """Extract complete JPEGs from a TCP byte stream, returning the newest.

    TCP packets can split JPEG markers or contain multiple images. Bytes of an
    incomplete JPEG remain in the buffer until more data arrives.
    """
    latest = None

    while True:
        start = buffer.find(JPEG_START)
        if start < 0:
            # Preserve a possible split start marker (0xFF in this chunk).
            buffer[:] = b"\xff" if buffer.endswith(b"\xff") else b""
            return latest

        if start:
            del buffer[:start]

        end = buffer.find(JPEG_END, len(JPEG_START))
        if end < 0:
            return latest  # Wait for the remainder of the JPEG.

        end += len(JPEG_END)
        latest = bytes(buffer[:end])
        del buffer[:end]


def show_camera(host: str, port: int) -> int:
    print(f"Connecting to AI-deck camera at {host}:{port} ...")
    try:
        connection = socket.create_connection((host, port), timeout=8.0)
    except OSError as exc:
        print(f"Connection failed: {exc}")
        print('Connect to Wi-Fi "Bitcraze AI-deck example" and retry.')
        return 1

    buffer = bytearray()
    frames_received = 0

    try:
        with connection:
            connection.settimeout(0.03)
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.imshow(WINDOW_NAME, np.zeros((240, 320, 3), dtype=np.uint8))
            print("Connected. Waiting for JPEG frames. Press Q or Esc to quit.")

            while True:
                try:
                    chunk = connection.recv(16384)
                except socket.timeout:
                    chunk = None  # Keep the OpenCV window responsive.

                if chunk == b"":
                    print("AI-deck closed the connection.")
                    break

                if chunk:
                    buffer.extend(chunk)
                    if len(buffer) > MAX_BUFFER_BYTES:
                        print("Stream buffer exceeded 8 MiB; discarding incomplete data.")
                        buffer.clear()
                    else:
                        jpeg = get_latest_jpeg(buffer)
                        if jpeg is not None:
                            frame = cv2.imdecode(
                                np.frombuffer(jpeg, dtype=np.uint8),
                                cv2.IMREAD_COLOR,
                            )
                            if frame is not None:
                                frames_received += 1
                                cv2.imshow(WINDOW_NAME, frame)
                                #save the image:
                                cv2.imwrite("sample.png", frame)

                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), ord("Q"), 27):
                    break

    except KeyboardInterrupt:
        print("Stopped by user.")
    except (OSError, cv2.error) as exc:
        print(f"Camera error: {exc}")
        return 1
    finally:
        cv2.destroyAllWindows()

    print(f"Viewer stopped. Displayed {frames_received} decoded frame(s).")
    if frames_received == 0:
        print("No JPEG frames were decoded. Check the AI-deck streaming firmware.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera-host", default=DEFAULT_HOST, help="AI-deck IP address")
    parser.add_argument("--camera-port", type=int, default=DEFAULT_PORT, help="TCP port")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION} build {BUILD}")
    args = parser.parse_args()
    return show_camera(args.camera_host, args.camera_port)


if __name__ == "__main__":
    raise SystemExit(main())
