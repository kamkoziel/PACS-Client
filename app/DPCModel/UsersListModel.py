from __future__ import unicode_literals

from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

tick = QtGui.QImage('res/img/icons/activeUsr_32.png')

class UsersListModel(QAbstractListModel):
    def __init__(self, fields=[], data=[], parent=None):
        super(UsersListModel, self).__init__()
        self.fields = fields
        self.data = data
        self.max_length=self._col_width()

    def update(self, data):
        self.data = data
        self.max_length = self._col_width()

    def rowCount(self, parent=QModelIndex()):
        """ Zwraca ilość wierszy """
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        """ Zwraca ilość kolumn """
        if self.data:
            return len(self.data[0])
        else:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        """ Wyświetlanie danych """
        i = index.row()
        j = index.column()

        if role == Qt.DisplayRole:
            if self.data[i][4]:
                return '{0}{1}{2}{3}{4}{5}'.format(self.data[i][1], " " * (self.max_length - len(str(self.data[i][1]))),
                                                  self.data[i][2], " " * (self.max_length - len(str(self.data[i][2]))),
                                                  self.data[i][3], " " * (self.max_length - len(str(self.data[i][3]))))
            else:
                return '        {0}{1}{2}{3}{4}{5}'.format(self.data[i][1], " " * (self.max_length - len(str(self.data[i][1]))),
                                           self.data[i][2], " " * (self.max_length - len(str(self.data[i][2]))),
                                           self.data[i][3], " " * (self.max_length - len(str(self.data[i][3]))))
        if role == Qt.DecorationRole:
            if self.data[i][4]:
                return tick
        else:
            return QVariant()

    def _col_width(self):
        col_width = 0
        data = self.data
        for row in zip(data):
            for col in row:
                for el in col:
                    if len(str(el)) > col_width:
                        col_width = len(str(el))

        return col_width+5