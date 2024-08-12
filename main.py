import json

from defs import get_all_directions, get_users_by_direction

def main():
    all_users = []

    directions = get_all_directions()
    for direction in directions:
        users = get_users_by_direction(direction)
        all_users += users

    with open('users.json', 'w') as json_file:
        json.dump(all_users, json_file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()