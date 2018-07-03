#ОПРЕДЕЛЕНИЕ РЕАКТИВНЫХ СОПРОТИВЛЕНИЙ И СДВИГА ФАЗ В ЦЕПЯХ С СИНУСОИДАЛЬНЫМ НАПРЯЖЕНИЕМ

from decimal import *
from math import *

def complex_mul(a, b):
	res = [0,0]
	res[0] = a[0]*b[0]+(-1*a[1]*b[1])
	res[1] = a[0]*b[1] + a[1]*b[0]
	return res

def complex_sum(a, b):
	res = [0,0]
	res[0] = a[0]+b[0]
	res[1] = a[1]+b[1]
	return res	

def complex_div(a, b):
	res = [0,0]
	tmp1 = complex_mul(a, [b[0], -1*b[1]])
	print('from complex_div:', a, b)
	print('tmp1 = ', tmp1)
	tmp2 = b[0]**2+b[1]**2
	res[0] = tmp1[0]/tmp2
	res[1] = tmp1[1]/tmp2
	return res

def main():
	E = 9
	nu = 3000
	R1, L1 = 4, 0.4*(10**-3)
	R2, L2 = 6, 0.2*(10**-3)
	R3, C3 = 10, 5*(10**-6)

	#Двухполюсник S1
	w = round(2*pi*nu)
	XL1 = w*L1
	_Z1 = [R1, XL1]
	Z1 = sqrt(_Z1[0]**2 + _Z1[1]**2)
	phiZ1 = degrees(atan(XL1/R1))

	#Двухполюсник P1
	XL2 = w*L2
	_Z2 = [0,0]
	_Z2[0] = (R2*(XL2**2))/(R2**2+XL2**2)
	_Z2[1] = ((R2**2)*XL2)/(R2**2+XL2**2)
	Z2 = sqrt(_Z2[0]**2+_Z2[1]**2)
	phiZ2 = degrees(atan(R2/XL2))

	#Двухполюсник P2
	XC3 = 1/(w*C3)
	_Z3 = [0,0]
	_Z3[0] = (R3*(XC3**2))/(R3**2+XC3**2)
	_Z3[1] = -1*((R3**2)*XC3)/(R3**2+XC3**2)
	Z3 = sqrt(_Z3[0]**2+_Z3[1]**2)
	phiZ3 = degrees(atan(-1*R3/XC3))

	print(w)
	print('XL1, _Z1, Z1, phiZ1', XL1, _Z1, Z1, phiZ1)
	print('XL2, _Z2, Z2, phiZ2', XL2, _Z2, Z2, phiZ2)
	print('XC3, _Z3, Z3, phiZ3', XC3, _Z3, Z3, phiZ3)
	print('\n')

	#Эквивалентное комплексное сопротивление разветвления
	_Z23 = complex_div(complex_mul(_Z2, _Z3), complex_sum(_Z2, _Z3)) 
	print('_Z23', _Z23)
	print('\n')

	#Комплексное входное сопротивление
	_Z = complex_sum(_Z1, _Z23)
	Z = sqrt(_Z[0]**2+_Z[1]**2)
	phiZ = degrees(atan(_Z[1]/_Z[0]))
	print('_Z, Z, phiZ', _Z, Z, phiZ)
	print('\n')

	#Комплексная величина входного напряжения
	_U = [E*(cos(radians(phiZ))), E*(sin(radians(phiZ)))]
	_E = _U
	psiU = phiZ
	print('_U, _E, psiU', _U, _E, psiU)
	print('\n')

	#Комплексная величина входного тока
	_I1 = complex_div(_U, _Z)
	I1 = sqrt(_I1[0]**2+_I1[1]**2)
	psiI1 = round(degrees(atan(_I1[1]/_I1[0])))
	print('_I1, I1, psiI1', _I1, I1, psiI1)
	print('\n')

	#Напряжение на двухполюснике S1
	_U1 = complex_mul(_I1, _Z1)
	U1 = sqrt(_U1[0]**2+_U1[1]**2)
	psiU1 = degrees(atan(_U1[1]/_U1[0]))
	print('_U1, U1, psiU1', _U1, U1, psiU1)
	print('\n')

	#Напряжение на двухполюсниках P1 и P2
	_U2 = complex_mul(_I1, _Z23)
	_U3 = _U2
	U2 = sqrt(_U2[0]**2+_U2[1]**2)
	U3 = U2
	psiU2 = degrees(atan(_U2[1]/_U2[0]))
	psiU3 = psiU2
	print('_U2, U2, psiU2', _U2, U2, psiU2)
	print('\n')

	#проверка
	tmp = complex_sum(_U, [-1*_U1[0], -1*_U1[1]])
	tmp = complex_sum(tmp, [-1*_U2[0], -1*_U2[1]])
	print('проверка: ', [round(i) for i in tmp])
	print('\n')

	#Ток, текущий через двухполюсник P1
	_I2 = complex_div(_U2, _Z2)
	I2 = sqrt(_I2[0]**2+_I2[1]**2)
	psiI2 = degrees(atan(_I2[1]/_I2[0]))
	print('_I2, I2, psiI2', _I2, I2, psiI2)
	print('\n')

	#Ток, текущий через двухполюсник P2
	_I3 = complex_div(_U3, _Z3)
	I3 = sqrt(_I3[0]**2+_I3[1]**2)
	psiI3 = degrees(atan(_I3[1]/_I3[0]))
	print('_I3, I3, psiI3', _I3, I3, psiI3)
	print('\n')

	#проверка по первому закону Кирхгофа
	tmp = complex_sum(_I1, [-1*_I2[0], -1*_I2[1]])
	tmp = complex_sum(tmp, [-1*_I3[0], -1*_I3[1]])
	print('проверка: ', [round(i) for i in tmp])
	print('\n')

	#проверка по фазовым углам
	phi1 = psiU1 - psiI1
	phi2 = psiU2 - psiI2
	phi3 = psiU3 - psiI3
	print(psiU1, psiI1, phi1)
	print(psiU2, psiI2, phi2)
	print(psiU3, psiI3, phi3)
	print('проверка: ', round(phiZ1 - phi1), round(phiZ2 - phi2), round(phiZ3 - phi3))

	#мощность на входе цепи
	P = E*I1*cos(radians(phiZ))
	print('P', P)


if __name__ == '__main__':
	main()