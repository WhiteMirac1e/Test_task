# Создаем словарь для хранения ошибок и количества их вхождений
res_dct = {}


with open('test_log', 'r', encoding='utf-8') as file:
    for line in file:
        for i in line.split():
            if len(i) == 5:
                res_dct[i] = res_dct.get(i, 0) + 1
        result = dict(sorted(res_dct.items(), key=lambda x: -x[1]))
        for i, j in result.items():
            print(i, j, sep=' : ')




