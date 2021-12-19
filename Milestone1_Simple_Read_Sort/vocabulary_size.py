dict = {}
with open('tweets.txt','r') as file:
    lines = file.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            if word not in dict:
                dict[word] = 1
            else:
                dict[word] += 1
count = 0
for word in dict:
    if dict[word] == 1:
        count += 1
print(count)
