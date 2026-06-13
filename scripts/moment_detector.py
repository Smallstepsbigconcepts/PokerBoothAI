import cv2
import csv
import os

VIDEO_PATH = "samples/session.mp4"
OUTPUT_DIR = "output/moment_detection"
FRAME_INTERVAL_SECONDS = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def main():
    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Video not found at {VIDEO_PATH}")
        print("Put a test video in samples/ and rename it session.mp4")
        return

    video = cv2.VideoCapture(VIDEO_PATH)

    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"Loaded video: {VIDEO_PATH}")
    print(f"FPS: {fps}")
    print(f"Duration: {format_time(duration)}")

    frame_interval = int(fps * FRAME_INTERVAL_SECONDS)

    results_path = os.path.join(OUTPUT_DIR, "candidate_moments.csv")

    with open(results_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "event_type", "confidence", "notes", "frame_file"])

        frame_number = 0
        saved_count = 0

        while True:
            ret, frame = video.read()
            if not ret:
                break

            if frame_number % frame_interval == 0:
                timestamp_seconds = frame_number / fps
                timestamp = format_time(timestamp_seconds)

                frame_file = f"frame_{saved_count:05d}_{timestamp.replace(':', '-')}.jpg"
                frame_path = os.path.join(OUTPUT_DIR, frame_file)

                cv2.imwrite(frame_path, frame)

                writer.writerow([
                    timestamp,
                    "Review Candidate",
                    "Low",
                    "Sampled frame for manual review",
                    frame_file
                ])

                saved_count += 1

            frame_number += 1

    video.release()

    print(f"Done.")
    print(f"Saved {saved_count} review frames.")
    print(f"Results written to: {results_path}")

if __name__ == "__main__":
    main()
