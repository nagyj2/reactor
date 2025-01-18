
# import abc
from copy import deepcopy

# Todo:
# add entity disable and corresponding toggle
# optimize __eq__?
# implement __del__


class Entity:
    '''Base class for a drawn entity.'''
    # __metaclass__ = abc.ABCMeta

    # Note:
    # Subclasses should not implement __iter__ because it can cause confusion when adding to self.repr

    def __init__(self):
        self.repr = []
        self.enable = True
        self.alive = True

    def __str__(self):
        return f'{type(self).__name__}()'

    def __eq__(self, other):
        if isinstance(other, Entity):
            if len(self.repr) != len(other.repr):
                return False
            for my_obj in self.repr:
                found = False
                for their_obj in other.repr:
                    if my_obj == their_obj:
                        found = True
                if not found:
                    return False
            return True
        return False

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    # @abc.abstractmethod  # require this function to be overwritten
    def _update(self, dt):
        '''Apply update logic'''
        for entity in self.repr:
            entity.update(dt)

    def update(self, dt):
        '''Apply update logic if enabled'''
        if self.enable and self.alive:
            # Can run any mandatory stuffs, like base class super()._update()
            self._update(dt)

    def _prepare(self):
        '''Prepares entity for next update.'''
        for entity in self.repr:
            entity.prepare()

    def prepare(self):
        '''Prepare for the next update if enabled'''
        if self.alive:
            if self.enable:
                self._prepare()
        else:
            self._kill()

    def _kill(self):
        '''Prepare entity for garbage collection'''
        pass

    def add(self, entity):
        self.repr.append(entity)

    def _remove(self, entity):
        found = False
        for e in self.repr:
            found = found or e._remove(entity)
        if entity in self.repr:
            self.repr.remove(entity)
            found = True
        return found

    def remove(self, entity):
        found = self._remove(entity)
        # del entity  # ensure it is killed to prevent stale references
        return found

    def remove_all(self, typ):
        c_len = len(self.repr)
        self.repr = list(filter(lambda e: type(e) is not typ, self.repr))
        return len(self.repr) != c_len
        # o_len = -1
        # found = False
        # while o_len != c_len:  # if 2 back to back runs are same length, no more typ in self.repr
        #     o_len = c_len
        #     for e in self.repr:
        #         if type(e) is typ:
        #             found = found or self.remove(e)
        #             break
        #     c_len = len(self.repr)
        # return found

    def has(self, typ):
        for e in self.repr:
            if type(e) is typ:
                return True
        return False

    def kill(self, dt=0):  # dt to allow pyuglet to schedule it
        self.alive = False
