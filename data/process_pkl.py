from cmath import pi
from email.mime import base
import pickle
import pandas as pd
from pandas import Series,DataFrame
import math
import time
import numpy as np
import random


# d is the constraints of start and ends
def gen_weight(d, type_list, L):
    weights = [[0 for k in type_list] for i in type_list]
    for i in range(len(type_list)):
        for j in range(len(type_list)):
            if j >= i:
                wij = check_weight(d, type_list[i], type_list[j], L)
                weights[i][j] = wij
                weights[j][i] = wij
            # if i == j:
            #     weights[i][j] = base_weight
            # if j > i:
            #     wij = check_weight(d, type_list[i], type_list[j], L)
            #     if wij > 0:
            #         wij += base_weight
            #     weights[i][j] = wij
            #     weights[j][i] = wij       
    # print(weights)
    return weights

def distance(u, v):
    return abs(u[0]-v[0])+abs(u[1]-v[1])

def check_weight(d, a, b, L):
    # print(a, b)
    a_start = [a[0]//L, a[0]%L]
    a_end = [a[1]//L, a[1]%L]
    b_start = [b[0]//L, b[0]%L]
    b_end = [b[1]//L, b[1]%L]
    if distance(a_start, b_start) > d or distance(a_end, b_end) > d:
        return 0
    else:
        route1 = distance(a_start, b_start) + distance(b_start, a_end) + distance(a_end, b_end)
        route2 = distance(b_start, a_start) + distance(a_start, a_end) + distance(a_end, b_end)
        route3 = distance(b_start, a_start) + distance(a_start, b_end) + distance(b_end, a_end)
        route4 = distance(a_start, b_start) + distance(b_start, b_end) + distance(b_end, a_end)
        return min(route1, route2, route3, route4)
    # print(a_start_x, a_start_y, a_end_x, a_end_y)

def cal_rate_bound(pickup, dropoff, L, d):
    x1_list = []
    y1_list = []
    pick_list = []
    drop_list = []
    M = L*L
    for i in range(len(pickup)):
        [x,y] = pickup[i]
        if x < -73 and x > -75 and y < 42 and y > 40:
            pick_list.append([-x, y])
            x1_list.append(-x)
            y1_list.append(y)
        [x,y] = dropoff[i]
        if x < -73 and x > -75 and y < 42 and y > 40:
            drop_list.append([-x, y])
            x1_list.append(-x)
            y1_list.append(y)
            

    minx = np.mean(x1_list)-3*np.std(x1_list, ddof=1)
    maxx = np.mean(x1_list)+3*np.std(x1_list, ddof=1)
    # print(t_list)
    # minx = min(x1_list)
    # maxx = max(x1_list)
    print(minx, maxx)
    dx = (maxx-minx)/L

    miny = np.mean(y1_list)-3*np.std(y1_list, ddof=1)
    maxy = np.mean(y1_list)+3*np.std(y1_list, ddof=1)
    print(miny, maxy)
    dy = (maxy-miny)/L

    pick = [[math.floor((x[0]-minx)/dx), math.floor((x[1]-miny)/dy)] for x in pick_list]
    drop = [[math.floor((x[0]-minx)/dx), math.floor((x[1]-miny)/dy)] for x in drop_list]

    Ntrips = min(len(pick), len(drop))
    pick = pick[0: Ntrips]
    drop = drop[0: Ntrips]

    new_pick = []
    old_pick = []
    for i in range(len(pick)):
        # if pick[i][0]>=L or pick[i][0]<0 or pick[i][1] >= L or pick[i][0]<0
        for j in range(2):
            if pick[i][j] >= L:
                pick[i][j] = L-1
            if pick[i][j] < 0:
                pick[i][j] = 0
            if drop[i][j] >= L:
                drop[i][j] = L-1
            if drop[i][j] < 0:
                drop[i][j] = 0
    M = L*L
    pick_single = []
    drop_single = []
    count_table = [[0 for j in range(M)] for i in range(M)]
    count = 0
    # print(count_table)
    for i in range(len(pick)):
        pick_point = pick[i][0]*L+pick[i][1]
        drop_point = drop[i][0]*L+drop[i][1]
        pick_single.append(pick_point)
        drop_single.append(drop_point)
        # print(pick[i], drop[i])
        # a = [pick_point, drop_point]
        # b = [pick_point, drop_point]
        # check_weight(3, a, b, L)
        count_table[pick_point][drop_point] += 1
        # count += 1
    # print(count_table)
    type_list = []
    min_count = 30
    count_list = []
    for i in range(M):
        for j in range(M):
            if count_table[i][j] >= min_count:
                type_list.append([i, j])
                count_list.append(count_table[i][j])
                # rates.append(count_table[i][j]/count)
    count = sum(count_list)
    rates = [c/count for c in count_list]
    print(count)
    print('type number', len(rates))
    weights = gen_weight(d, type_list, L)
    deg = [0 for i in weights]
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if weights[i][j] > 0:
                deg[i] += 1
    print('avg deg', sum(deg)/len(deg))
    print('max deg', max(deg), 'min deg', min(deg))
    save_data(rates, weights, L, d, len(rates))
    return

def save_data(rates, weights, L, d, type_number):
    filename = 'nyc_'+str(L)+'_'+str(d)+'_'+str(type_number)
    with open(filename, 'w') as f:
        f.write(' '.join([str(i) for i in rates])+'\n')
        for i in range(len(weights)):
            f.write(' '.join([str(j) for j in weights[i]])+'\n')
# with open('rate', 'w') as f:
#     f.write(' '.join([str(i) for i in rate]))

# with open('nyc', 'w') as f:
#     for i in range(1000):
#         f.write(str(t_list[i])+' '+str(cali_x[i]*L+cali_y[i])+'\n')
# print(x1_list)


# minmax r:73.776657, 74.126198, 40.641136, 40.853745

# def gen_arrivals():
#     r_minmax = [73.636093, 74.370033, 40.291973, 41.202354]
#     d_minmax = [73.500938, 74.622017, 40.289955, 41.32531]
#     for i in range(20):

    


if __name__ == '__main__':
    infile = open('taxi_csv1_1.pkl','rb')
    new_dict = pickle.load(infile)
    L = 20
    d = 2
    print(new_dict.columns)
    #print(x1_list)
    #print(y1_list)

    pickup = new_dict.head(200000)['pickup_coordinates']
    dropoff = new_dict.head(200000)['dropoff_coordinates']
    # pickt = new_dict.head(200000)[' pickup_datetime']
    # dropt = new_dict.head(200000)[' dropoff_datetime']
    # print(pickt[0], pickt[100000])
    # print(pickup)
    cal_rate_bound(pickup, dropoff, L, d)
    infile.close()


