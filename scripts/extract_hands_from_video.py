import cv2

from hero_hand_detector_v1 import read_hero_hand
from export_hand_timeline_csv import save_hand_timeline

VIDEO_PATH = "sample_video.mp4"
OUTPUT_CSV = "hand_timeline.csv"

SAMPLE_EVERY_SECONDS = 30


def format_time(seconds):

    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)

    return f"{h:02d}:{m:02d}:{s:02d}"


def main():

    rows = []

    video = cv2.VideoCapture(VIDEO_PATH)

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    duration_seconds = frame_count / fps

    current_second = 0

    while current_second < duration_seconds:

        video.set(
            cv2.CAP_PROP_POS_MSEC,
            current_second * 1000
        )

        success, frame = video.read()

        if success:

            try:

                hand_notation, cards = read_hero_hand(
                    frame
                )

                rows.append(
                    (
                        format_time(
                            current_second
                        ),
                        hand_notation
                    )
                )

            except Exception:

                pass

        current_second += SAMPLE_EVERY_SECONDS

    video.release()

    save_hand_timeline(
        rows,
        OUTPUT_CSV
    )

    print(
        f"Saved {len(rows)} rows to {OUTPUT_CSV}"
    )


if __name__ == "__main__":
    main()
