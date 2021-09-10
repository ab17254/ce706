# list(set(sys1).intersection(set(sys2)))

class Queries:
    q1_rel = ['x53t9i4k', 'k1hwh640', 'nhb4o6ty', 'hkc4vbmj', 'dcjwfes7', 'baugu1gh', 'mxjtj5c0', 't6l692zu',
              '31q7ftnd']
    q1_sys1 = ['bjjft7ut', 'x53t9i4k', 'sbnnh2mm', 'tloaa3v1', 'jzwcy7dr', 'k1hwh640', 'nhb4o6ty', 'hkc4vbmj',
               'dcjwfes7', 'baugu1gh']
    q1_sys2 = ['x53t9i4k', 'bjjft7ut', 'nhb4o6ti', 'mxjtj5c0', 't6l692zu', '6d9x0xbj', '31q7ftnd', 'sbnnh2mm',
               'dcjwfes7', 'hkc4vbmj']
    q2_rel = ['ttyo4z6f', 't7004uw2', '2mfbqs8i', '31q7ftnd', 'crjwej14', '5b936n3g', 'fite9vs8', 'h3yxymh3',
              '9fr0m92p', '36dhfptw']
    q2_sys1 = ['ttyo4z6f', 't7004uw2', '2mfbqs8i', '31q7ftnd', 'crjwej14', '5b936n3g', 'fite9vs8', 'h3yxymh3',
               '9fr0m92p', '36dhfptw']
    q2_sys2 = ['t7004uw2', 'ttyo4z6f', '31q7ftnd', 'crjwej14', '2mfbqs8i', '5b936n3g', 'h3yxymh3', '36dhfptw',
               'fite9vs8', '2ad1tu4']
    q3_rel = ['7vhcf929', 'hwlvk68z', 'ntx35a8s', 'v9k7vpi8']
    q3_sys1 = ['hwlvk68z', 'ntx35a8s', 'v9k7vpi8']
    q3_sys2 = ['hwlvk68z', 'ntx35a8s', 'v9k7vpi8']


def pk(actual, pred, k=5):
    k_pred = set(pred[:k])
    actual = set(actual)
    correct = len(k_pred & actual)
    p = correct / float(k)
    return p


def rk(actual, pred, k=5):
    matches = len(set(pred[:5]) & set(actual))
    if matches == 0:
        return 0
    return float(matches) / len(actual)


if __name__ == "__main__":
    data = Queries
    print('PK')
    print('Q1 Sys1: ' + str(pk(data.q1_rel, data.q1_sys1)))
    print('Q1 Sys2: ' + str(pk(data.q1_rel, data.q1_sys2)))
    print('\nRK')
    print('Q1 Sys1: ' + str(rk(data.q1_rel, data.q1_sys1)))
    print('Q1 Sys2: ' + str(rk(data.q1_rel, data.q1_sys2)))

    print('\n\nPK')
    print('Q2 Sys1: ' + str(pk(data.q2_rel, data.q2_sys1)))
    print('Q2 Sys2: ' + str(pk(data.q2_rel, data.q2_sys2)))
    print('\nRK')
    print('Q2 Sys1: ' + str(rk(data.q2_rel, data.q2_sys1)))
    print('Q2 Sys2: ' + str(rk(data.q2_rel, data.q2_sys2)))

    print('\n\nPK')
    print('Q3 Sys1: ' + str(pk(data.q3_rel, data.q3_sys1)))
    print('Q3 Sys2: ' + str(pk(data.q3_rel, data.q3_sys2)))
    print('\nRK')
    print('Q3 Sys1: ' + str(rk(data.q3_rel, data.q3_sys1)))
    print('Q3 Sys2: ' + str(rk(data.q3_rel, data.q3_sys2)))

