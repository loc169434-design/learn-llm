import argparse
import json


def load_users(filepath: str) -> list[dict]:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def filter_by_city(users, city) -> list[dict]:
    return [user for user in users if user["city"] == city]


def filter_by_min_age(users, min_age) -> list[dict]:
    return [user for user in users if user["age"] >= min_age]


def main():
    parser = argparse.ArgumentParser(description="Công cụ lọc người dùng theo thành phố")
    parser.add_argument("--city", help="Tên thành phố cần lọc")
    parser.add_argument("--min-age", type=int, help="Tuổi tối thiểu cần lọc")
    args = parser.parse_args()
    users = load_users("users.json")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
