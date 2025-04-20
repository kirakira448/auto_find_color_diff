def trans_ltrb_to_xywh(left, top, right, bottom):
    """
    将左上右下坐标转换为左上宽高的格式
    """
    return (left, top, right - left, bottom - top)


def get_center_point(x,y,w,h):
    """
    获取方块的中心点
    :param x: 方块的左上角x坐标
    :param y: 方块的左上角y坐标
    :param w: 方块的宽度
    :param h: 方块的高度
    :return: 方块的中心点坐标
    """
    return int(x+w/2),int(y+h/2)