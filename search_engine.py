def build_bmh_table(pattern: str) -> dict:
    m = len(pattern)
    table = {c: m for c in map(chr, range(256))}
    for i in range(m - 1):
        table[pattern[i]] = m - 1 - i
    return table

def bmh_search(text: str, pattern: str) -> list:
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    table = build_bmh_table(pattern)
    hits = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            hits.append(i)
            i += m
        else:
            c = text[i + m - 1]
            i += table.get(c, m)
    return hits