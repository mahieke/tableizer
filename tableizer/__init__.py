#!/usr/bin/env python
__author__ = 'mahieke'

__version__ = '0.0.1'

from collections import deque

class Tableizer():
    def __init__(self,cols,layout):
        '''
        A simple tool for creating an ascii table.

        :param cols: columns of table
        :param layout: layout for table (list) with integers which define the length of a column
        :raise TypeError: types of the parameters must be correct
        :raise ValueError: the list must be of size of the specific column length
        '''
        if not isinstance(cols, int):
            raise TypeError('first parameter "cols" must be int')
        if not isinstance(layout, list):
            raise TypeError('second parameter "layout" must be a list')
        if len(layout) != cols:
            raise ValueError('layout must specify {} columns'.format(cols))
        if not all(isinstance(item, int) for item in layout):
            raise TypeError('elements of second parameter must be of type int')

        self.__layout = layout
        self.__layout_str = u'{:' + '} {:'.join(str(s) for s in layout) + '}'
        self.__cols = cols
        self.__seperator = list(' '*cols)
        self.__table = []

    @property
    def layout(self):
        '''

        :return: layout string for table columns
        '''
        return self.__layout

    @property
    def cols(self):
        '''


        :return: number of columns of the table
        '''
        return self.__cols


    def add_row(self,content=None):
        '''
        Adds a row to the table. This row must have :__cols columns.

        :param content: list with content for each column or empty string for a newline
        :return: None
        '''
        if not isinstance(content, list) and content != None:
            raise TypeError('"content" parameter must be a list')

        if content != None and len(content) != self.__cols:
            raise ValueError('"content" parameter must have {} elements'.format(self.__cols))

        if content == None:
            content = list(' '*(self.__cols))

        self.__add_row(content)


    def add_rrow(self, content):
        '''
        Adds a row with less columns than :__cols aligned to the right of the table

        :param content: list with content each column or a string for one column
        :return: None
        '''
        if not isinstance(content, list) and not isinstance(content, str):
            raise TypeError('"content" parameter must be a list')

        if isinstance(content, list) and len(content) >= self.__cols:
            raise ValueError('"content" parameter must have less elements than {}'.format(self.__cols))

        to_add = deque()
        if isinstance(content, str):
            to_add.append(content)
        else:
            to_add.extend(content)

        to_add.extendleft(' '*(self.__cols - len(to_add)))
        self.__add_row(list(to_add))


    def add_lrow(self, content):
        '''
        Adds a row with less columns than :__cols aligned to the left of the table

        :param content: list with content each column
        :return: None
        '''
        if not isinstance(content, list) and not isinstance(content, str):
            raise TypeError('"content" parameter must be a list')

        if isinstance(content, list) and len(content) >= self.__cols:
            raise ValueError('"content" parameter must have less elements than ' + self.__cols)

        to_add = deque()
        if isinstance(content, str):
            to_add.append(content)
        else:
            to_add.extend(content)

        to_add.extend(' '*(self.__cols - len(to_add)))
        self.__add_row(list(to_add))


    def __add_row(self, content):
        '''
        Adds a row for a table
        :param content: list with content for each row
        :return: None
        '''
        u_content= [element.decode('UTF-8') for element in content]
        entries = self.__tableize(u_content)
        self.__table.extend(entries)


    def __tableize(self, content):
        '''
        rows which are longer than defined into several rows

        :param content:
        :return:
        '''

        layout = deque(self.__layout[:])
        outp = deque()
        to_parse = deque(content)
        for k in range(len(to_parse)):
            width = layout.popleft()
            inp = to_parse.popleft().split()
            i = 0
            j = 0
            while j < len(inp):
                if i >= len(outp):
                    # add a new row
                    outp.append(deque())
                    outp[i].extend(' '*(len(content)))


                if len(outp[i][k].strip()) + len(inp[j]) < width:
                    word = inp[j] + ' '
                    outp[i][k] += word
                    j += 1
                elif len(outp[i][k].strip()) == 0:
                    word = inp[j][:width-1] + '-'
                    outp[i][k] += word
                    inp[j] = inp[j][width-1:]
                    i += 1
                else:
                    i += 1

        return map(lambda x:map(lambda y:y.strip(),x),outp)



    def print_table(self):
        for row in self.__table:
            print(self.__layout_str.format(*row))
