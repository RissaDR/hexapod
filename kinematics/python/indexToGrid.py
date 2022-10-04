def indexToColumn(index, scope):
    column = index // scope
    return column

def indexToRow(index, scope):
    row = index % scope
    return row

def rowColumnToIndex(row, column, scope):
    index = row * scope + column
    return index

for i in range(9):
    print(i, "\t", indexToColumn(i, 3), indexToRow(i, 3))