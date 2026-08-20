import minimatrix as mm


def test_all():

    # Test Unit 0
    assert mm.Matrix(dim=(2, 3), init_value=-
                     1).data == [[-1, -1, -1], [-1, -1, -1]]

    # Test Unit 1.1 (Methods of Matrix class)
    mat = mm.Matrix([[1, 2, 3], [6, 5, 4], [7, 8, 9]])
    assert mat.shape() == (3, 3)
    assert mat.reshape((1, 9)).data == [[1, 2, 3, 6, 5, 4, 7, 8, 9]]
    assert mat.dot(mat).data == [[34, 36, 38], [64, 69, 74], [118, 126, 134]]
    assert mat.T().data == [[1, 6, 7], [2, 5, 8], [3, 4, 9]]
    assert mat.sum().data == [[45]]
    assert mat.sum(0).data == [[14], [15], [16]]
    assert mat.sum(1).data == [[6], [15], [24]]
    assert mat.copy().data == mat.data
    assert mat.copy() is not mat
    assert mat.copy().data is not mat.data
    assert mat.Kronecker_product(mat).data == [[1, 2, 3, 2, 4, 6, 3, 6, 9],
                                               [6, 5, 4, 12, 10, 8, 18, 15, 12],
                                               [7, 8, 9, 14, 16, 18, 21, 24, 27],
                                               [6, 12, 18, 5, 10, 15, 4, 8, 12],
                                               [36, 30, 24, 30, 25,
                                                   20, 24, 20, 16],
                                               [42, 48, 54, 35, 40,
                                                   45, 28, 32, 36],
                                               [7, 14, 21, 8, 16, 24, 9, 18, 27],
                                               [42, 35, 28, 48, 40,
                                                   32, 54, 45, 36],
                                               [49, 56, 63, 56, 64, 72, 63, 72, 81]]
    assert mat[0, 1] == 2
    assert mat[:, :].data == mat.data
    assert mat[:1, 1:].data == [[2, 3]]
    mat2 = mat.copy()
    mat2[1:, 1:] = mm.Matrix([[1, 1], [4, 5]])
    assert mat2.data == [[1, 2, 3], [6, 1, 1], [7, 4, 5]]
    mat2[0, 0] = 2
    assert mat2.data == [[2, 2, 3], [6, 1, 1], [7, 4, 5]]
    assert (mat ** 2).data == [[34, 36, 38], [64, 69, 74], [118, 126, 134]]
    assert (mat + mat).data == [[2, 4, 6], [12, 10, 8], [14, 16, 18]]
    assert (mat - mat).data == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert (mat * mat).data == [[1, 4, 9], [36, 25, 16], [49, 64, 81]]
    assert len(mat) == 9
    print(mat)
    assert mat.det() == 0
    assert mm.Matrix([[1, 2], [1, 3]]).inverse().data == [[3, -2], [-1, 1]]
    assert mat.rank() == 2

    # Test Unit 1.2 (Outside functions)
    assert mm.I(2).data == [[1, 0], [0, 1]]
    assert mm.narray((3, 3), 6).data == [[6, 6, 6], [6, 6, 6], [6, 6, 6]]
    assert mm.arange(1, 10, 3).data == [[1, 4, 7]]
    assert mm.zeros((3, 3)).data == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert mm.zeros_like(mat).data == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert mm.ones((3, 3)).data == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert mm.ones_like(mat).data == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    print(mm.nrandom((3, 3)))
    print(mm.nrandom_like(mat))
    assert mm.concatenate([mat, mat]).data == [[1, 2, 3], [6, 5, 4], [
        7, 8, 9], [1, 2, 3], [6, 5, 4], [7, 8, 9]]
    assert mm.concatenate([mat, mat], axis=1).data == [
        [1, 2, 3, 1, 2, 3], [6, 5, 4, 6, 5, 4], [7, 8, 9, 7, 8, 9]]

    def func(x):
        return x ** 2
    F = mm.vectorize(func)
    assert F(mat).data == [[1, 4, 9], [36, 25, 16], [49, 64, 81]]

    @mm.vectorize
    def my_abs(x):
        if x < 0:
            return -x
        else:
            return x
    assert my_abs(mat).data == [[1, 2, 3], [6, 5, 4], [7, 8, 9]]

    # Test Unit 2
    m24 = mm.arange(0, 24)
    assert m24.reshape((3, 8)).data == [[0, 1, 2, 3, 4, 5, 6, 7], [
        8, 9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22, 23]]
    assert m24.reshape((24, 1)).data == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [
        10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]]
    assert m24.reshape((4, 6)).data == [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [
        12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23]]
    print(m24.reshape((3, 8)))
    print(m24.reshape((24, 1)))
    print(m24.reshape((4, 6)))

    # Test Unit 3
    print(mm.zeros((3, 3)))
    assert mm.zeros_like(m24).data == [[0] * 24]

    # Test Unit 4
    print(mm.ones((3, 3)))
    assert mm.ones_like(m24).data == [[1] * 24]

    # Test Unit 5
    print(mm.nrandom((3, 3)))
    print(mm.nrandom_like(m24))

    # Test Unit 6
    m, n = 1000, 100
    x = mm.nrandom((m, n))
    w = mm.nrandom((n, 1))
    e0 = mm.nrandom((m, 1))
    e1 = mm.Matrix(dim=(m, 1), init_value=e0.sum().data[0][0] / m)
    e = e0 - e1
    y = x.dot(w) + e
    w1 = (x.T().dot(x).inverse().dot(x.T())).dot(y)
    print(w - w1)
    print((w - w1).sum())


if __name__ == "__main__":
    test_all()
