'''

Program is the combo of multiple algo's
which provide the best utilization of their
spaces in a hotels as per the client requirements

It is a POC of the bigger problem statements

'''

__author__ = "ankit's Team"

import sys
import pprint, json
from itertools import combinations

graph_dict, area_with_size = {}, {}

#----------------------------------
# Algo to find the adjacent element
# in matrix
#----------------------------------
def adjacent(rw, cl):
    new_lst = []

    if rw - 1 >= 0:
        new_lst.append(str(rw-1) + str(cl))
    if rw + 1 < len(H_airlifts):
        new_lst.append(str(rw+1) + str(cl))
    if cl - 1 >= 0:
        new_lst.append(str(rw) + str(cl-1))
    if cl + 1 < len(V_airlifts):
        new_lst.append(str(rw) + str(cl+1))

    graph_dict[str(rw)+str(cl)] = new_lst

#-------------------------------------------------
# Problem statement: 1 - Validate all combinations
#-------------------------------------------------
def validation(lst):
    for values in lst:
        if len(values) == 1:
            for i in values:
                area_with_size[json.dumps(values)] = areas[int(i[0])][int(i[1])]
        else:
            nw_lst = []
            sum = 0
            values = list(values)
            values.sort()
            flag = True
            nw_lst.append(values[0])
            for i in nw_lst:
                for val in graph_dict[i]:
                    if val in values and val not in nw_lst:
                        nw_lst.append(val)

            if sorted(nw_lst) == sorted(values):
                res_list.append((nw_lst))
                for i in nw_lst:
                    sum += areas[int(i[0])][int(i[1])]
                area_with_size[json.dumps(nw_lst)] = sum

#--------------------------------------
# Problem statement: 2 - allocate space
#--------------------------------------
def allocate_space(area):
    total_area = area_with_size.copy()
    answer = min(x for x in total_area.values() if x >= area)
    for name, res_area in total_area.items():
        if res_area == answer:
            print 'The allocated area: ', name
            name = json.loads(name)
            for val in name:
               areas[int(val[0])][int(val[1])] = 'Allocated'
            break

H_airlifts, V_airlifts  = [], []
rows, areas, res_list = [], [], []

handle = open("dataset.csv",'r')
for dataset in handle.readlines():
    data = dataset.split(',')
    Height = int(data[0])
    Width = int(data[1])
    hor_arlft = int(data[2])
    ver_arlft = int(data[2+hor_arlft+1])

    for airliftSizes in range(1, hor_arlft + 1):
        H_airlifts.append(int(data[2 + airliftSizes]))

    for airliftSizes in range(2 + hor_arlft+2, len(data)):
        V_airlifts.append(int(data[airliftSizes]))

    H_airlifts.append(Height - sum(H_airlifts))
    V_airlifts.append(Width - sum(V_airlifts))

    mtrx_size = len(H_airlifts) * len(V_airlifts)

    for H_airlift in H_airlifts:
       for V_airlift in V_airlifts:
          rows.append(H_airlift * V_airlift)
       areas.append(rows)
       rows = []

    print "All roomlet Areas: ", areas

    for i in range(len(H_airlifts)):
        for j in range(len((V_airlifts))):
           adjacent(i,j)

    print "---------- Finding all adjacent elements -----------"
    #print "All adjacent elements: "
    #pprint.pprint(graph_dict)

    dum = 0
    for i in range(1, mtrx_size + 1):
        last_list = [subset for subset in combinations(list(graph_dict.keys()), i)]
        dum += len(last_list)
        validation(last_list)

    print "All possible combinations :", len(res_list)
    #pprint.pprint(res_list)

    print "---------- Finding all possible combinations with Area -----------"
    #print ("All possible combinations with Area :")
    #pprint.pprint(area_with_size)

handle.close()

inputRequest = raw_input("Do you want the best Allocation of complete space ? (Y|N) ")
if inputRequest == 'Y':
    area = input('For how much area ? ')
    allocate_space(area)
    print 'This is what we assign to the required space: ', 
    pprint.pprint(areas)
else:
    pass

print "\nThanks for using event Management tool"
sys.exit(0)
