from collections import OrderedDict
from enum import IntEnum
from robosuite.utils.mjcf_utils import xml_path_completion
import robocasa


class TabletopLayoutType(IntEnum):
    """
    Enum for available tabletop layouts in RoboCasa environment
    """

    TABLETOP = 0
    CLUTTERED_TABLETOP = 1
    TABLETOP_WITH_MICROWAVE = 2
    TABLETOP_COTRAIN = 3
    TABLETOP_WITH_DRAWER = 4
    TABLETOP_WITH_CABINET = 5

    # negative values correspond to groups (see TABLETOP_LAYOUT_GROUPS_TO_IDS)
    ALL = -1


TABLETOP_LAYOUT_GROUPS_TO_IDS = {
    -1: list(range(len(TabletopLayoutType) - 1)),  # all
}


class StyleType(IntEnum):
    """
    Enums for available styles in RoboCasa environment
    """

    INDUSTRIAL = 0
    SCANDANAVIAN = 1
    COASTAL = 2
    MODERN_1 = 3
    MODERN_2 = 4
    TRADITIONAL_1 = 5
    TRADITIONAL_2 = 6
    FARMHOUSE = 7
    RUSTIC = 8
    MEDITERRANEAN = 9
    TRANSITIONAL_1 = 10
    TRANSITIONAL_2 = 11

    # negative values correspond to groups
    ALL = -1


STYLE_GROUPS_TO_IDS = {
    -1: list(range(12)),  # all
}


def get_tabletop_layout_path(layout_id):
    """
    Get corresponding blueprint filepath (yaml) for a layout

    Args:
        layout_id (int or TabletopLayoutType): layout id (int or enum)

    Return:
        str: yaml path for specified layout
    """
    if isinstance(layout_id, int):
        layout_int_to_name = dict(
            map(lambda item: (item.value, item.name.lower()), TabletopLayoutType)
        )
        layout_name = layout_int_to_name[layout_id]
    elif isinstance(layout_id, TabletopLayoutType):
        layout_name = layout_id.name.lower()
    else:
        raise ValueError

    # special case: if name starts with one letter, capitalize it
    if layout_name[1] == "_":
        layout_name = layout_name.capitalize()

    return xml_path_completion(
        f"scenes/tabletop_layouts/{layout_name}.yaml",
        root=robocasa.models.assets_root,
    )


def get_style_path(style_id):
    """
    Get corresponding blueprint filepath (yaml) for a style

    Args:
        style_id (int or StyleType): style id (int or enum)

    Return:
        str: yaml path for specified style
    """
    if isinstance(style_id, int):
        style_int_to_name = dict(
            map(lambda item: (item.value, item.name.lower()), StyleType)
        )
        style_name = style_int_to_name[style_id]
    elif isinstance(style_id, StyleType):
        style_name = style_id.name.lower()
    else:
        raise ValueError

    return xml_path_completion(
        f"scenes/kitchen_styles/{style_name}.yaml",
        root=robocasa.models.assets_root,
    )


def unpack_tabletop_layout_ids(layout_ids):
    if layout_ids is None:
        layout_ids = TabletopLayoutType.ALL

    if not isinstance(layout_ids, list):
        layout_ids = [layout_ids]

    layout_ids = [int(id) for id in layout_ids]

    all_layout_ids = []
    for id in layout_ids:
        if id < 0:
            all_layout_ids += TABLETOP_LAYOUT_GROUPS_TO_IDS[id]
        else:
            all_layout_ids.append(id)
    return list(OrderedDict.fromkeys(all_layout_ids))


def unpack_style_ids(style_ids):
    if style_ids is None:
        style_ids = StyleType.ALL

    if not isinstance(style_ids, list):
        style_ids = [style_ids]

    style_ids = [int(id) for id in style_ids]

    all_style_ids = []
    for id in style_ids:
        if id < 0:
            all_style_ids += STYLE_GROUPS_TO_IDS[id]
        else:
            all_style_ids.append(id)
    return list(OrderedDict.fromkeys(all_style_ids))
