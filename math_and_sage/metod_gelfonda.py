def sub():
	p = 97
	k = GF(p)
	a =  [0,0,0,1,9] 
	E = EllipticCurve(k, a)
	
	N = 90
	n_base = factor(N)
	Q = E.point((34, 16, 1))
	P = E.point((69, 40, 1))

	l = [] 
	foo = []
	for pi, ai in n_base:
		q, a = int(pi), int(ai)
		print
		print 'q = %d, a = %d' % (q, a)
		k = [0]
		S = E.point((0,1,0))
		Q_ = int(N/q)*Q
		for j in range(a):
			S = S + Q*int(k[j]*q**(j-1))
			P_ = (N/q**(j+1))*(P - S)
			P_, Q_ = E.point(P_), E.point(Q_)

			print 'P\' =',P_, ', Q\' =', Q_
			try:
				sol = Q_.discrete_log(P_)
		 	except ValueError:
				pass

			try:
				sol = P_.discrete_log(Q_)
		 	except ValueError:
				pass

			k.append(int(sol))
			#k.append(int(rhoPollarc_EC(E, P_, Q_)))
			print 'ki =', sol

		l.append(int(mod(sum([k[i+1]*q**i for i in range(a)]), q**a)))
		foo.append(int(q**a))
	
	res = CRT(l, foo)
	print
	print 'solution:', res


def main():
	sub()

if __name__ == '__main__':
	main()