import pandas as pd

global df
df = False
useOneHot = False

def getExtn(fPath):
    idx = fPath.rfind(".")
    return fPath[idx + 1:]

def openDataset(fPath):
    data = fPath
    ext = getExtn(fPath)
    if ext == "csv":
        data = pd.read_csv(fPath)
    elif ext == "xlsx":
        data = pd.read_excel(fPath)
    else:
        print("The slected file format is not supported.")
    global df
    df = data

def findNans(df):
    return df.columns[df.isna().any()].tolist()

openDataset(str(input("Enter the file path: ")))

dataType = int(input("Does the data contain string values? (y/n) "))

if dataType == y:
    useOneHot = True

nIn = int(input("How many columns are to be taken as the input? "))
nOut = int(input("How many columns are to be taken as the output? "))

