#implement base on http://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html
from collections import namedtuple
import random

#generated from https://www.mobilefish.com/services/prime_numbers_generator_checker/prime_numbers_generator_checker.php
prime_list = [98764321234,98764241,454646503,454451,84516167,8451616171,812151127,12315461,123456791,
			123456803,123456811,123456821,123456841,123456871,123456887,123456919,123456937,123456967]

PrivateKey = namedtuple('PrivateKey',['n','d'])
PublicKey  = namedtuple('PublicKey',['n','e'])

def quick_power_mod(n,p,mod):
	r = n % mod
	k = 1
	while p>1:
		if (p & 1) > 0:
			k = (k * r) % mod
		r = (r * r) % mod
		p = p >> 1
		
	return (r * k) % mod


#第四步，随机选择一个整数e，条件是1< e < φ(n)，且e与φ(n) 互质。（实际应用中，常常选择65537。故这里直接返回65537）
def choice_e(phi_n):
	return 65537


def exgcd(a,b):
	if b == 0:
		return a, 1, 0
	else:
		g, x, y = exgcd(b,a%b)
		d = x - int(a / b) * y
		return g, y, d

#ed ≡ 1 (mod φ(n))
def evaluate_d(phi_n,e):
	_,__,d = exgcd(phi_n,e)
	if d < 0:
		d = d + phi_n
	return d


def encrypt(public_key,m):
	encrypted_m = quick_power_mod(m, public_key.e, public_key.n)
	return encrypted_m
	
def decrypt(private_key,encrypted_m):
	m = quick_power_mod(encrypted_m, private_key.d, private_key.n)
	return m

def main():
	#第一步，随机选择两个不相等的质数p和q。
	p,q = random.sample(prime_list,2)
	print('p:',p,',q:',q)
	#第二步，计算p和q的乘积n。
	n = p * q
	#第三步，计算n的欧拉函数φ(n)。 phi(n) = (p-1) * (q-1)
	phi_n = (p-1) * (q-1)
	e = choice_e(phi_n)
	#第五步，计算e对于φ(n)的模反元素d。所谓"模反元素"就是指有一个整数d，可以使得ed被φ(n)除的余数为1。
	# ed ≡ 1 (mod φ(n)) 等价于 ed - 1 = kφ(n)
	#于是，找到模反元素d，实质上就是对下面这个二元一次方程求解。
	# ex + φ(n)y = 1
	d = evaluate_d(phi_n,e)
	
	#第六步，将n和e封装成公钥，n和d封装成私钥。
	public_key  = PublicKey._make((n,e))
	private_key = PrivateKey._make((n,d))
	print(public_key)
	print(private_key)
	message = random.randint(0,0xffffffff)
	print('message:',message)
	encrypted_message = encrypt(public_key,message)
	print("encrypted_message:",encrypted_message)
	
	decrypted_message = decrypt(private_key,encrypted_message)
	print("decrypted_message:",decrypted_message)
	


if __name__ == '__main__':
	main()
	
# 有问题	
# PublicKey(n=44902853270206744702, e=65537)
# PrivateKey(n=44902853270206744702, d=13485175642940345549)
# message: 1003519300
# encrypted_message: 25652184213593662914
# decrypted_message: 38511012732324671620
	
# p: 98764321234 ,q: 123456937
# PublicKey(n=12193140584433700258, e=65537)
# PrivateKey(n=12193140584433700258, d=6389505526574356505)
# message: 3160296762
# encrypted_message: 3776646186332417096
# decrypted_message: 6159067747137684200
	
	
	
	
	
	