from api.agreement.asset import Asset

Test = Asset.Group.Section.Course
file = 'test.json'


with open(file) as data:
    result = Test.model_validate_json(data.read())

    print(type(result))
    print(result)

    match(result):
        case Test():    print('Success!')
        case _:         print('Failure!')

    if isinstance(result, Test):    print("Success!")
    else:                           print('Failure!')