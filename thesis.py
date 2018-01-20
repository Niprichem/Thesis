import requests
import json

import time


def get_user_groups(params):
    response = requests.get('https://api.vk.com/method/groups.get', params).json()
    return response


def get_group_by_id(id_, version):
    params = {
        'group_id': id_,
        'fields': ['members_count'],
        'v': version
    }
    response = requests.get('https://api.vk.com/method/groups.getById', params).json()
    group_data = response['response'][0]
    return {
        'name': group_data['name'],
        'gid': group_data['id'],
        'members_count': group_data['members_count']
    }


def main():
    version = '5,69'
    token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'

    params = {
        'user_id': 5030613,
        'access_token': token,
        'v': version
    }

    response = requests.get('https://api.vk.com/method/friends.get', params).json()
    friends = set(response['response']['items'])

    group_response = get_user_groups(params)
    groups = set(group_response['response']['items'])

    all_friend_groups = set()
    for i, friend_id in enumerate(friends):
        params = {
            'user_id': friend_id,
            'access_token': token,
            'v': version
        }

        if i % 3 == 0:
            time.sleep(1)

        response = get_user_groups(params)
        if response.get('error'):
            continue

        all_friend_groups = all_friend_groups | set(response['response']['items'])
        print(i)

    group_id_set = groups - all_friend_groups

    result_list = []
    for group_id in group_id_set:

        if i % 3 == 0:
            time.sleep(1)

        result_list.append(get_group_by_id(group_id, version))

    filename = 'groups.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4)


if __name__ == '__main__':
    main()
