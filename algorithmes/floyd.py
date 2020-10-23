import numpy as np


class Floyd:
    def __init__(self, matrix):
        self.A = np.array(matrix)
        x, y = np.shape(self.A)
        if x == y:
            self.n = x
        zeroes = list(np.diagonal(self.A))
        if zeroes == [np.int32(0) for _ in range(x)]:
            self.algorithm()
        else:
            print('Неправильно введены данные')

    def algorithm(self):
        try:
            for k in range(self.n):
                for i in range(self.n):
                    for j in range(self.n):
                        if int(self.A[i][k]) + int(self.A[k][j]) < int(self.A[i][j]):
                            self.A[i][j] = self.A[i][k]+self.A[k][j]
        except ValueError:
            print('Неправильно введены данные')
        except NameError:
            print('Неправильно введены данные')
        print(self.A)


f = Floyd([[0, 1, 5, 2], [1, 0, 1, 5], [5, 1, 0, 1], [2, 5, 1, 0]])

