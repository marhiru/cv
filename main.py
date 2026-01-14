from features.detection import Detector


def main() -> int:
    d = Detector(
        image_path="./tomhanks01.jpeg",
        show=False,
    )
    numbers = [1, 2, 3, 4]
    d.run()

    doubled_numbers = list(map(lambda n: n * 2, numbers))

    print(doubled_numbers)
    return 0


if __name__ == "__main__":
    main()
