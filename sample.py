import random

id = []
# with open("/storage/miniapp/wechat/index.list", 'r') as l:
#     for line in l:
#         # print(line.split('/')[-1].split('.')[0])
#         # exit()
#         id.append(line.split('/')[-1].split('.')[0])

name_id = []
with open('fingerprinting_name_miniapps_id.txt', 'r') as l:
    for line in l:
        name_id.append(line)

string_id = []
with open('fingerprinting_string_miniapps_id.txt', 'r') as l:
    for line in l:
        string_id.append(line)

fw1 = open("sample_name", "w")
for i in random.sample(name_id, 30):
    fw1.write(i)
    # fw1.write('\n')

fw2 = open("sample_string", "w")
for i in random.sample(string_id, 20):
    fw2.write(i)
    # fw2.write('\n')

