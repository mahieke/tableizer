__author__ = 'mahieke'

__version__ = '0.0.2'

class Tableizer():
    def __init__(self,cols,layout):
        """

        :param cols: columns of table
        :param layout: layout for table (list) with integers which define the length of a column
        :raise TypeError: types of the parameters must be correct
        :raise ValueError: the list must be of size of the specific column length
        """

        if isinstance(cols, int):
            raise TypeError('first parameter "cols" must be int')
        if isinstance(layout, list):
            raise TypeError('second parameter "layout" must be a list')
        if len(layout.split) != cols:
            raise ValueError('layout must specify {} columns'.format(cols))
        if all(isinstance(item, int) for item in layout):
            raise TypeError('elements of second parameter must be of type int')

        self.__layout = '{:' + '} {:'.join(layout) + '}'
        self.__cols = cols
        self.__table = []

    @property
    def layout(self):
        return self.__layout

    @property
    def cols(self):
        return self.__cols

    def add_row(self, content):
        if isinstance(content, list):
            raise TypeError('"content" parameter must be a list')

        if len(list) > self.__cols:
            raise ValueError('"content" parameter must have less or equal number of elements than ' + self.__cols)

        self.__table.append(content)


    def print_table(self):
        for row in self.__table:
            print(self.__layout.format(*row))