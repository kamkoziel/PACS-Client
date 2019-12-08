from __future__ import unicode_literals

from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QAbstractTableModel

class PacsItemModel(QAbstractTableModel):
    def __init__(self, fields=[], data=[], parent=None):
        super(PacsItemModel, self).__init__()
        self.fields = fields
        self.data = data

    def update(self, data):
        self.data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        if self.data:
            return len(self.data[0])
        else:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        i = index.row()
        j = index.column()

        if role == Qt.DisplayRole:
            return '{0}'.format(self.data[i][j])
        else:
            return QVariant()

    def flags(self, index):
        """ Zwraca właściwości kolumn tabeli """
        flags = super(PacsItemModel, self).flags(index)
        j = index.column()

        return flags

    def setData(self, index, value, role=Qt.DisplayRole):
        """ Zmiana danych """
        i = index.row()
        j = index.column()
        if role == Qt.EditRole:
            self.data[i][j] = value

        return True

    def headerData(self, section, direct, role=Qt.DisplayRole):
        """ Zwraca nagłówki kolumn """
        if role == Qt.DisplayRole and direct == Qt.Horizontal:
            return self.fields[section]
        elif role == Qt.DisplayRole and direct == Qt.Vertical:
            return section + 1
        else:
            return QVariant()