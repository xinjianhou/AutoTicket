#!/usr/bin/python3
# coding=utf-8

import sqlite3


# db = pymysql.connect("localhost", "root", "Root@123", "AUTO_TEST")
# cursor = db.cursor()
# cursor.execute('create table TEST_CONFIG(ID INT NOT NULL AUTO_INCREMENT,'
#                ' PARAM VARCHAR(30) NOT NULL, VALUE VARCHAR(100) NOT NULL, PRIMARY KEY (ID))')
#
# #data = cursor.fetchone()
# #print(data)
#
# db.close()


class DBUtil():

    def __init__(self):

        self.__DATA_BASE__ = "/Users/xinjianhou/PycharmProjects/automationtest/data/automation.sqlite"

        connect = sqlite3.connect(self.__DATA_BASE__)
        cursor = connect.cursor()

        try:
            cursor.execute('drop table if exists TEST_CONFIG')
            cursor.execute('create table TEST_CONFIG(ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'

                           'PARAM VARCHAR(30) NOT NULL, VALUE VARCHAR(100) NOT NULL)')

            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("BROWSER", "SAFARI")')
            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("URL", "https://www.12306.cn/index/")')

        except TabError as error:
            print('error occurs' + str(error))
        except sqlite3.OperationalError as error:
            print('error occurs' + str(error))
        finally:
            connect.commit()
            connect.close()

    def __getData__(self, types):

        connect = sqlite3.connect(self.__DATA_BASE__)
        cursor = connect.cursor()
        data = ''
        try:
            data = cursor.execute('SELECT VALUE FROM TEST_CONFIG WHERE PARAM = "{0}"'.format(types)).fetchone()[0]
        except TabError as error:
            print('error occurs {0}'.format(error))
        finally:
            connect.commit()
            connect.close()
        return data

    def getBrowser(self):
        return self.__getData__('BROWSER')

    def getURL(self):
        return self.__getData__('URL')

    def getOrigin(self):
        return self.__getData__('ORIGIN')

    def getDes(self):
        return self.__getData__('DESTINATION')

    def getDate(self):
        return self.__getData__('TRAVEL_DATE')

    def getTime(self):
        return self.__getData__('TRAVEL_TIME')

    def getUserName(self):
        return self.__getData__('USERNAME')

    def getPassword(self):
        return self.__getData__('PASSWORD')

    def count(self):
        connect = sqlite3.connect(self.__DATA_BASE__)
        cursor = connect.cursor()
        data = ''
        try:
            data = cursor.execute('SELECT count(1) FROM TEST_CONFIG').fetchone()[0]
        except TabError as error:
            print('error occurs {0}'.format(error))
        finally:
            connect.commit()
            connect.close()
        return data


    def setUser(self, name, password):
        connect = sqlite3.connect(self.__DATA_BASE__)
        cursor = connect.cursor()

        try:

            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("USERNAME", "{0}")'.format(name))
            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("PASSWORD", "{0}")'.format(password))

        except TabError as error:
            print('error occurs:' + str(error))
        except sqlite3.OperationalError as error:
            print('error occurs:' + str(error))
        finally:
            connect.commit()
            connect.close()

    def setTiket(self, origin, destination, travel_date, travel_time):
        connect = sqlite3.connect(self.__DATA_BASE__)
        cursor = connect.cursor()

        try:

            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("ORIGIN", "{0}")'.format(origin))
            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("DESTINATION", "{0}")'.format(destination))
            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("TRAVEL_DATE", "{0}")'.format(travel_date))
            cursor.execute('INSERT INTO TEST_CONFIG(PARAM, VALUE) VALUES("TRAVEL_TIME", "{0}")'.format(travel_time))

        except TabError as error:
            print('error occurs:' + str(error))
        except sqlite3.OperationalError as error:
            print('error occurs:' + str(error))
        finally:
            connect.commit()
            connect.close()
