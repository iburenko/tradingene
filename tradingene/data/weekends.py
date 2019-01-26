from datetime import datetime

days_off = [
    datetime(2017, 1, 1),
    datetime(2017, 1, 2),
    datetime(2017, 1, 7),
    datetime(2017, 1, 8),
    datetime(2017, 2, 23),
    datetime(2017, 3, 8),
    datetime(2017, 5, 1),
    datetime(2017, 5, 8),
    datetime(2017, 5, 9),
    datetime(2017, 6, 12),
    datetime(2017, 11, 6),
    datetime(2018, 1, 1),
    datetime(2018, 1, 2),
    datetime(2018, 1, 8),
    datetime(2018, 2, 23),
    datetime(2018, 3, 8),
    datetime(2018, 5, 1),
    datetime(2018, 5, 9),
    datetime(2018, 6, 12),
    datetime(2018, 11, 5),
    datetime(2018, 12, 31),
    datetime(2019, 1, 1),
    datetime(2019, 1, 2),
    datetime(2019, 1, 7),
    datetime(2019, 3, 8),
    datetime(2019, 5, 1),
    datetime(2019, 5, 9),
    datetime(2019, 6, 12),
    datetime(2019, 11, 4)
    ]

no_evening_session = [datetime(2017, 12, 29)]

# from 19.05:
#     datetime(2017, 1, 18
#     datetime(2017, 1, 19
#     datetime(2017, 1, 26
#     datetime(2017, 2, 9
#     datetime(2017, 2, 15
#     datetime(2017, 2, 16
#     datetime(2017, 2, 22
#     datetime(2017, 2, 24
#     datetime(2017, 3, 2
#     datetime(2017, 3, 9
#     datetime(2017, 3, 15
#     datetime(2017, 3, 16
#     datetime(2017, 3, 23
#     datetime(2017, 3, 28
#     datetime(2017, 3, 30
#     datetime(2017, 4, 6
#     datetime(2017, 4, 13
#     datetime(2017, 4, 19
#     datetime(2017, 4, 20
#     datetime(2017, 4, 25
#     datetime(2017, 4, 27
#     datetime(2017, 5, 4
#     datetime(2017, 5, 11
#     datetime(2017, 5, 17
#     datetime(2017, 5, 18
#     datetime(2017, 5, 25
#     datetime(2017, 6, 1
#     datetime(2017, 6, 8
#     datetime(2017, 6, 14
#     datetime(2017, 6, 15
#     datetime(2017, 6, 22
#     datetime(2017, 6, 27
#     datetime(2017, 6, 29
#     datetime(2017, 7, 6
#     datetime(2017, 7, 13
#     datetime(2017, 7, 19
#     datetime(2017, 7, 20
#     datetime(2017, 7, 26
#     datetime(2017, 7, 27
#     datetime(2017, 8, 3
#     datetime(2017, 8, 10
#     datetime(2017, 8, 16
#     datetime(2017, 8, 17
#     datetime(2017, 8, 24
#     datetime(2017, 8, 25
#     datetime(2017, 8, 31
#     datetime(2017, 9, 7
#     datetime(2017, 9, 14
#     datetime(2017, 9, 20
#     datetime(2017, 9, 21
#     datetime(2017, 9, 26
#     datetime(2017, 9, 28
#     datetime(2017, 10, 5
#     datetime(2017, 10, 12
#     datetime(2017, 10, 18
#     datetime(2017, 10, 19
#     datetime(2017, 10, 26
#     datetime(2017, 11, 2
#     datetime(2017, 11, 9
#     datetime(2017, 11, 15
#     datetime(2017, 11, 16
#     datetime(2017, 11, 23
#     datetime(2017, 11, 27
#     datetime(2017, 11, 30
#     datetime(2017, 12, 7
#     datetime(2017, 12, 14
#     datetime(2017, 12, 20
#     datetime(2017, 12, 21,
#     datetime(2017, 12, 28
#     datetime(2018, 1, 11
#     datetime(2018, 1, 17
#     datetime(2018, 1, 18
#     datetime(2018, 1, 25
#     datetime(2018, 1, 26
#     datetime(2018, 2, 1
#     datetime(2018, 2, 8
#     datetime(2018, 2, 14
#     datetime(2018, 2, 15
#     datetime(2018, 2, 22
#     datetime(2018, 2, 26
#     datetime(2018, 3, 1
#     datetime(2018, 3, 7
#     datetime(2018, 3, 14
#     datetime(2018, 3, 15
#     datetime(2018, 3, 22
#     datetime(2018, 3, 26
#     datetime(2018, 3, 29
#     datetime(2018, 4, 5
#     datetime(2018, 4, 12
#     datetime(2018, 4, 18
#     datetime(2018, 4, 19
#     datetime(2018, 4, 25
#     datetime(2018, 4, 26
#     datetime(2018, 5, 3
#     datetime(2018, 5, 10
#     datetime(2018, 5, 16
#     datetime(2018, 5, 17
#     datetime(2018, 5, 24
#     datetime(2018, 5, 25
#     datetime(2018, 5, 31
#     datetime(2018, 6, 7
#     datetime(2018, 6, 14
#     datetime(2018, 6, 15
#     datetime(2018, 6, 20
#     datetime(2018, 6, 21
#     datetime(2018, 6, 26
#     datetime(2018, 6, 28
#     datetime(2018, 7, 5
#     datetime(2018, 7, 12
#     datetime(2018, 7, 18
#     datetime(2018, 7, 19
#     datetime(2018, 7, 25
#     datetime(2018, 7, 26
#     datetime(2018, 8, 2
#     datetime(2018, 8, 9
#     datetime(2018, 8, 15
#     datetime(2018, 8, 16
#     datetime(2018, 8, 23
#     datetime(2018, 8, 28
#     datetime(2018, 8, 30
#     datetime(2018, 9, 6
#     datetime(2018, 9, 13
#     datetime(2018, 9, 17
#     datetime(2018, 9, 19
#     datetime(2018, 9
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018
#     datetime(2018