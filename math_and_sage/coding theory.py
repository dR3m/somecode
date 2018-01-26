#
#
#скрипт для решения контрольной по теории кодирования 
#
#
# -*- coding: utf-8 -*-
from sympy import n_order
from itertools import combinations, permutations
from sympy import Symbol	 

def cyclotomic_code(q, n, k, vector):
	F = GF(q)
	R, x = PolynomialRing(F, 'x').objgen()
	X = x**n - 1
	f = sum([vector[i]*x**i for i in range(len(vector))])
	h = X//f
	k = h.degree()
	d = n_order(q, n)
	c1 = euler_phi(n)/d
	F, alpha = F.extension(f, 'alpha').objgen()
	print 'q = {0}, n = {1}'.format(q, n)
	print 'd = ord {0} mod {1} = {2}'.format(q, n, d)
	print 'phi(n)/d = {0}'.format(c1)
	print 'Ф{0} раскладывается над F{1} на {2} множителей степени {3}'.format(n,q,c1,d)
	print 'Ф{0} = {1}'.format(n, cyclotomic_polynomial(n))
	c2 = X.factor()
	print 'X = {0} = {1}\n'.format(X, X.factor())
	print 'Сколько существует кодов длины {0}  над F{1}: {2}'.format(n, q, factorial(len(c2)))
	t = []
	c3 = [i[0] for i in c2]
	for i in range(1,len(c3)):
		for j in combinations(c3, i):
			t.append(n-sum([_.degree() for _ in j]))
			print t[-1], j

	#мб в следующей строке должно быть n-k		
	G =  matrix([[0 for j in range(i)]+f.coefficients(sparse=False)+[ 0 for j in range(n-f.degree()-i-1)] for i in range(k)])	
	print '\nПорождающий многочлен f = {0}'.format(f)
	print 'Порождающая матрица G: \n{0}\n'.format(G)
	
	u = Matrix([1,0,0,1])
	#code_word = u*G
	#print 'Кодовое слово u*G = {0}\n'.format(code_word)

	print 'Проверочный многочлен h = {0}'.format(h)

	#мб в следующей строке должно быть n-k
	H =  matrix([[ 0 for j in range(n-h.degree()-i-1)]+h.coefficients(sparse=False)[::-1]+[0 for j in range(i)] for i in range(n-k)])	
	print 'Проверочная матрица H: \n' ,H

	#u = Matrix([1,1,0,0,1,0,1]) #кодовое слово
	#xT = transpose(code_word)
	#print '\nH*xt = \n{0}\n'.format(H*xT) #должен получиться 0

def cycl_pol(n):
	R, x = PolynomialRing(GF(2), 'x').objgen()
	tmp = [[(x**(n//i)-1), moebius(i)] for i in range(1,n+1) if n%i == 0]
	res = cyclotomic_polynomial(n)
	print 'Проверка: ',mul([i[0]**i[1] for i in tmp]) == res
	print 'Ф{0} ='.format(n),' + '.join(['('+str(i[0])+')^'+str(i[1]) for i in tmp]), '=', res
	return res


def BCH_code(p, n, b, delta, vector):
	clear_vars()
	m = n_order(p, n)
	q = p**m
	if b == -1: b = 1
	if delta == -1: delta = 0

	F = GF(p) # q = p^m
	R, x = PolynomialRing(F, 'x').objgen()
	#R2, alpha = PolynomialRing(F, 'alpha').objgen()
	#x = Symbol('x')
	alpha = Symbol('alpha')
	ALPHAS = [alpha**i for i in range(b, b+delta-1)]
	print 'Базис =', ALPHAS

	print '\nЦиклотомические классы:'
	cyclotomic_classes = []
	tmp = []
	for i in range(len(ALPHAS)):
		#t = q-1//gcd(i+1, q-1)
		#di = n_order(i+1, t)
		if i+1 not in tmp: 
			cyclotomic_classes.append([(i+1)*(p**j) for j in range(0, m) if (i+1)**(p**j)<q])
			for _ in cyclotomic_classes[-1]: tmp.append(_)
			print cyclotomic_classes[-1], 'f_a^{0} = {1}'.format(i+1, [x-alpha**_ for _ in cyclotomic_classes[-1]])
	
	#if vector != []: f = sum([vector[i]*x**i for i in range(len(vector))])
	#else:
	f = [cycl_pol(n//gcd(i[0],n)) for i in cyclotomic_classes]
	if vector != []: 
		f[0] = sum([vector[i]*x**i for i in range(len(vector))]) 
	print 'f = НОК({0})'.format(f)	

	f = (x**2-x-1)*(x**2+1)*(x+1)
	F, xi = F.extension(f, 'xi').objgen()
	X = x**n-1
	h = X//f
	k = h.degree()
	print 'k = ',k
	#cyclotomic_code(p,n,k, f.coefficients(sparse=False)[::-1])

	print 'Проверочный многочлен h = {0}'.format(h)
	H =  matrix([[ 0 for j in range(n-h.degree()-i-1)]+h.coefficients(sparse=False)[::-1]+[0 for j in range(i)] for i in range(n-k)])	
	print 'Проверочная матрица H: \n' ,H

	G =  Matrix([[0 for j in range(i)]+f.coefficients(sparse=False)+[ 0 for j in range(n-f.degree()-i-1)] for i in range(k)])
	print '\nПорождающий многочлен f = {0}'.format(f)
	print 'Порождающая матрица G: \n{0}\n'.format(G)

	#print 'f = {1} = {0}'.format(f.factor(), f)
	#print 'alpha корень ', f.factor()[0][0]
	#print 'Примитивный элемент',F2.primitive_element()

def main():
	cyclotomic_code(2, 7, 3, [1,1,0,1,0,0,0])
	BCH_code(5, 12, 3,3, []) #[1,0,0,0,1,0,1,1,1])#[1,1,0,0,1,0,0,0]) #[1,1,0,1,0,0,0])

if __name__ == '__main__':
	main()
