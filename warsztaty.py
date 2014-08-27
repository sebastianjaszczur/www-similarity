#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import pandas as pd

df = pd.read_csv('www10.csv', delimiter='\t', header=None, encoding="utf8")

tab = []

ALL_USERS = 57

result_json = dict(nodes=[], links=[])

for ind in xrange(len(df)):
    subdata = list(df.irow(ind))

    warsztaty_type = subdata[0]
    oid = len(tab)
    block = subdata[1]
    name = subdata[2]
    scores = map(int, subdata[3:])
    print scores
    tab.append(dict(id=oid, name=name, scores=scores, type=warsztaty_type,
                    block=block))

    result_json['nodes'].append(dict(name=name, block=block))

for ind1, obj in enumerate(tab):
    result_json['nodes'][ind1]['users'] = obj['scores'][ind1]
    result_json['nodes'][ind1]['type'] = obj['type']
    for ind2, common_users in enumerate(obj['scores']):
        if ind2 >= ind1:
            break
        if common_users > 0:
            prob = (float(common_users) * ALL_USERS /
                    (tab[ind1]['scores'][ind1] * tab[ind2]['scores'][ind2])) - 1
            result_json['links'].append(dict(source=ind1, target=ind2,
                                             value=prob, common_users=common_users))


json.dump(result_json, open("miserables.json", "w"), indent=2)
