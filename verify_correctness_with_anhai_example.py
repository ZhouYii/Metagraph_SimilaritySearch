# coding=utf-8

import numpy as np
import build_hin
import metapath_operations as mp

file = open("out", "w")
target = "AnHai Doan"
#target = "Yuri Breitbart"
p_a, p_p, p_v, a_p, v_p, a_v = build_hin.start()

'''
    Calculate metapath score between target and other authors.
'''
m1, v_i = mp.seed_matrix_AV(target, a_p, a_v, p_v)
m2, p_i = mp.matrix_VP(v_i, v_p)
m3, a_i = mp.matrix_PA(p_i, p_a)

p1 = np.dot(m1, m2)
p2 = np.dot(p1, m3)

'''
    Generate score from self-to-self
'''
t_t = mp.self_APVPA(target, a_v, p_v, a_p)
file.write("self_score : " +str(t_t) + "\n")

candidates = ["AnHai Doan", "Jignesh M. Patel", "Amol Deshpande", "Jun Yang", \
                "Renée J. Miller", "Jiawei Han", "Philip S. Yu", \
                "Gerhard Weikum", "Samuel DeFazio", "Adam Silberstein"]

for c in candidates :
    if not a_i.has_key(c) :
        continue

    c_c = mp.self_APVPA(c, a_v, p_v, a_p)
    t_c = p2[0, a_i[c]]
    file.write(c + " c-c score:" + str(c_c) + " t-c score:"+str(t_c) + \
            " pathsim score:" + str( 2*float(t_c) / (float(c_c) + t_t)))

    file.write("\n")
file.close()
