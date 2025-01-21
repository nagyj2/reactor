
from Entity import Entity


# @dataclass
class Thermal(Entity):
    transfer_coefficients = {}    # key is set of classes and value is matching coefficient
    dissipation_coefficients = {}  #

    @staticmethod
    def register_transfer_coefficient(t1, t2, k):
        Thermal.transfer_coefficients[frozenset((t1, t2))] = k

    @staticmethod
    def register_dissipation_coefficient(t1, k):
        Thermal.dissipation_coefficients[t1] = k

    def __init__(self, T, typ, min=None, max=None):
        super().__init__()
        self.T = T
        self.typ = typ
        self.min = min
        self.max = max

    def transfer(self, other, dt):
        K = Thermal.transfer_coefficients[frozenset((self.typ, other.typ))]

        # K = Q * d / (A * dT)
        self.T += K * 1 * (other.T - self.T) / 1 * dt
        # K	= 	thermal conductivity
        # Q	= 	amount of heat transferred
        # d	= 	distance between the two isothermal planes
        # A	= 	area of the surface
        # \Delta T	= 	difference in temperature

        if self.max is not None and self.T > self.max:
            self.T = self.max

    def dissipate(self, dt):
        self.T -= self.T * Thermal.dissipation_coefficients[self.typ] * dt

        if self.min is not None and self.T < self.min:
            self.T = self.min
