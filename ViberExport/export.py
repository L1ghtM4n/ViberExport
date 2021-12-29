#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ['Main']

# Import modules
from sys import argv
from os import path, mkdir
# Import packages
from core.extractor import ViberExtractor


def Main() -> int:
    # Author
    print('[?] Coded by github.com/L1ghtM4n')
    # Require db path
    if len(argv) != 2:
        db = input('[?] Please provide viber.db location: ')
    else:
        db = argv[1]
    # Check if db exists
    if not path.exists(db):
        exit('[X] Database file not found!')
    # Initialyze extractor
    extractor = ViberExtractor(db)
    # Create export directory
    if not path.exists('export'):
        mkdir('export')
    # Export all chats with contacts
    for contact in extractor.contacts:
        print('[?] Exporting chats from {user} with phone {phone}'.format(user=contact['user'], phone=contact['phone']))
        with open('export\\{phone}.txt'.format(phone=contact['phone']), 'w', encoding='utf-8') as out:
            for message in contact['messages']():
                data = '< {sender} | {phone} | {date} >\n {message}\n\n'.format(
                    sender=message['user'],
                    phone=message['phone'],
                    date=message['date'].strftime("%d/%m/%Y, %H:%M:%S"),
                    message=message['message']
                )
                out.write(data)
    # Export all group chats
    for group in extractor.groups:
        print('[?] Exporting group {name}'.format(name=group['name']))
        with open('export\\{name}.txt'.format(name=group['name']), 'w', encoding='utf-8') as out:
            for message in group['messages']():
                data = '< {sender} | {phone} | {date} >\n {message}\n\n'.format(
                    sender=message['user'],
                    phone=message['phone'],
                    date=message['date'].strftime("%d/%m/%Y, %H:%M:%S"),
                    message=message['message']
                )
                out.write(data)

    return 0


if __name__ == '__main__':
    exit(code=Main())
