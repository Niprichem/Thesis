import requests


def get_user_groups(params):
    response = requests.get('https://api.vk.com/method/groups.get', params).json()
    return response


def main():
    VERSION = '5,69'
    TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'

    params = {
        'user_id': 5030613,
        'access_token': TOKEN,
        'v': VERSION
    }

    response = requests.get('https://api.vk.com/method/friends.get', params).json()
    friends = set(response['response']['items'])

    group_response = get_user_groups(params)
    groups = set(group_response['response']['items'])

    all_friend_groups = set()
    for friend_id in friends:
        params = {
            'user_id': friend_id,
            'access_token': TOKEN,
            'v': VERSION
        }

        response = get_user_groups(params)
        if response.get('error'):
            continue

        all_friend_groups = all_friend_groups | set(response['response']['items'])
        print('*******************************************************')
        #print(set(response['response']['items']))

    print('result: {}'.format(groups - all_friend_groups))


if __name__ == '__main__':
    main()
