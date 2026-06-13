import csv


def save_hand_timeline(rows, output_file):

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "timestamp",
            "hero_hand"
        ])

        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":

    sample_rows = [
        ("00:00:30", "KQo"),
        ("00:01:00", "66"),
        ("00:01:30", "A3s"),
    ]

    save_hand_timeline(
        sample_rows,
        "sample_timeline.csv"
    )

    print(
        "Timeline exported."
    )
