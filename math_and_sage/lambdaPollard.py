def lambda_pollard(alpha,beta,a,b,t=1):
	n = alpha.multiplicative_order()
	w = b-a
	N = int(sqrt(w))
	k = ceil(0.5*log(w,2))
   
	alpha0 = alpha**b
	c0 = mod(b, n)
	AC = [(alpha0, c0)]

	for _ in range(1, t*N+1):
		fi = int(mod(int(AC[-1][0]), k))
		alpha_i = AC[-1][0]*alpha**(2**fi)
		ci = mod(AC[-1][1]+2**fi, n)
		AC.append((alpha_i, ci))


	beta_i = beta
	di = 0
	BD = [(beta_i, di)]
	   
	while True:
		tmp = dict(AC)
		if tmp.has_key(BD[-1][0]): 
			return tmp[BD[-1][0]] - BD[-1][1] #ci - di
		   
	   	fi = int(mod(int(BD[-1][0]), k))
	   	beta_i = BD[-1][0] * alpha**(2**fi)
	   	di = mod(BD[-1][1] + 2**fi, n)
	   	BD.append(((beta_i, di)))
	   
	   	if BD[-1][0] == BD[0][0]: 
			return -1
   
	return (AC,BD)

def main():
	p, alpha, beta= 11113, 13, 7035#23, 6, 12
	a, b = 8311, 8553

	F = GF(p)
	alpha = F(alpha)
	beta = F(beta)
	
	res = lambda_pollard(alpha, beta, a, b)   
	print res
	print power_mod(alpha, int(res), p) == beta

if __name__ == '__main__':
	main()