
import pytest

from entities import Emitter
from entities.component_emitter import ProbabilityEmitter, TimeEmitter
from geometry import Point, Vector

params_emitter_params = [
    (0, 0, 1, Vector(1, 1))
]


@pytest.mark.parametrize('x,y,n,vf', params_emitter_params)
def test_emitter_creation(x, y, n, vf):
    output = []
    emitter = Emitter(x, y, n, vf, output)

    assert emitter.origin == Point(x, y)
    assert emitter.output_lst is output
    assert emitter.emit_n == n
    assert emitter.emit_vec is vf


@pytest.mark.parametrize('x,y,n,vf', params_emitter_params)
def test_emitter_emit(x, y, n, vf):
    output = []
    emitter = Emitter(x, y, n, vf, output)

    emitter.emit()
    assert len(output) == n
    assert output[n-1].pos == Point(x, y)

    emitter.emit()
    assert len(output) == n * 2
    assert output[n*2-1].pos == Point(x, y)


@pytest.mark.parametrize('x,y,n,vf', params_emitter_params)
def test_probabilityemitter_creation(x, y, n, vf):
    output = []
    emitter = ProbabilityEmitter(x, y, n, vf, output, 0.5)

    iterations = 5
    o_len = 0
    for _ in range(iterations):
        emitter.update(1)
        emitted = len(output) - o_len
        assert emitted == 0 or emitted == n
        o_len = len(output)


@pytest.mark.parametrize('x,y,n,vf', params_emitter_params)
def test_timeemitter_creation(x, y, n, vf):
    output = []
    timeframe = 0.3
    emitter = TimeEmitter(x, y, n, vf, output, timeframe)

    iterations = 5
    dt = 1
    for i in range(iterations):
        emitter.update(dt)
        assert len(output) == 0 + (i+1)*dt // timeframe
