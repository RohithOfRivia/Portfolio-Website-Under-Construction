projects = [
    {"name": "test", "desc": "bla bla bla"},
    {"name": "dsv", "desc": "sdzg bla bla"}
]


for dict in projects:
    print([(key, item) for (key, item) in dict.items()])


