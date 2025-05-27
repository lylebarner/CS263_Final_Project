t = int(input())
for _ in range(t):
    n = int(input())
    words = []
    word_set = set()
    for _ in range(n):
        w = input()
        words.append(w)
        word_set.add(w)

    idx_by_type = {'01': [], '10': []}
    count_type = {'00': 0, '11': 0, '01': 0, '10': 0}

    for i, w in enumerate(words):
        t = w[0] + w[-1]
        count_type[t] += 1
        if t in ('01', '10'):
            idx_by_type[t].append(i)

    # Edge case: only '00' and '11' exist, and no '01' or '10' to start the chain
    if count_type['01'] == 0 and count_type['10'] == 0:
        if count_type['00'] > 0 and count_type['11'] > 0:
            print(-1)
            continue
        else:
            print(0)
            continue

    # Try to balance '01' and '10'
    diff = abs(count_type['01'] - count_type['10']) // 2
    from_type = '01' if count_type['01'] > count_type['10'] else '10'
    reversed_indices = []

    for i in idx_by_type[from_type]:
        rev = words[i][::-1]
        if rev not in word_set:
            reversed_indices.append(i + 1)  # 1-based indexing
            if len(reversed_indices) == diff:
                break

    if len(reversed_indices) < diff:
        print(-1)
    else:
        print(len(reversed_indices))
        if reversed_indices:
            print(' '.join(map(str, reversed_indices)))

