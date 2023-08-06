import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore


import numpy as np
from . import colfilters
from . import newtable
from .filteredtablemodel import FilteredTableModel

class SuperTableWidget(QtWidget.QDialog):
    def __init__(self, df, num=1000, parent=None):
        QtWidget.QMainWindow.__init__(self, parent)
        self.df = df
        self.ncol = len(df.columns)
        self.max_width  = 1000

        self.collection = create_filter_collection(df)
        self.collection.changed.connect(self.updateFilters)

        self.tableModel = FilteredTableModel(df)
        self.tableView = QtWidget.QTableView()
        self.tableView.setModel(self.tableModel)
        self.tableView.setSortingEnabled(True)
        # self.tableView.setHorizontalHeaderLabels(df.columns)
        self.tableView.resizeColumnsToContents()
        
        # self.table = newtable.TableWidget(df, num=num)
        layout = QtWidget.QVBoxLayout()
        layout.addWidget(self.collection)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        self.show()

    def updateFilters(self):
        idx = self.collection.getFilteredIn()
        # print("In Supertable.updateFilters: ", np.sum(idx), " of ", len(idx))
        self.tableModel.setFiltered(idx)

    def toggleColumn(self, sender_label, state):
        #cols = self.table.df.columns
        cols = self.tableModel.getColumns()
        for i in range(self.ncol):
            if cols[i] == sender_label:
                if state:
                    self.tableView.showColumn(i)
                    self.collection.showColumn(i)
                else:
                    self.tableView.hideColumn(i)
                    self.collection.hideColumn(i)

    def showAll(self):
        for i in range(self.ncol):
            self.table.showColumn(i)
            self.collection.showColumn(i)

    def hideAll(self):
        for i in range(self.ncol):
            self.table.hideColumn(i)
            self.collection.hideColumn(i)


    def set_size_policy(self):
        tv = self.tableView
        width_pix = tv.horizontalHeader().length() + tv.verticalHeader().width() + 20
        height_pix = tv.verticalHeader().length() + tv.horizontalHeader().width()
        tv.setMaximumSize(width_pix, height_pix)
        self.max_width = width_pix

        width_pix = min(width_pix, 1000)
        height_pix = min(height_pix, 1000)
        self.resize(width_pix, height_pix)

    def getMaxWidth(self):
        return self.max_width




def create_filter_collection(df):
    cols = df.columns

    filter_list = []
    for c in cols:
        filter_list.append(create_column_filter(df, c))
        # print(c, filter_list[-1])

    collection = colfilters.FilterCollection(filter_list)
    return collection


def create_column_filter(df, c):
    # import pdb; pdb.set_trace()
    col = df[c]
    num_values = len(set(col))
    if num_values < 10:
        return colfilters.CategoricalFilter(col)

    # idebug()
    dtype = col.dtype
    if dtype == np.dtype('int') or dtype == np.dtype('float'):
        return colfilters.NumericFilter(col)
    elif isinstance(dtype, object):
        return colfilters.StringFilter(col)
