import numpy as np

d = list()

for x in range(1,15):
    for y in range(1,15):
        d.append((x,y))

d_cube=list()

for c in d:
    d_cube.append((c[0],c[1],-c[0]-c[1]))

print('len_d', len(d))
print('len_d_cube', len(d_cube))

uniq_d = np.unique(d)
uniq_d_cube = np.unique(d_cube)

print('uniq len_d', len(uniq_d))
print('uniq len_d_cube', len(uniq_d_cube))

print(uniq_d)
print(uniq_d_cube)