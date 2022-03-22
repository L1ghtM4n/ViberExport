#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ['ViberExtractor']

# Import modules
from sqlite3 import connect
from typing import Iterable
from datetime import datetime


# Viber messages extractor class
class ViberExtractor:
    '''
        >>> Viber database is located at path:
        >>> C:/Users/<User>/AppData/Roaming/ViberPC/<Phone>/viber.db
    '''
    def __init__(self, db: str) -> None:
        self.connection = connect(db)
        self.cursor = self.connection.cursor()

    @property
    def groups(self) -> Iterable[dict]:
        # Prepare sql query
        sql = (' SELECT DISTINCT ChatID, Name' 
               ' FROM ChatInfo'
               ' WHERE Token IS NOT NULL;')
        # Execute sql and fetch data
        for row in self.cursor.execute(sql).fetchall():
            yield dict(
                chat=row[0],
                name=row[1] if row[1] else 'Group_{id}'.format(id=row[0]),
                messages=lambda : self.__dump_messages(row[0])
            )

    @property
    def contacts(self) -> Iterable[dict]:
        # Prepare sql query
        sql = (' SELECT DISTINCT ChatRelation.ChatID, Contact.Number, Contact.Name, Contact.ClientName, DateOfBirth' 
               ' FROM Contact'
               ' INNER JOIN ChatRelation ON ChatRelation.ContactID = Contact.ContactID'
               ' WHERE (Contact.Name IS NOT NULL OR Contact.ClientName IS NOT NULL)')
        for g in self.groups:
            sql += ' AND ChatRelation.ChatID != {chat}'.format(chat=g['chat'])
        sql += ';'
        # Execute sql and fetch data
        for row in self.cursor.execute(sql).fetchall():
            yield dict(
                chat=row[0],
                user=(row[2] if row[2] else row[3])[1:-1],
                phone=int(row[1][1:] if row[1] else 0),
                dateOfBirth=row[4] if row[4] else 'Unknown',
                messages=lambda : self.__dump_messages(row[0])
            )

    def __dump_messages(self, chat_id: int) -> Iterable[dict]:
        # Prepare sql query
        sql = (
            ' SELECT Contact.Name, Contact.ClientName, Contact.Number, MessageInfo.Body, MessageInfo.TimeStamp'
            ' FROM ChatInfo'
            ' INNER JOIN MessageInfo ON ChatInfo.ChatID = MessageInfo.ChatID'
            ' INNER JOIN Contact ON Contact.ContactID = MessageInfo.ContactID'
            ' WHERE MessageInfo.Body IS NOT NULL AND MessageInfo.ChatID = {chat_id}'.format(chat_id=chat_id) +
            ' ORDER BY MessageInfo.TimeStamp;'
        )
        # Execute sql and fetch data
        for row in self.cursor.execute(sql).fetchall():
            yield dict(
                date=datetime.fromtimestamp(row[4] / 1000),
                user=str((row[0] if row[0] else row[1]))[1:-1],
                phone=row[2][1:] if row[2] else 0,
                message=row[3]
            )
