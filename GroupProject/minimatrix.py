# Framework for IEEE course final project
# Fan Cheng, 2022

import random
from typing import Iterable


class Matrix:
    r"""
    自定义的二维矩阵类

    Args:
        data: 一个二维的嵌套列表，表示矩阵的数据。即 data[i][j] 表示矩阵第 i+1 行第 j+1 列处的元素。
              当参数 data 不为 None 时，应根据参数 data 确定矩阵的形状。默认值: None
        dim: 一个元组 (n, m) 表示矩阵是 n 行 m 列, 当参数 data 为 None 时，根据该参数确定矩阵的形状；
             当参数 data 不为 None 时，忽略该参数。如果 data 和 dim 同时为 None, 应抛出异常。默认值: None
        init_value: 当提供的 data 参数为 None 时，使用该 init_value 初始化一个 n 行 m 列的矩阵，
                    即矩阵各元素均为 init_value. 当参数 data 不为 None 时，忽略该参数。 默认值: 0

    Attributes:
        dim: 一个元组 (n, m) 表示矩阵的形状
        data: 一个二维的嵌套列表，表示矩阵的数据

    Examples:
        >>> mat1 = Matrix(dim=(2, 3), init_value=0)
        >>> print(mat1)
        >>> [[0 0 0]
             [0 0 0]]
        >>> mat2 = Matrix(data=[[0, 1], [1, 2], [2, 3]])
        >>> print(mat2)
        >>> [[0 1]
             [1 2]
             [2 3]]
    """
    data: list[list]
    dim: tuple[int, int]

    def __init__(self, data=None, dim=None, init_value=0):
        if data is not None:
            assert type(data) == list and len(data) > 0
            self.data = data
            self.dim = len(data), len(data[0])
        elif dim is not None:
            assert type(dim) == tuple
            self.data = [[init_value] * dim[1] for _ in range(dim[0])]
            self.dim = dim
        else:
            raise Exception("data和dim不能同时为None")

    def shape(self) -> tuple[int, int]:
        r"""
        返回矩阵的形状 dim
        """
        return self.dim

    def reshape(self, newdim):
        r"""
        将矩阵从(m,n)维拉伸为newdim=(m1,n1)
        该函数不改变 self

        Args:
            newdim: 一个元组 (m1, n1) 表示拉伸后的矩阵形状。
            如果 m1 * n1 不等于 self.dim[0] * self.dim[1], 应抛出异常

        Returns:
            Matrix: 一个 Matrix 类型的返回结果, 表示 reshape 得到的结果
        """
        m1, n1 = newdim
        if m1 * n1 != self.dim[0] * self.dim[1]:
            raise Exception("元素个数不符，无法拉伸")
        flat = []
        for row in self.data:
            flat += row
        matrix = [flat[n1 * m: n1 * (m + 1)] for m in range(m1)]
        return Matrix(matrix)

    def dot(self, other):
        r"""
        矩阵乘法：矩阵乘以矩阵
        按照公式 A[i, j] = \sum_k B[i, k] * C[k, j] 计算 A = B.dot(C)

        Args:
            other: 参与运算的另一个 Matrix 实例

        Returns:
            Matrix: 计算结果

        Examples:
            >>> A = Matrix(data=[[1, 2], [3, 4]])
            >>> A.dot(A)
            >>> [[ 7 10]
                 [15 22]]
        """
        assert isinstance(other, Matrix)
        assert self.dim[1] == other.dim[0], "行列数不匹配，无法相乘"
        ans = Matrix(dim=(self.dim[0], other.dim[1]))
        for i in range(ans.dim[0]):
            for j in range(ans.dim[1]):
                for k in range(self.dim[1]):
                    ans[i, j] += self[i, k] * other[k, j]
        return ans

    def T(self):
        r"""
        矩阵的转置

        Returns:
            Matrix: 矩阵的转置

        Examples:
            >>> A = Matrix(data=[[1, 2], [3, 4]])
            >>> A.T()
            >>> [[1 3]
                 [2 4]]
            >>> B = Matrix(data=[[1, 2, 3], [4, 5, 6]])
            >>> B.T()
            >>> [[1 4]
                 [2 5]
                 [3 6]]
        """
        res = Matrix(dim=(self.dim[1], self.dim[0]), init_value=0)
        for i in range(self.dim[1]):
            for j in range(self.dim[0]):
                res[i, j] = self[j, i]
        return res

    def sum(self, axis=None):
        r"""
        根据指定的坐标轴对矩阵元素进行求和

        Args:
            axis: 一个整数，或者 None. 默认值: None
                  axis = 0 表示对矩阵进行按列求和，得到形状为 (1, self.dim[1]) 的矩阵
                  axis = 1 表示对矩阵进行按行求和，得到形状为 (self.dim[0], 1) 的矩阵
                  axis = None 表示对矩阵全部元素进行求和，得到形状为 (1, 1) 的矩阵

        Returns:
            Matrix: 一个 Matrix 类的实例，表示求和结果

        Examples:
            >>> A = Matrix(data=[[1, 2, 3], [4, 5, 6]])
            >>> A.sum()
            >>> [[21]]
            >>> A.sum(axis=0)
            >>> [[5 7 9]]
            >>> A.sum(axis=1)
            >>> [[6]
                 [15]]
        """
        if axis == 0:
            res = [0] * self.dim[1]
            for i in range(self.dim[0]):
                for j in range(self.dim[1]):
                    res[j] += self.data[i][j]
            return Matrix(list(map(lambda x: [x], res)))
        elif axis == 1:
            return Matrix([[sum(_)] for _ in self.data])
        elif axis is None:
            return Matrix([[sum(sum(_) for _ in self.data)]])
        else:
            raise Exception("axis必须为0,1或留空")

    def copy(self):
        r"""
        返回matrix的一个备份

        Returns:
            Matrix: 一个self的备份
        """
        return Matrix([row[:] for row in self.data])

    def Kronecker_product(self, other):
        r"""
        计算两个矩阵的Kronecker积，具体定义可以搜索，https://baike.baidu.com/item/克罗内克积/6282573

        Args:
            other: 参与运算的另一个 Matrix

        Returns:
            Matrix: Kronecke product 的计算结果
        """
        assert isinstance(other, Matrix)
        ans = Matrix(dim=(self.dim[0] * other.dim[0],
                     self.dim[1] * other.dim[1]))
        for i in range(other.dim[0]):
            for j in range(other.dim[1]):
                ans[i * self.dim[0]: (i + 1) * self.dim[0], j * self.dim[1]: (
                    j + 1) * self.dim[1]] = self * Matrix(dim=other.dim, init_value=other[i, j])
        return ans

    def __getitem__(self, key):
        r"""
        实现 Matrix 的索引功能，即 Matrix 实例可以通过 [] 获取矩阵中的元素（或子矩阵）

        x[key] 具备以下基本特性：
        1. 单值索引
            x[a, b] 返回 Matrix 实例 x 的第 a 行, 第 b 列处的元素 (从 0 开始编号)
        2. 矩阵切片
            x[a:b, c:d] 返回 Matrix 实例 x 的一个由
            第 a, a+1, ..., b-1 行, 第 c, c+1, ..., d-1 列元素
            构成的子矩阵
            特别地, 需要支持省略切片左(右)端点参数的写法, 如 x 是一个 n 行 m 列矩阵, 那么
            x[:b, c:] 的语义等价于 x[0:b, c:m]
            x[:, :] 的语义等价于 x[0:n, 0:m]

        Args:
            key: 一个元组，表示索引

        Returns:
            索引结果，单个元素或者矩阵切片

        Examples:
            >>> x = Matrix(data=[
                        [0, 1, 2, 3],
                        [4, 5, 6, 7],
                        [8, 9, 0, 1]
                    ])
            >>> x[1, 2]
            >>> 6
            >>> x[0:2, 1:4]
            >>> [[1 2 3]
                 [5 6 7]]
            >>> x[:, :2]
            >>> [[0 1]
                 [4 5]
                 [8 9]]
        """
        k1, k2 = key
        if type(k1) == int and type(k2) == int:
            return self.data[k1][k2]
        elif isinstance(k1, slice) and isinstance(k2, slice):
            k1 = slice(0 if k1.start is None else k1.start,
                       self.dim[0] if k1.stop is None else k1.stop,
                       k1.step)
            k2 = slice(0 if k2.start is None else k2.start,
                       self.dim[1] if k2.stop is None else k2.stop,
                       k2.step)
            return Matrix([[self.data[i][j] for j in range(k2.start, k2.stop)] for i in range(k1.start, k1.stop)])
        else:
            raise Exception("值类型错误")

    def __setitem__(self, key, value):
        r"""
        实现 Matrix 的赋值功能, 通过 x[key] = value 进行赋值的功能

        类似于 __getitem__ , 需要具备以下基本特性:
        1. 单元素赋值
            x[a, b] = k 的含义为，将 Matrix 实例 x 的 第 a 行, 第 b 处的元素赋值为 k (从 0 开始编号)
        2. 对矩阵切片赋值
            x[a:b, c:d] = value 其中 value 是一个 (b-a)行(d-c)列的 Matrix 实例
            含义为, 将
            由 Matrix 实例 x 的第 a, a+1, ..., b-1 行, 第 c, c+1, ..., d-1 列元素构成的子矩阵
            赋值为 value 矩阵
            即 子矩阵的 (i, j) 位置赋值为 value[i, j]
            同样地, 这里也需要支持如 x[:b, c:] = value, x[:, :] = value 等省略写法

        Args:
            key: 一个元组，表示索引
            value: 赋值运算的右值，即要赋的值

        Examples:
            >>> x = Matrix(data=[
                        [0, 1, 2, 3],
                        [4, 5, 6, 7],
                        [8, 9, 0, 1]
                    ])
            >>> x[1, 2] = 0
            >>> x
            >>> [[0 1 2 3]
                 [4 5 0 7]
                 [8 9 0 1]]
            >>> x[1:, 2:] = Matrix(data=[[1, 2], [3, 4]])
            >>> x
            >>> [[0 1 2 3]
                 [4 5 1 2]
                 [8 9 3 4]]
        """
        k1, k2 = key
        if (isinstance(k1, int) or isinstance(k1, float)) and (isinstance(k2, int) or isinstance(k2, float)) and (isinstance(value, int) or isinstance(value, float)):
            self.data[k1][k2] = value
        elif isinstance(k1, slice) and isinstance(k2, slice) and isinstance(value, Matrix):
            k1 = slice(0 if k1.start is None else k1.start,
                       self.dim[0] if k1.stop is None else k1.stop,
                       k1.step)
            k2 = slice(0 if k2.start is None else k2.start,
                       self.dim[1] if k2.stop is None else k2.stop,
                       k2.step)
            assert value.dim == (k1.stop - k1.start, k2.stop - k2.start)
            for i in range(k1.start, k1.stop):
                for j in range(k2.start, k2.stop):
                    self.data[i][j] = value.data[i - k1.start][j - k2.start]
        else:
            raise Exception("值类型错误")

    def __pow__(self, n):
        r"""
        矩阵的n次幂，n为自然数
        该函数应当不改变 self 的内容

        Args:
            n: int, 自然数

        Returns:
            Matrix: 运算结果
        """
        if self.dim[0] != self.dim[1]:
            raise Exception("不是方阵，无法求幂")
        if n == 0:
            return I(self.dim[0])
        matrix = self.copy()
        for _ in range(n - 1):
            matrix = matrix.dot(self)
        return matrix

    def __add__(self, other):
        r"""
        两个矩阵相加
        该函数应当不改变 self 和 other 的内容

        Args:
            other: 一个 Matrix 实例

        Returns:
            Matrix: 运算结果
        """
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise Exception("两个矩阵行数与列数不一致，无法相加")
        matrix = Matrix(dim=self.dim)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matrix.data[i][j] = self.data[i][j] + other.data[i][j]
        return matrix

    def __sub__(self, other):
        r"""
        两个矩阵相减
        该函数应当不改变 self 和 other 的内容

        Args:
            other: 一个 Matrix 实例

        Returns:
            Matrix: 运算结果
        """
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise Exception("两个矩阵行数与列数不一致，无法相减")
        matrix = Matrix(dim=self.dim)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matrix.data[i][j] = self.data[i][j] - other.data[i][j]
        return matrix

    def __mul__(self, other):
        r"""
        两个矩阵 对应位置 元素  相乘
        注意 不是矩阵乘法dot
        该函数应当不改变 self 和 other 的内容

        Args:
            other: 一个 Matrix 实例

        Returns:
            Matrix: 运算结果

        Examples:
            >>> Matrix(data=[[1, 2]]) * Matrix(data=[[3, 4]])
            >>> [[3 8]]
        """
        if self.dim[0] != other.dim[0] or self.dim[1] != other.dim[1]:
            raise Exception("两个矩阵行数与列数不一致，无法对应位置相乘")
        matrix = Matrix(dim=self.dim)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matrix.data[i][j] = self.data[i][j] * other.data[i][j]
        return matrix

    def __len__(self):
        r"""
        返回矩阵元素的数目

        Returns:
            int: 元素数目，即 行数 * 列数
        """
        return self.dim[0] * self.dim[1]

    def __str__(self):
        r"""
        按照
        [[  0   1   4   9  16  25  36  49]
          [ 64  81 100 121 144 169 196 225]
          [256 289 324 361 400 441 484 529]]
         的格式将矩阵表示为一个 字符串
         ！！！ 注意返回值是字符串
        """
        print_value = []
        line = [0] * self.dim[1]
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                len1 = len(str(self.data[i][j]))
                if len1 > line[j]:
                    line[j] = len1
        for i in range(self.dim[0]):
            if i == 0:
                print_value.append("[[")
            else:
                print_value.append(" [")
            for j in range(self.dim[1]):
                len1 = len(str(self.data[i][j]))
                if j == 0:
                    a = [" "] * (line[j] - len1)
                else:
                    a = [" "] * (line[j] + 1 - len1)
                print_value.extend(a)
                print_value.append(str(self.data[i][j]))
            if i == self.dim[0] - 1:
                print_value.append("]]")
            else:
                print_value.append("]\n")
        return "".join(print_value)
    def __repr__(self):
        return self.__str__()

    def det(self):
        r"""
        计算方阵的行列式。对于非方阵的情形应抛出异常。
        要求: 该函数应不改变 self 的内容; 该函数的时间复杂度应该不超过 O(n**3).
        提示: Gauss消元

        Returns:
            一个 Python int 或者 float, 表示计算结果
        """
        if self.dim[0] != self.dim[1]:
            raise Exception("该矩阵非方阵，无法求行列式")
        matrix = self.copy()
        times = 0
        for i in range(matrix.dim[1]):
            for j in range(i, matrix.dim[0]):
                if matrix.data[j][i] != 0:
                    if i != j:
                        matrix.data[i], matrix.data[j] = matrix.data[j], matrix.data[i]
                        times += 1
                    break
            if matrix.data[i][i] == 0:
                return 0
            for j in range(i + 1, matrix.dim[0]):
                k = matrix.data[j][i] / matrix.data[i][i]
                for n in range(matrix.dim[1]):
                    matrix.data[j][n] -= k * matrix.data[i][n]
        det_value = 1
        for i in range(matrix.dim[0]):
            det_value *= matrix.data[i][i]
        if times % 2 == 1:
            det_value *= -1
        return det_value

    def inverse(self):
        r"""
        计算非奇异方阵的逆矩阵。对于非方阵或奇异阵的情形应抛出异常。
        要求: 该函数应不改变 self 的内容; 该函数的时间复杂度应该不超过 O(n**3).
        提示: Gauss消元

        Returns:
            Matrix: 一个 Matrix 实例，表示逆矩阵
        """
        if self.dim[0] != self.dim[1]:
            raise Exception("该矩阵非方阵，无法求逆矩阵")
        matrix = self.copy()
        inverse_matrix = Matrix(dim=self.dim)
        for i in range(self.dim[0]):
            inverse_matrix.data[i][i] = 1  # 在右侧加入一个单位矩阵，变化后的结果即为逆矩阵
        for i in range(matrix.dim[0]):
            if matrix.data[i][i] == 0:
                raise Exception("该阵为奇异阵")
            for j in range(matrix.dim[0]):
                if j != i:
                    k = matrix.data[j][i] / matrix.data[i][i]
                    for n in range(matrix.dim[1]):
                        matrix.data[j][n] -= k * matrix.data[i][n]
                        inverse_matrix.data[j][n] -= k * \
                            inverse_matrix.data[i][n]  # 同步操作
        for i in range(matrix.dim[0]):
            k = 1 / matrix.data[i][i]
            for n in range(matrix.dim[1]):
                inverse_matrix.data[i][n] *= k
        return inverse_matrix

    def rank(self):
        r"""
        计算矩阵的秩
        要求: 该函数应不改变 self 的内容; 该函数的时间复杂度应该不超过 O(n**3).
        提示: Gauss消元

        Returns:
            一个 Python int 表示计算结果
        """
        matrix = self.copy()
        for i in range(matrix.dim[1]):
            x = None
            for j in range(i, matrix.dim[0]):
                if matrix.data[j][i] != 0:
                    x = j
                break
            if x is None:
                continue
            if i != x:
                matrix.data[i], matrix.data[x] = matrix.data[x], matrix.data[i]
            for j in range(i + 1, matrix.dim[0]):
                k = matrix.data[j][i] / matrix.data[i][i]
                for n in range(matrix.dim[1]):
                    matrix.data[j][n] -= k * matrix.data[i][n]
        rank = 0
        for line in matrix.data:
            for a in line:
                if a != 0:
                    rank += 1
                    break
        return rank


def I(n):
    '''
    return an n*n unit matrix
    '''
    matrix = Matrix(dim=(n, n))
    for i in range(n):
        matrix.data[i][i] = 1
    return matrix


def narray(dim, init_value=1):  # dim (,,,,,), init为矩阵元素初始值
    r"""
    返回一个matrix，维数为dim，初始值为init_value

    Args:
        dim: Tuple[int, int] 表示矩阵形状
        init_value: 表示初始值，默认值: 1

    Returns:
        Matrix: 一个 Matrix 类型的实例
    """
    return Matrix(dim=dim, init_value=init_value)


def arange(start, end, step=1):
    r"""
    返回一个1*n 的 narray 其中的元素类同 range(start, end, step)

    Args:
        start: 起始点(包含)
        end: 终止点(不包含)
        step: 步长

    Returns:
        Matrix: 一个 Matrix 实例
    """
    n = (end - start) // step
    data = [[start + i * step for i in range(n)]]
    return Matrix(data)


def zeros(dim):
    r"""
    返回一个维数为dim 的全0 narray

    Args:
        dim: Tuple[int, int] 表示矩阵形状

    Returns:
        Matrix: 一个 Matrix 类型的实例
    """
    return narray(dim, init_value=0)


def zeros_like(matrix: Matrix):
    """    
    Args:
        matrix: 一个 Matrix 实例

    Returns:
        Matrix: 一个 Matrix 类型的实例

    Examples:
        >>> A = Matrix(data=[[1, 2, 3], [2, 3, 4]])
        >>> zeros_like(A)
        >>> [[0 0 0]
             [0 0 0]]
    """
    return narray(matrix.dim, init_value=0)


def ones(dim):
    r"""
    返回一个维数为dim 的全1 narray
    类同 zeros
    """
    return narray(dim, init_value=1)


def ones_like(matrix: Matrix):
    r"""
    返回一个维数和matrix一样 的全1 narray
    类同 zeros_like
    """
    return narray(matrix.dim, init_value=1)


def nrandom(dim):
    r"""
    返回一个维数为dim 的随机 narray
    参数与返回值类型同 zeros
    """
    data = [[random.random() for __ in range(dim[1])]
            for _ in range(dim[0])]
    return Matrix(data)


def nrandom_like(matrix: Matrix):
    r"""
    返回一个维数和matrix一样 的随机 narray
    参数与返回值类型同 zeros_like
    """
    data = [[random.random() for __ in range(matrix.dim[1])]
            for _ in range(matrix.dim[0])]
    return Matrix(data)


def concatenate(items: Iterable[Matrix], axis=0):
    r"""
    将若干矩阵按照指定的方向拼接起来
    若给定的输入在形状上不对应，应抛出异常
    该函数应当不改变 items 中的元素

    Args:
        items: 一个可迭代的对象，其中的元素为 Matrix 类型。
        axis: 一个取值为 0 或 1 的整数，表示拼接方向，默认值 0.
              0 表示在第0维即行上进行拼接
              1 表示在第1维即列上进行拼接

    Returns:
        Matrix: 一个 Matrix 类型的拼接结果

    Examples:
        >>> A, B = Matrix([[0, 1, 2]]), Matrix([[3, 4, 5]])
        >>> concatenate((A, B))
        >>> [[0 1 2]
             [3 4 5]]
        >>> concatenate((A, B, A), axis=1)
        >>> [[0 1 2 3 4 5 0 1 2]]
    """
    assert items, "items不能为空"
    first_matrix = items[0]
    assert isinstance(first_matrix, Matrix), "矩阵类型不对"
    assert axis in [0, 1], "axis必须为0或1"
    first_shape = first_matrix.shape()
    if axis == 0:
        columns = first_shape[1]
        for item in items:
            if item.shape()[1] != columns:
                raise Exception(
                    "矩阵的列数不相等")
    else:
        rows = first_shape[0]
        for item in items:
            if item.shape()[0] != rows:
                raise Exception(
                    "矩阵的行数不相等")
    result_data = []
    if axis == 0:
        result_data = [row for matrix in items for row in matrix.data]
    else:
        result_data = []
        for row in range(rows):
            result_row = []
            for item in items:
                result_row.extend(item.data[row])
            result_data.append(result_row)
    return Matrix(result_data)


def vectorize(func):
    r"""
    将给定函数进行向量化

    Args:
        func: 一个Python函数

    Returns:
        一个向量化的函数 F: Matrix -> Matrix, 它的参数是一个 Matrix 实例 x, 返回值也是一个 Matrix 实例；
        它将函数 func 作用在 参数 x 的每一个元素上

    Examples:
        >>> def func(x):
                return x ** 2
        >>> F = vectorize(func)
        >>> x = Matrix([[1, 2, 3],[2, 3, 1]])
        >>> F(x)
        >>> [[1 4 9]
             [4 9 1]]
        >>>
        >>> @vectorize
        >>> def my_abs(x):
                if x < 0:
                    return -x
                else:
                    return x
        >>> y = Matrix([[-1, 1], [2, -2]])
        >>> my_abs(y)
        >>> [[1, 1]
             [2, 2]]
    """
    def f(matrix: Matrix) -> Matrix:
        new_matrix = matrix.copy()
        for i in range(new_matrix.dim[0]):
            for j in range(new_matrix.dim[1]):
                new_matrix[i, j] = func(new_matrix[i, j])
        return new_matrix
    return f


if __name__ == "__main__":
    pass
