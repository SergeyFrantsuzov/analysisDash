import pandas as pd
import os


def create_dataframe(path):
    """Create Pandas DataFrame from local CSV."""

    fileList = os.listdir(path)

    nameArray = ['RCAL', 'CP', 'FF', 'RI']
    existDfArrayNames = []
    existDfArray = []
    for i in nameArray:
        locals()["path" + i + "Index"] = [j for j, e in enumerate(fileList)
                                          if e.endswith('_' + i + '.csv') == True]
        if len(eval("path" + i + "Index")) > 0:
            locals()['df_' + i.lower()] = pd.read_csv(path + "\\" + fileList[eval("path" + i + "Index")[0]], sep=';',
                                                      header=0) # возможно стоит немного переделать загрузку данных с with open( ) as f: ...

            existDfArrayNames.append(i)
            existDfArray.append(eval('df_' + i.lower()))

    return existDfArrayNames, existDfArray

# pathData = os.getcwd() + "\\" + "data"
# dfNames, df = create_dataframe(pathData)
# print(pathData)
# print(dfNames.index('CP'))
