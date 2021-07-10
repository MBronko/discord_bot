def convert_default(_type=int, default=0):
    def conv(value):
        try:
            return _type(value)
        except ValueError:
            return default

    return conv
