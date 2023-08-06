from graph_builder import GraphBuilder


def test_scale_overlay():
    builder = GraphBuilder("sample_data/in.webm")
    w_overlay, h_overlay = builder.scale_overlay(xpos=0.0, ypos=0.0, scale=2.0)
    except_w, except_h = -960, -1080
    assert w_overlay == except_w
    assert h_overlay == except_h

    # Test case 1: Scale and overlay at center
    w_overlay, h_overlay = builder.scale_overlay(xpos=0.5, ypos=0.5, scale=0.5)
    print(w_overlay, h_overlay)
    assert w_overlay == 1440
    assert h_overlay == 0

    # Test case 2: Scale and overlay at top-right corner
    w_overlay, h_overlay = builder.scale_overlay(xpos=1.0, ypos=0.0, scale=1.5)
    print(w_overlay, h_overlay)
    assert w_overlay == 1440
    assert h_overlay == -540

    # Test case 3: Scale and overlay at bottom-left corner
    w_overlay, h_overlay = builder.scale_overlay(xpos=0.0, ypos=1.0, scale=0.75)
    print(w_overlay, h_overlay)
    assert w_overlay == 240
    assert h_overlay == -810

    # Test case 4: Scale and overlay with no position change
    w_overlay, h_overlay = builder.scale_overlay(xpos=0.25, ypos=0.75, scale=1.0)
    print(w_overlay, h_overlay)
    assert w_overlay == 480
    assert h_overlay == -810
