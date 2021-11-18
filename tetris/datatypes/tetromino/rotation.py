def index():
    transformation = [
        lambda n, r, c:      n * r + c,                 # 0   degrees clockwise
        lambda n, r, c:      n * ((n - 1) - c) + r,     # 90  degrees clockwise
        lambda n, r, c: -1 + n * (n - r) - c,           # 180 degrees clockwise
        lambda n, r, c:      n * c + ((n - 1) - r),     # 270 degrees clockwise
    ]

    # index ###############################################
    def index(n, times_90_degrees, row, column):
        """Assuming the existence of an n*n element list acting
        as a two dimensional square array of n rows and n columns,
        this function gives back the appropriate index into the
        array at the given row and column, after rotating the array
        clockwise by some integer multiple of 90 degrees.
        """
        return transformation[int(times_90_degrees) % 4](n, row, column)
    return index


index = index()
