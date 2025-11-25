def test_add_two():
    x = 1
    y = 2
    assert x + y ==  new_func()

def new_func():
    return 3

def test_dict_contains():
    x  = {"a":1,"b":2}

    expected = {"a":1}

    assert expected.items() <= x.items()