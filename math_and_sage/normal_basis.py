#арифметика в представлении нормальных базисов 
from sympy import n_order
def _pow(b, e):
	x, y, c = 1, b, e
	while c>0:
		if c&1: #четное не чётное\ последний бит 0 или 1
			x, c = x*y, c-1
		else:
			y, c = y*y, c>>1
	return x

def _mul(a, b, B, q):
	print('Нормальный базис: {0:s}\nОбразующая: alpha = {1:s}\n'.format(str(B), str(B[0])))
	print('a = {0:d}\nb = {1:d}'.format(a, b))

	n = len(B)
	alpha = B[0]
	coef_a = [(a&2**i)>>i for i in range(n-1,-1,-1)]#бинарное представление n-битных чисел
	coef_b = [(b&2**i)>>i for i in range(n-1,-1,-1)]

	#представление чисел a, b в базисe
	a = [coef_a[i]*B[i] for i in range(n)]	
	b = [coef_b[i]*B[i] for i in range(n)]	

	#p - список коэффициентов разложения в базисе произведения 
	#равные сумме произведений в строке: t[i,j]*alpha^(q^i)
	#t[i,j] элемент матрицы, строки которой коэффициенты элемента alpha*alpha^(q^m)
	p = [sum([B[k]*coef_a[k]*coef_b[m] for k in range(n) ]) for m in range(n)]
	result = [p[m]*B[m] for m in range(n)]

	print('Представление a, b в нормальном базисе:\na = {0:s}\nb = {1:s}\n'.format(str(' + '.join([str(i) for i in a])), str(' + '.join([str(i) for i in b]))))
	print('a*b = {0:s} = {1:s}'.format(str(' + '.join([str(i) for i in result])), str(sum(result))))

	return sum(result)

def main():
	q, n = 2, 6

	F = GF(q)
	R, x = PolynomialRing(F, 'x').objgen()
	m = 2 #поиск m для кругового многочлена
	while True:
		if gcd(q, m) == 1 and n_order(q,m) == n and euler_phi(m) == n: break
		else: m+=1 
	f = cyclotomic_polynomial(m) #неприодим над Fq
	F, zeta = F.extension(f, 'zeta').objgen() #примитивный корень степени m из единицыб корень f
	print F
	
	alpha = 0		
	for i in F:#поиск образующего элемена
		if i !=0  and i.multiplicative_order() == q**n-1: 
			alpha = i
			break
	alpha = zeta + zeta**3

	B = [_pow(alpha, _pow(q, i)) for i in range(n)] #нормальный базис

	#n-битные числа
	_mul(12, 25, B, q)		
	clear_vars()

if __name__ == '__main__':
	main()
