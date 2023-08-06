import pytest
import logging
import numpy as np

from mumott import Geometry
from mumott.data_handling.geometry import GeometryTuple


tuple_list = [GeometryTuple(rotation=np.eye(3), j_offset=0.3, k_offset=0.7),
              GeometryTuple(rotation=np.eye(3) * 0.732, j_offset=0.3, k_offset=0.7),
              GeometryTuple(rotation=-np.eye(3), j_offset=0.3, k_offset=0.7)]

rotation_array = np.array([[[0.955336, 0.190379, 0.226026],
                           [0., 0.764842, -0.644218],
                           [-0.2955, 0.615445, 0.730682]],
                          [[0.955336, 0.190379, 0.226026],
                           [0., 0.764842, -0.644218],
                           [-0.29552, 0.615445, 0.730682]]])

rotation_list = [np.array([[0.955336, 0.190379, 0.226026],
                          [0., 0.764842, -0.644218],
                          [-0.2955, 0.615445, 0.730682]]),
                 np.array([[0.955336, 0.190379, 0.226026],
                          [0., 0.764842, -0.644218],
                          [-0.29552, 0.615445, 0.730682]])]

expected_rotated_array = [
    np.array([[[-0.190379, 0.955336, 0.226026],
               [-0.764842, 0., -0.644218],
               [-0.615445, -0.2955, 0.730682]],
              [[-0.190379, 0.955336, 0.226026],
               [-0.764842, 0., -0.644218],
               [-0.615445, -0.29552, 0.730682]]])]

j_list = [0.7, 0.8, 0.4]
k_list = [0.3, 0.5, 0.1]

j_array = np.array([2.1, -1, 0.2322])
k_array = np.array([2.1, -1, 0.2322])


@pytest.mark.parametrize('test_list', [(tuple_list)])
def test_input_output(test_list, tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'test.geo'
    g = Geometry()
    for t in tuple_list:
        g.append(t)
    for a, b in zip(g, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    g.write(p)
    k = Geometry()
    k.read(p)
    for a, b in zip(k, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    assert hash(k) == hash(g)
    m = Geometry(p)
    for a, b in zip(m, tuple_list):
        assert np.allclose(a.rotation, b.rotation)
        assert np.isclose(a.j_offset, b.j_offset)
        assert np.isclose(a.k_offset, b.k_offset)
    assert hash(g) == hash(m)

    # test that deleting works after loading
    del k[-1]
    del m[-1]


@pytest.mark.parametrize('test_array,expected_array', [(rotation_array, expected_rotated_array)])
def test_reconstruction_rotation(test_array, expected_array, caplog):
    caplog.set_level(logging.INFO)
    g = Geometry()
    g.rotations = test_array
    recon_rot = np.array([[0, 1., 0], [-1., 0., 0.], [0., 0., 1.]])
    g.rotate_reconstruction(recon_rot)
    print(g.rotations)
    assert np.allclose(expected_rotated_array, g.rotations)

    assert np.allclose(g.reconstruction_rotations, recon_rot)

    g = Geometry()
    g.rotations = test_array
    recon_rotvec = np.array([0, 0, 1.])
    recon_rotangle = -np.pi/2
    g.rotate_reconstruction(axis=recon_rotvec, angle=recon_rotangle)
    assert np.allclose(expected_rotated_array, g.rotations)

    assert np.allclose(g.reconstruction_rotations, recon_rot)

    g.write('test.geo')
    k = Geometry('test.geo')
    assert np.allclose(k.rotations, g.rotations)

    with pytest.raises(ValueError, match='Cannot modify rotations'):
        g.rotations = test_array

    assert 'axis and/or angle' not in caplog.text

    g.rotate_reconstruction(recon_rot, axis=recon_rotvec, angle=recon_rotangle)

    assert 'axis and/or angle' in caplog.text


def test_system_rotation(caplog):
    caplog.set_level(logging.INFO)
    g = Geometry()
    system_rot = np.array([[0, 1., 0], [-1., 0., 0.], [0., 0., 1.]])
    g.rotate_system_vectors(system_rot)
    assert np.allclose(np.array((1, 0, 0)), g.p_direction_0)
    assert np.allclose(np.array((0, -1, 0)), g.j_direction_0)
    assert np.allclose(np.array((0, 0, 1)), g.k_direction_0)
    assert np.allclose(np.array((0, -1, 0)), g.detector_direction_origin)
    assert np.allclose(np.array((0, 0, 1)), g.detector_direction_positive_90)

    assert np.allclose(g.system_rotations, system_rot)

    g = Geometry()
    system_rotvec = np.array([0, 0, 1.])
    system_rotangle = -np.pi/2
    g.rotate_system_vectors(axis=system_rotvec, angle=system_rotangle)
    assert np.allclose(np.array((1, 0, 0)), g.p_direction_0)
    assert np.allclose(np.array((0, -1, 0)), g.j_direction_0)
    assert np.allclose(np.array((0, 0, 1)), g.k_direction_0)
    assert np.allclose(np.array((0, -1, 0)), g.detector_direction_origin)
    assert np.allclose(np.array((0, 0, 1)), g.detector_direction_positive_90)

    assert np.allclose(g.system_rotations, system_rot)

    g.write('test.geo')
    k = Geometry('test.geo')
    assert np.allclose(k.p_direction_0, g.p_direction_0)
    assert np.allclose(k.j_direction_0, g.j_direction_0)
    assert np.allclose(k.k_direction_0, g.k_direction_0)
    assert np.allclose(k.detector_direction_origin, g.detector_direction_origin)
    assert np.allclose(k.detector_direction_positive_90, g.detector_direction_positive_90)

    with pytest.raises(ValueError, match='Cannot modify system vectors'):
        g.p_direction_0 = np.array((0, 0, 1))

    with pytest.raises(ValueError, match='Cannot modify system vectors'):
        g.j_direction_0 = np.array((0, 0, 1))

    with pytest.raises(ValueError, match='Cannot modify system vectors'):
        g.k_direction_0 = np.array((0, 0, 1))

    with pytest.raises(ValueError, match='Cannot modify system vectors'):
        g.detector_direction_origin = np.array((0, 0, 1))

    with pytest.raises(ValueError, match='Cannot modify system vectors'):
        g.detector_direction_positive_90 = np.array((0, 0, 1))

    assert 'axis and/or angle' not in caplog.text

    g.rotate_system_vectors(system_rot, axis=system_rotvec, angle=system_rotangle)

    assert 'axis and/or angle' in caplog.text


@pytest.mark.parametrize('test_list,test_array', [(rotation_list, rotation_array)])
def test_rotation_list_array(test_list, test_array):
    g = Geometry()
    g.rotations = test_array
    assert np.allclose(g.rotations_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.rotation, b)
    for a, b in zip(g.rotations, test_array):
        assert np.allclose(a, b)

    g.rotations = test_list
    assert np.allclose(g.rotations_as_array, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.rotation, b)
    for a, b in zip(g.rotations, test_list):
        assert np.allclose(a, b)


@pytest.mark.parametrize('test_list,test_array', [(j_list, j_array)])
def test_j_list_array(test_list, test_array):
    g = Geometry()
    g.j_offsets = test_array
    assert np.allclose(g.j_offsets_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.j_offset, b)
    for a, b in zip(g.j_offsets, test_array):
        assert np.allclose(a, b)

    g.j_offsets = test_list
    assert np.allclose(g.j_offsets, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.j_offset, b)
    for a, b in zip(g.j_offsets, test_list):
        assert np.allclose(a, b)


@pytest.mark.parametrize('test_list,test_array', [(k_list, k_array)])
def test_k_list_array(test_list, test_array):
    g = Geometry()
    g.k_offsets = test_array
    assert np.allclose(g.k_offsets_as_array, test_array)
    for a, b in zip(g, test_array):
        assert np.allclose(a.k_offset, b)
    for a, b in zip(g.k_offsets, test_array):
        assert np.allclose(a, b)

    g.k_offsets = test_list
    assert np.allclose(g.k_offsets, test_list)
    for a, b in zip(g, test_list):
        assert np.allclose(a.k_offset, b)
    for a, b in zip(g.k_offsets, test_list):
        assert np.allclose(a, b)


def test_empty_hash():
    g = Geometry()
    assert str(hash(g))[:6] == '135563'
    assert g.hash_rotations[:6] == '786a02'
    assert g.hash_j_offsets[:6] == '786a02'
    assert g.hash_k_offsets[:6] == '786a02'


hash_list = ['119687', '134744', '334171']


@pytest.mark.parametrize('tup,hsh', [t for t in zip(tuple_list, hash_list)])
def test_gm_tuple_hash(tup, hsh):
    assert str(hash(tup))[:6] == hsh


def test_p_setter():
    g = Geometry()
    testvec = np.array((1, 2, 3))
    g.p_direction_0 = testvec
    assert np.allclose(g.p_direction_0, testvec)

    with pytest.raises(ValueError, match='size of the new value'):
        g.p_direction_0 = np.array((1, 2, 3, 4, 5))


def test_j_setter():
    g = Geometry()
    testvec = np.array((1, 2, 3))
    g.j_direction_0 = testvec
    assert np.allclose(g.j_direction_0, testvec)

    with pytest.raises(ValueError, match='size of the new value'):
        g.j_direction_0 = np.array((1, 2, 3, 4, 5))


def test_k_setter():
    g = Geometry()
    testvec = np.array((1, 2, 3))
    g.k_direction_0 = testvec
    assert np.allclose(g.k_direction_0, testvec)

    with pytest.raises(ValueError, match='size of the new value'):
        g.k_direction_0 = np.array((1, 2, 3, 4, 5))


def test_det_or():
    g = Geometry()
    testvec = np.array((1, 2, 3))
    g.detector_direction_origin = testvec
    assert np.allclose(g.detector_direction_origin, testvec)

    with pytest.raises(ValueError, match='size of the new value'):
        g.detector_direction_origin = np.array((1, 2, 3, 4, 5))


def test_det_90():
    g = Geometry()
    testvec = np.array((1, 2, 3))
    g.detector_direction_positive_90 = testvec
    assert np.allclose(g.detector_direction_positive_90, testvec)

    with pytest.raises(ValueError, match='size of the new value'):
        g.detector_direction_positive_90 = np.array((1, 2, 3, 4, 5))
