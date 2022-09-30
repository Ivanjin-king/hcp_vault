def num_rushes(slope_height, rush_height_gain, back_sliding):
    """5% reduction in height gain and back sliding on each rush"""
    current_height = 0
    rushes = 0
    while current_height < slope_height:
        print('x')
        current_height += rush_height_gain
        if current_height < slope_height:
            current_height -= back_sliding
        rush_height_gain = rush_height_gain * 0.95
    rushes += 1

    return rushes

ans = num_rushes(100, 15, 7)
print(ans)