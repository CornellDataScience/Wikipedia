def retrieve_all(list, i):
    s = []
    for rows in list:
        s.append(rows[i])
    return s


def calculate_times(word, list):
    i = 0
    for rows in list:
        for item in rows:
            if (item == word):
                i += 1
    return i

def process_list(data, n):
    mylist = []
    for i in range(len(data[0])):
        if i <= n:
            innerlist = []
            base = retrieve_all(data, i)
            if i >= 1:
                list(filter((data[0][0]).__ne__, base))
            d = {}
            for b in base:
                d[b] = calculate_times(b, data)
            sorted_dict = sorted(d, key=d.get, reverse=True)[:(i+1)]

            for j in range(len(sorted_dict)):
                innerlist.append(sorted_dict[j])
            mylist.append(innerlist)
        else:
            return mylist
    return mylist


def generate_json(lst,acc):
    # for i in rang(len(list)):
    if lst==[]:
        return
    else:
        dic = {}
        dic["name"]= str(acc)
        dic["children"]=[{"name":i, "size":10} for i in lst[0]]
        dic["children"] = dic["children"] + [generate_json(lst[1:],acc+1)]
        return dic
