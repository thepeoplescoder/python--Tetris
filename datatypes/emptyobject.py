# A class for empty objects that can be updated on the fly.
class EmptyObject(object):
    # __init__ ############################################
    def __init__(self, *args, **kwargs):
        if args:
            EmptyObject.field_copy(self, args[0])
        EmptyObject.field_copy(self, kwargs)
    # field_copy ##########################################
    @staticmethod
    def field_copy(dest, src):
        if not isinstance(src, dict):
            src = vars(src)
        for key, value in src.items():
            setattr(dest, key, value)
    # __repr__ ############################################
    def __repr__(self):
        s = ["<EmptyObject[",]
        entries = vars(self)
        if entries:
            for key, value in entries.items():
                s.append('(')
                s.append(repr(key))
                s.append(", ")
                s.append(repr(value))
                s.append(')')
                s.append(", ")
            s.pop()
        s.append("] at ")
        s.append(hex(id(self)))
        s.append('>')
        return "".join(s)