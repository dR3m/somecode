from sympy.ntheory import n_order

def PoygHellman(p, a, b):
	F = GF(p)
	a = F(a)
	b = F(b)
	r = a.multiplicative_order()
	r_factor = factor(r)
	x = []
	for el in r_factor:
		q, beta = el
		c, y, xi = 1, 0, 0
		a_ = a**(r/q)

		for k in range(beta):
			c = c*a**(y*q**(k-1))
			b_ = (b*c**-1)**(r/q**(k+1))
			y = log(b_, base=a_)
			xi = mod(xi + y*q**k, q**beta)

		x.append(xi)
	return crt([int(l) for l in x], [h[0]**h[1] for h in r_factor])


def main():
	a, b, p = 78, 565, 12007
	res = PoygHellman(p, a, b)
	print 'x =',res
	print '{}^{} = {} (mod {})'.format(a, res, b, p)
	print 'Check: ', b == power_mod(a, res, p)

if __name__ == '__main__':
	main()