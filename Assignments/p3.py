
# Big Integers

class BigInt:
    val: list[int]
    length: int
    neg: bool = False
    
    def __init__(self, value: str = None, data: list[int] = None, neg: bool = False):
        if value:
            l = []
            for _ in value[::-1]:
                if _ == '-':
                    self.neg = True
                else:
                    l.append(int(_))
            self.val = l
        elif data:
            self.val = data
            self.neg = neg
        else:
            raise ValueError("Invalid Integer")
        self.length = len(self.val)
            
    def __add__(self, value):
        assert isinstance(value, BigInt)
        self._0(max(self.length, value.length))
        value._0(max(self.length, value.length))
        p = 0
        l = []
        k1 = -1 if self.neg else 1
        k2 = -1 if value.neg else 1
        for i in range(self.length):
            sum = k1 * self.val[i] + p + k2 * value.val[i]
            l.append(sum % 10)
            p = sum // 10
        if p < 0:
            return (self.oppo() + value.oppo()).oppo()
        if p:
            l.append(p)
        return BigInt(data=l)
    
    def __sub__(self, value):
        assert isinstance(value, BigInt)
        return self + value.oppo()
    
    def __mul__(self, value):
        assert isinstance(value, BigInt)
        k = self.neg ^ value.neg
        l = [0] * (self.length + value.length)
        for i in range(self.length):
            for j in range(value.length):
                nl = l[i + j] + self.val[i] * value.val[j]
                l[i + j] = nl % 10
                l[i + j + 1] += nl // 10
        return BigInt(data=l, neg=k)
    
    def __truediv__(self, value):
        assert isinstance(value, BigInt)
        num = self.copy()
        ans = BigInt('0')
        for k in range(self.length - value.length, -1, -1):
            for i in range(9, 0, -1):
                if not (num - value * BigInt(str((10 ** k) * i))).neg:
                    num -= value * BigInt(str((10 ** k) * i))
                    ans += BigInt(str((10 ** k) * i))
                    break
        return ans, num
    
    def __pow__(self, value: int):
        num = int(value)
        ans = BigInt('1')
        while num:
            ans *= self
            num -= 1
        return ans
    
    def _0(self, n: int):
        if self.length < n:
            self.val += [0] * (n - self.length)
            self.length = n
        
    def __str__(self):
        for i in range(self.length - 1, -1, -1):
            if self.val[i]:
                break
            self.val.pop(i)
        if len(self.val) == 0:
            self.val = [0]
        self.length = len(self.val)
        ret = ""
        for i in range(self.length - 1, -1, -1):
            ret += str(self.val[i])
        return ("-" if self.neg else "") + ret
    
    def __repr__(self):
        return self.__str__()
    
    def copy(self):
        return BigInt(data=[_ for _ in self.val], neg=self.neg)
    
    def oppo(self):
        bint = BigInt(data = self.val, neg = not self.neg)
        return bint

def add(str1: str, str2: str) -> str:
    return (BigInt(str1) + BigInt(str2)).__str__()

def sub(str1: str, str2: str) -> str:
    return (BigInt(str1) + BigInt(str2).oppo()).__str__()

def mul(str1: str, str2: str) -> str:
    return (BigInt(str1) * BigInt(str2)).__str__()

def div(str1: str, str2: str) -> tuple[str, str]:
    ans, rem = BigInt(str1) / BigInt(str2)
    return ans.__str__(), rem.__str__()

def pow(str1: str, n: int) -> str:
    return (BigInt(str1) ** n).__str__()
    
def main():
    print(add('22222222222222', '8773849905050505'))
    print(sub('11111111', '9877344555'))
    print(sub('345676778778', '222222'))
    print(mul('123456', '789'))
    print(div('8773849905050505', '123')[0]) # 整除
    print(pow('2', 66))
    print(add(pow('2', 100), pow('3', 50)))
    print(sub(add(mul('2', '100'), mul('123456', '789')), div('8773849905050505', '123')[0]))
    
if __name__ == "__main__":
    main()
    
    # print(BigInt('123') + BigInt('-234'))
    # print(BigInt('-123') + BigInt('234'))
    # print(BigInt('123') - BigInt('234'))
    # print(BigInt('1234567') + BigInt('7654321'))
    # print(BigInt('11') * BigInt('-876'))
    # print(BigInt('20') / BigInt('3'))
    # print(BigInt('20') ** BigInt('3'))
    # print(BigInt('1').copy())
