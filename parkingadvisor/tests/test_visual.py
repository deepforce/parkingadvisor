"""
Test the visualization module
"""
from datetime import datetime
from parkingadvisor import visual

def test_color_bar():
    """
    Smoke-test of creating colormap
    """
    for i in range(3):
        assert visual.color_bar(1 + i)


def test_switch_layer():
    """
    Smoke-test of choose correct layer
    """
    for i in range(3):
        assert visual.switch_layer(1 + i)
    assert visual.switch_layer(1)[1] == 'RATE'
    assert visual.switch_layer(2)[1] == 'OCCUPANCY'
    assert visual.switch_layer(3)[1] == 'RECOMM'

def test_MapLayer():
    """
    Testing the creation of a map with selected layer
    """

    now = datetime.now()
    # smode test of initiation
    assert visual.MapLayer(1, now, (47.6062, -122.3321))

    m = visual.MapLayer(1, now, (47.6062, -122.3321))
    assert m.mode == 1
    assert m.dest == (47.6062, -122.3321)

    # Testing mode-1 conresponsing to rate layer
    assert m.gdf.shape == (0, 0) # before

    m.add_layer() #  after
    assert 'RATE' in m.gdf.columns.values
