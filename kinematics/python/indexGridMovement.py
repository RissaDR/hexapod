def indexToColumn(index, scope):
    column = index // scope
    return column

def indexToRow(index, scope):
    row = index % scope
    return row

def rowColumnToIndex(row, column, scope):
    index = row * scope + column
    return index

def canMoveIndex(i_from, i_to, scope):
    i_fromRow = indexToRow(i_from, scope)
    i_fromColumn = indexToColumn(i_from, scope)
    i_toRow = indexToRow(i_to, scope)
    i_toColumn = indexToColumn(i_to, scope)
    print(i_fromColumn, i_fromRow)
    print(i_toColumn, i_toRow)

    # only row or column is different; not both, or none

    if (i_fromRow == i_toRow and i_fromColumn == i_fromColumn):
        return False
    elif (i_fromRow != i_toRow and i_fromColumn != i_fromColumn):
        return False
    
    # difference between either rows or columns respectively is 1 but not both or none

    if (abs(i_fromRow - i_toRow) == 1 and abs(i_fromColumn - i_fromColumn) == 1):
        return False
    if (abs(i_fromRow - i_toRow) != 1 and abs(i_fromColumn - i_fromColumn) != 1):
        return False

    # movement is within scope

    if (i_toRow > scope or i_toColumn > scope):
        return False
    
    return True

    # if (i_fromRow == i_toRow or i_fromColumn == i_fromColumn):
    #     print("same row/column")
    #     if (abs(i_fromRow - i_toRow) == 1 or abs(i_fromColumn - i_fromColumn) == 1):
    #        print("only moves one")
    #         if (i_toRow < scope or i_toColumn < scope):
    #             print("within scope")
    #             return True
    # return False

print(canMoveIndex(0,4,3))