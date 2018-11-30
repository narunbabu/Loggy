import numpy as np
def str_array2floats(strarray):
    floats=[]
    for s in strarray:
        try:
            floats.append(float(s))
        except:
            floats.append(s)
    return np.array(floats)
def find_keyIndxWithStr(log,string):
    found=False
    indx=-999
    for i,key in enumerate(log.keys()):
        if string in key:
            found=True
            indx=i
            break
    
    return found,indx
def find_depth_indx(log):
    found,indx=find_keyIndxWithStr(log,'DEPT')
    if not found:
        found,indx=find_keyIndxWithStr(log,'TVD')
    if not found:
        print('Depth collumn not found with existing tokens. Refine token in find_depth_indx function...')
    return indx

# log=las[0]
def find_prop_indexes(log):
    propindxs=[]
    for i,key in enumerate(log.keys()):
        if (key not in ['TIME', 'DATE']) & ('DEPT' not in key):
#             print(log.curves[i].data)
            propindxs.append(i)
    return np.array(propindxs)