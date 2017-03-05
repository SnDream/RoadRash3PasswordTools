#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Road-Rash-3-Password-Tools.py
#
#  Copyright 2017 SnDream <xnight@outlook.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

CODE_RANGE = '0123456789ABCDEFGHIJKLMNOPQRSTUV '

TRACK_NAME = ['BRAZIL', 'GERMANY', 'KENYA', 'U.KINGDOM',
              'ITALY', 'AUSTRALIA', 'JAPAN']
LEVEL_TRACK = [[],
               [TRACK_NAME[0], TRACK_NAME[3], TRACK_NAME[1],
                TRACK_NAME[4], TRACK_NAME[2]],
               [TRACK_NAME[0], TRACK_NAME[3], TRACK_NAME[1],
                TRACK_NAME[4], TRACK_NAME[5]],
               [TRACK_NAME[0], TRACK_NAME[3], TRACK_NAME[1],
                TRACK_NAME[6], TRACK_NAME[5]],
               [TRACK_NAME[1], TRACK_NAME[2], TRACK_NAME[5],
                TRACK_NAME[4], TRACK_NAME[6]],
               [TRACK_NAME[0], TRACK_NAME[3], TRACK_NAME[4],
                TRACK_NAME[2], TRACK_NAME[6]]]

BIKE_NAME = [
    'PERRO 125', 'CORSAIR 400', 'KAMAKAZI 250', 'BANZAI 450',
    'RATZO 500', 'STILETTO 600', 'PERRO 250', 'PERRO 250',
    'DIABLO 750', 'DMG 1000', 'CORSAIR 600 N', 'KAMAKAZI 750 N',
    'BANZAI 750 1100', 'STILETTO 900 N', 'DIABLO 1000 N', 'WILD THING 2000']

UPGRADE_NAME = ['PERFORMANCE', 'PROTECTION', 'TIRES', 'SUSPENSION']

INPUT_HINT = [
    'Money    (0-655350): ',
    'Level         (1-5): ',
    'Track (00000-11110): ',
    'Bike         (0-15): ',
    'Upgrade (0000-1111): ',
    'Checksum1          : ',
    'Checksum2          : ',
    'Password(XXXX XXXX): ',
    'Tool Select   (1,2): ',
    'Vaild              : ',
    'Fixed Password     : ']


def main(args):
    try:
        print('1:Generator 2:Analyzer')
        action = input(INPUT_HINT[8])
        if action not in ['1', '2']:
            raise UserWarning('WRONG INPUT')
    except:
        exit(1)
    if action == '1':
        password_geneartor()
    elif action == '2':
        password_analyzer()
    return 0


def password_geneartor():
    try:
        money = int(input(INPUT_HINT[0])) // 10
        if money > 65535 or money < 0:
            raise UserWarning('MONEY ERROR')
    except:
        money = 0
        print(INPUT_HINT[0] + '0')
    try:
        level = int(input(INPUT_HINT[1]))
        if level > 5 or level < 1:
            raise UserWarning('LEVEL ERROR')
    except:
        level = 1
        print(INPUT_HINT[1] + '1')
    try:
        print('%-9s|%-9s|%-9s|%-9s|%-9s' % tuple(LEVEL_TRACK[level]))
        print('UNQUALIFIED:0  QUALIFIED:1')
        track = int(input(INPUT_HINT[2])[::-1], 2)
        if track >= 0b11111 or track < 0:
            raise UserWarning('TRACK ERROR')
    except:
        track = 0
        print(INPUT_HINT[2] + '00000')
    try:
        print('[RAT BIKES]    [SPORT BIKES]  [SUPER BIKES]     ')
        print('0:PERRO 125   |5:STILETTO 600|10:CORSAIR 600 N  ')
        print('1:CORSAIR 400 |6:PERRO 250   |11:KAMAKAZI 750 N ')
        print('2:KAMAKAZI 250|7:KAMAKAZI 750|12:BANZAI 750 1100')
        print('3:BANZAI 450  |8:DIABLO 750  |13:STILETTO 900 N ')
        print('4:RATZO 500   |9:DMG 1000    |14:DIABLO 1000 N  ')
        print('[HIDDEN BIKE] 15:WILD THING 2000')
        bike = int(input(INPUT_HINT[3]))
        if bike > 15 or level < 0:
            raise UserWarning('BIKE ERROR')
    except:
        bike = 0
        print(INPUT_HINT[3] + '0')
    try:
        print('PERFORMANCE|PROTECTION |TIRES      |SUSPENSION ')
        print('NOT UPGRADED:0  UPGRADED:1')
        upgrade = int(input(INPUT_HINT[4]), 2)
        if upgrade > 0b1111 or upgrade < 0:
            raise UserWarning('UPGRADE ERROR')
    except:
        upgrade = 0
        print(INPUT_HINT[4] + '0000')
    moneybin = [
        money & 0xF, (money >> 4) & 0xF, (money >> 8) & 0xF, (money >> 12) & 0xF]
    checksum1 = (moneybin[2] + moneybin[3] + bike) & 0b11
    password = []
    password.append((moneybin[0] << 1) | ((upgrade >> 3) & 1))
    password.append((moneybin[1] << 1) | ((upgrade) & 1))
    password.append((moneybin[2] << 1))
    password.append((moneybin[3] << 1) | ((checksum1) & 1))
    password.append(((upgrade << 2) & 0b11000) | level)
    password.append((bike << 1) | ((checksum1 >> 1) & 1))
    checksum2 = ((sum(password) ^ track) + 1) & 0b11111
    password.append(track)
    password.append(checksum2)
    passwordtext = ''
    for code in password:
        passwordtext += CODE_RANGE[code]
    print(INPUT_HINT[5] + str(checksum1))
    print(INPUT_HINT[6] + str(checksum2))
    print(INPUT_HINT[7] + passwordtext[:4] + ' ' + passwordtext[4:])


def password_analyzer():
    try:
        passwordtext = input(INPUT_HINT[7])
        password = []
        for code in passwordtext:
            if code == ' ':
                continue
            password.append(int(code, 32))
        if len(password) != 8:
            raise UserWarning('WRONG FORMAT')
    except:
        print('Wrong Format!')
        exit(1)
    if password[2] & 1 == 1:
        password[2] &= 0b11110
        valid = 'No'
    else:
        valid = 'Yes'
    money = ((password[0] >> 1) + ((password[1] >> 1) << 4) +
             ((password[2] >> 1) << 8) + ((password[3] >> 1) << 12)) * 10
    level = password[4] & 0b111
    if level > 5:
        level = 5
        password[4] = (password[4] & 0b11000) | 0b101
        valid = 'No'
    if level == 0:
        level = 1
        password[4] = (password[4] & 0b11000) | 0b001
        valid = 'No'
    if password[6] == 0b11111:
        password[6] = 0b11110
        valid = 'No'
    tracktext = ''
    for i in range(0, 5):
        if (password[6] >> i) & 1 == 1:
            tracktext += LEVEL_TRACK[level][i] + ' '
    bike = (password[5] >> 1) & 0b111
    upgrade = []
    upgradetext = ''
    upgrade.append((password[0]) & 1)
    upgrade.append((password[4] >> 4) & 1)
    upgrade.append((password[4] >> 3) & 1)
    upgrade.append((password[1]) & 1)
    for i in range(0, 4):
        if upgrade[i] == 1:
            upgradetext += UPGRADE_NAME[i] + ' '
    checksum1 = (((password[2] & 0b110) + (password[3] & 0b110) +
                  (password[5] & 0b110)) >> 1) & 0b11
    checksum1_2 = (password[3] & 1) | ((password[5] & 1) << 1)
    if checksum1 != checksum1_2:
        password[3] = (password[3] & 0b11110) | (checksum1 & 1)
        password[5] = (password[5] & 0b11110) | ((checksum1 >> 1) & 1)
        valid = 'No'
    checksum2 = ((sum(password[0:6]) ^ password[6]) + 1) & 0b11111
    checksum2_2 = password[7]
    if checksum2 != checksum2_2:
        password[7] = checksum2
        valid = 'No'
    print('%s%d' % (INPUT_HINT[0], money))
    print('%s%d' % (INPUT_HINT[1], level))
    print('%s%s' % (INPUT_HINT[2], tracktext))
    print('%s%s' % (INPUT_HINT[3], BIKE_NAME[bike]))
    print('%s%s' % (INPUT_HINT[4], upgradetext))
    print('%s%d (%d)' % (INPUT_HINT[5], checksum1_2, checksum1))
    print('%s%d (%d)' % (INPUT_HINT[6], checksum2_2, checksum2))
    print('%s%s' % (INPUT_HINT[9], valid))
    if valid is 'No':
        passwordtext = ''
        for code in password:
            passwordtext += CODE_RANGE[code]
        print(INPUT_HINT[10] + passwordtext[:4] + ' ' + passwordtext[4:])

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
