dic = {0:"zero", 1:"one", 2:"two", None:None}
print(dic)
for num in dic:
    print(num)

    if num is None:
        dic[num] = 3

print(dic)

x = (1, 2)
y = (30, 40)

print(x + y)
run = True
x= 0
while run:
    msg = ""
    print("cool", msg)
    if x == 5:
        msg = "hi"
        run = False
    x+=1