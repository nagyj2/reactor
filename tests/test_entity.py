from copy import copy, deepcopy

import pytest

from Entity import Entity
from Settings import init_settings

init_settings(default=True)


class TestEntity(Entity):  # test class to be copyable, comparable and contains state
    def __init__(self, init=1):
        super().__init__()
        self.state = init

    def __eq__(self, other):
        if isinstance(other, TestEntity):
            return self.state == other.state
        return False

    def update(self, dt):
        self.state += dt


params_entity_manual_identical_repr = [
    ((2, '3', 2.0), ((2, '3', 2.0))),
    ((Entity(),), (Entity(),)),
    ((TestEntity(5),), (TestEntity(5),)),
]

params_entity_copyable_repr = [
    (Entity(),),
    (TestEntity(),),
    (TestEntity(5), TestEntity(1)),
]


def test_entity_value():
    e = Entity()
    assert e.repr == []
    assert len(e.repr) == 0


def test_vector_str():
    assert str(Entity()) == 'Entity()'


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_add(r1):
    e1 = Entity()
    assert e1.repr == []
    c = 0
    for e in r1:
        e1.add(e)
        c += 1
        assert e in e1.repr
        assert len(e1.repr) == c


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_remove(r1):
    e1 = Entity()
    assert e1.repr == []
    e1.repr = [e for e in r1]
    c = len(r1)
    for e in r1:
        e1.remove(e)
        c -= 1
        assert e not in e1.repr
    assert len(e.repr) == c


def test_entity_remove_all():
    e1 = Entity()
    assert e1.repr == []
    rep = [TestEntity(), TestEntity(), TestEntity()]
    e1.repr = deepcopy(rep)
    assert len(e1.repr) == 3
    e1.remove_all(TestEntity)
    assert len(e1.repr) == 0


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_has(r1):
    e1 = Entity()
    e1.repr = r1
    for e in r1:
        assert e1.has(type(e))


def test_entity_empty_eq():
    e = Entity()
    assert e == e


@pytest.mark.parametrize('r1,r2', params_entity_manual_identical_repr)
def test_entity_junk_eq(r1, r2):
    e1 = Entity()
    e1.repr = r1
    assert e1 == e1


def test_entity_empty_ne():
    e1 = Entity()
    e2 = Entity()
    assert e1 != e2


@pytest.mark.parametrize('r1', [
    ((2, '3', 2.0)),
    ((2, '3', 2.0)),
    ((Entity(),)),
    ((TestEntity(1),)),
])
def test_entity_junk_ne(r1):
    e1 = Entity()
    e2 = Entity()
    e1.repr = r1
    e2.repr = r1
    assert e1 != e2

    e2 = Entity()
    new_rep = [2, '3', 2.0, object()]
    e2.repr = new_rep
    assert e1 != e2


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_copy(r1):
    e1 = Entity()
    e2 = copy(e1)
    for e in e1.repr:
        assert type(e) in e2.repr
    for e in e2.repr:
        assert type(e) in e1.repr

    e1.repr.extend(r1)  # repr is aliased
    for e in e1.repr:
        assert type(e) in e2.repr
    for e in e2.repr:
        assert type(e) in e1.repr


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_deepcopy(r1):
    e1 = Entity()
    e2 = deepcopy(e1)
    assert e1 != e2


@pytest.mark.parametrize('r1', params_entity_copyable_repr)
def test_entity_deepcopy_ne(r1):
    e1 = Entity()
    e2 = deepcopy(e1)
    for e in e1.repr:
        assert type(e) in e2.repr
    for e in e2.repr:
        assert type(e) in e1.repr

    e1.repr.extend(r1)  # repr is aliased
    assert r1 not in e2.repr


def test_entity_update():
    e1 = Entity()
    e2 = Entity()
    e2.id = e1.id
    e1.update(1)
    assert e1 == e2


def test_entity_prepare():
    e1 = Entity()
    e2 = Entity()
    e2.id = e1.id
    e1.prepare()
    assert e1 == e2


def test_entity_enable():
    e = Entity()
    e.repr = [TestEntity()]
    e_copy = deepcopy(e)
    e_copy.id = e.id
    assert e == e_copy

    e.enable = False
    e.update(5)
    assert e == e_copy
