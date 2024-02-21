def naming(columnId: str, columnName: str, targetTable):
    print(targetTable.loc[columnId][columnName])