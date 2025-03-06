dic = {0:"zero", 1:"one", 2:"two", None:None}
print(dic)
for num in dic:
    print(num)

    if num is None:
        dic[num] = 3

print(dic)