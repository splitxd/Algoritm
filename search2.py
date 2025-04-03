import time
import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def get_random_substring(text, pattern_length):
    start_pos = random.randint(0, len(text) - pattern_length)
    return text[start_pos:start_pos + pattern_length]


def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    positions = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)
    return positions


def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0: return []

    bad_char = {pattern[i]: i for i in range(m)}

    positions = []
    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            positions.append(s)
            s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return positions


def rabin_karp_search(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    positions = []
    if m == 0 or m > n: return positions

    h = pow(d, m - 1) % q
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[s + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(s)

        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0: t += q
    return positions


def measure_time(search_func,length=100000, substring_length=100):
    total_time = 0
    err = 0
    for _ in range(10):
        text = generate_random_string(length)
        pattern = get_random_substring(text, substring_length)
        expected = [i for i in range(len(text)) if text.startswith(pattern, i)]
        start_time = time.time()
        result = search_func(text, pattern)
        if result != expected:
            err += 1
        end_time = time.time()
        total_time += (end_time - start_time)
    if err == 0:
        print(f"Поиск {search_func.__name__} завершен успешно.")
    else:
        print(f"Поиск {search_func.__name__} завершен с ошибкой.")
    return total_time / 10


print(f"ГАРАНТИРОВАННО ЧТО ПОДСТРОКА ЕСТЬ В ТЕКСТЕ!")

naive_time = measure_time(naive_search)
bm_time = measure_time(boyer_moore_search)
rk_time = measure_time(rabin_karp_search)


print(f"Простой поиск: {naive_time:.6f} сек")
print(f"Бойер-Мур: {bm_time:.6f} сек")
print(f"Рабин-Карп: {rk_time:.6f} сек")