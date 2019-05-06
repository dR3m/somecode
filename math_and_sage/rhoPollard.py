def f(E, P, Q, W):
	x = W[0]
	if mod(x, 2) == 0:
		return ((0, 1), E.point(W + P))
	else:	
		return ((1, 0), E.point(W + Q))

def sub3(E, P, Q):
	a, b, c, d = [randint(0, 73) for _ in range(4)]	
	logR = [a, b]
	logS = [c, d]
	R = a*Q + b*P
	S = c*Q + d*P

	for i in range(1000):
		t, R = f(E, P, Q, R)
		logR[0] += t[0]
		logR[1] += t[1]
		
		t, S = f(E, P, Q, S)
		logS[0] += t[0]
		logS[1] += t[1]

		t, S = f(E, P, Q, S)
		logS[0] += t[0]
		logS[1] += t[1]


		print R, S		
		print logR, logS		
		print

		if R == S:
			return (logR, logS)
		elif R == -S:
			return (logR, [-logS[0], -logS[1]])

	return -1

def rhoPollarc_EC():
	k = GF(73)
	F = PolynomialRing(k, 'x, y')
	x, y = F.gens()

	a =  [0,0,0,3,9] 
	E = EllipticCurve(k, a)
	Q = E.point((31, 6, 1))
	P = E.point((24, 53, 1))
	r = 83 #prostoy poryadok gruppy <Q>

	while 1:
		tmp = sub3(E, P, Q)
		while tmp == -1:	
			tmp = sub3(E, P, Q)

		logR, logS = tmp
		l = var('l')
		sol = solve_mod(logS[0]+logS[1]*l==logR[0]+logR[1]*l, r)
		if len(sol) > 0:
			sol = int(sol[0][0])
			print sol
			print P == Q*sol
			return sol

def main():
	rhoPollarc_EC()


if __name__ == '__main__':
	main()