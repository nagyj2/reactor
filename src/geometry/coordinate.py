
# todo:
# disallow bool
# rename coordinate to something akin to a protected value

class Coordinate:
    '''Handles a 1D coordinate point.'''
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        try:
            instance.__dict__[self._name] = float(value)
            return
        except ValueError:
            raise TypeError(f'\'{self._name}\' must be a number')
