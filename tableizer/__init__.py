#!/usr/bin/env python
__author__ = 'mahieke'

__version__ = '0.0.3'

from collections import deque

class Tableizer():
    def __init__(self, width):
        '''
        A simple tool for creating an ascii table.

        :raise TypeError: types of the parameters must be correct
        :raise ValueError: the list must be of size of the specific column length
        '''
        if not isinstance(width,int):
            raise TypeError('Width attribute must be of type int')

        self.__width = width
        self.__layout = ''
        self.__table = []
        self.__styleList = deque()

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

    def next_layout(self, layout):
        '''
        Layout for the next columns:

        :param layout: layout for table (list) with integers which define the length of a column
        '''
        if not isinstance(layout, list):
            raise TypeError('second parameter "layout" must be a list')

        if not all(isinstance(item, int) for item in layout):
            raise TypeError('elements of second parameter must be of type int')

        self.__cols = len(layout)

        if sum(layout) + self.__cols - 1 > self.__width:
            self.__cols = 0
            raise Exception('The given layout must fit in the row length of ' + str(self.__width) + ' chars.')

        self.__layout = layout
        self.__layout_str = '{:' + '} {:'.join(str(s) for s in layout) + '}'
        self.__seperator = list(' '*self.__cols)


    def add_row(self, content, style=None):
        '''
        Adds a row to the table. This row must have :__cols columns.

        :param content: list with content for each column or empty string for a newline
        :return: None
        '''
        if not isinstance(content, list):
            raise TypeError('"content" parameter must be a list')

        self.__check_layout()

        if len(content) != self.__cols:
            raise ValueError('"content" parameter must have {} elements'.format(self.__cols))

        self.__add_row(content, style)


    def add_seperator(self, style=None):
        self.__check_layout()
        if style:
            self.__styleList.append(style)
        else:
            self.__styleList.append('')

        self.__table.append(self.__layout_str.format(*self.__seperator))


    def add_rrow(self, content, style=None):
        '''
        Adds a row with less columns than :__cols aligned to the right of the table

        :param content: list with content each column or a string for one column
        :return: None
        '''
        if not isinstance(content, list):
            raise TypeError('"content" parameter must be a list')

        self.__check_layout()

        if isinstance(content, list) and len(content) >= self.__cols:
            raise ValueError('"content" parameter must have less elements than {}'.format(self.__cols))

        to_add = deque()
        to_add.extend(content)
        to_add.extendleft(' '*(self.__cols - len(to_add)))
        self.__add_row(list(to_add), style)


    def add_lrow(self, content, style=None):
        '''
        Adds a row with less columns than :__cols aligned to the left of the table

        :param content: list with content each column
        :return: None
        '''
        if not isinstance(content, list):
            raise TypeError('"content" parameter must be a list')

        self.__check_layout()

        if isinstance(content, list) and len(content) >= self.__cols:
            raise ValueError('"content" parameter must have less elements than ' + self.__cols)

        to_add = deque()
        to_add.extend(content)
        to_add.extend(' '*(self.__cols - len(to_add)))
        self.__add_row(list(to_add), style)


    def print_table(self):
        '''
        Prints the whole table with its style components
        :return: None
        '''
        for row in self.__table:
            print(self.__styleList[0] + row)
            self.__styleList.rotate(-1)


    def __add_row(self, content, style=None):
        '''
        Adds a row for a table
        :param content: list with content for each row
        :return: None
        '''
        u_content = [str(element) for element in content]
        entries = self.__tableize(u_content)

        for i in range(len(entries)):
            if style:
                self.__styleList.append(style)
            else:
                self.__styleList.append('')

        self.__table.extend(entries)


    def __tableize(self, content):
        '''
        Divides cols which are longer than defined into several rows

        :param content: list with content for each row
        :return: divided rows for content
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

        return [self.__layout_str.format(*[y.strip() for y in x]) for x in outp]


    def __check_layout(self):
        if self.__layout == '':
            raise AttributeError('No layout was set.')