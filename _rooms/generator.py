import random, string

def randtext(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def uniqueid(n, wcount, head=''):
    return [head + randtext(wcount) + str(i+1).zfill(2) for i in range(n)]

fd_list = uniqueid(33, 3, 'fd')
sd_list = uniqueid(33, 3, 'sd')
dg_list = uniqueid(33, 3, 'dg')

with open('_rooms/socio.txt', 'w') as f:
    for x in fd_list:
        f.write(f"{x}\n")
    for x in sd_list:
        f.write(f"{x}\n")
    for x in dg_list:
        f.write(f"{x}\n")