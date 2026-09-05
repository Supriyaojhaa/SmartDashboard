def data_generator(data):
    for row in data:
        yield row


def multiplier(factor):

    def inner(value):
        return value * factor

    return inner