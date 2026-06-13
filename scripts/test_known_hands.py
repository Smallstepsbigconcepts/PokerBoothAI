from hero_hand_detector_v1 import hand_class

tests = [
    ("K", "spade", "Q", "diamond", "KQo"),
    ("T", "heart", "5", "club", "T5o"),
    ("A", "spade", "3", "spade", "A3s"),
    ("6", "club", "6", "diamond", "66"),
]

for r1, s1, r2, s2, expected in tests:

    result = hand_class(
        r1,
        s1,
        r2,
        s2
    )

    status = "PASS" if result == expected else "FAIL"

    print(
        status,
        expected,
        result
    )
