from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import os


class AESUtil:
	'''
	AES Util
	block_size : must up to a multiple of 16
	iv : IV length must be 16 bytes long
	'''
	CHARSET = 'utf-8'
	CHUNK_SIZE = 1024
	def __init__(self,key_bytes,block_size = AES.block_size,iv = 'akame'):
		self.key_bytes = self._pading(key_bytes,block_size)
		self.block_size = block_size
		self.iv_bytes = self._pading(iv.encode(AESUtil.CHARSET),16)
		self.crypter = AES.new(self.key_bytes,AES.MODE_CBC,self.iv_bytes)
		
	def _pading(self,src_bytes,block_size):
		n = block_size - (len(src_bytes) % block_size)
		src_bytes += b'\0' * n
		return src_bytes
	
	def _unpading(self,src_bytes):
		return src_bytes.rstrip(b'\0')
	
	def encrypt(self,src_bytes,pading=True):
		if pading:
			src_bytes = self._pading(src_bytes,self.block_size)
		encrypted_bytes = self.crypter.encrypt(src_bytes)
		return encrypted_bytes
	
	def decrypt(self,encrypted_bytes,unpading=True):
		src_bytes = self.crypter.decrypt(encrypted_bytes)
		if unpading:
			return self._unpading(src_bytes)
		else:
			return src_bytes
		
	def _ensure_path(self,path):
		parent_path = os.path.abspath(os.path.dirname(path))
		if not os.path.exists(parent_path):
			os.makedirs(parent_path)
		
	def encrypt_file(self,infile_path,outfile_path):
		assert os.path.exists(infile_path)
		self._ensure_path(outfile_path)
		with open(infile_path,'rb') as fin:
			with open(outfile_path,'wb') as fout:
				while True:
					data = fin.read(AESUtil.CHUNK_SIZE)
					if len(data) > 0:
						dest = self.encrypt(data,len(data) != AESUtil.CHUNK_SIZE)
						fout.write(dest)
					else:
						break
						
	def decrypt_file(self,infile_path,outfile_path):
		assert os.path.exists(infile_path)
		self._ensure_path(outfile_path)
		with open(infile_path,'rb') as fin:
			with open(outfile_path,'wb') as fout:
				while True:
					data = fin.read(AESUtil.CHUNK_SIZE)
					if len(data) > 0:
						#只有在最后一个chunk中才需要pading或unpading
						dest = self.decrypt(data,len(data) != AESUtil.CHUNK_SIZE)
						fout.write(dest)
					else:
						break
		
	
def test_encrypt():
	msg = input("input_message:")
	key = input("input_key:")
	util = AESUtil(key.encode('utf-8'))
	dest_bytes = util.encrypt(msg.encode('utf-8'))
	print(b2a_hex(dest_bytes).decode('utf-8'))
	# print(b2a_hex(dest_bytes))
	
	
def test_decrypt():
	encrypt_hex_str = input("encrypt_hex_str:")
	key = input("input_key:")
	util = AESUtil(key.encode('utf-8'))
	src_bytes = util.decrypt(a2b_hex(encrypt_hex_str))
	print(src_bytes.decode('utf-8'))
	# print(b2a_hex(src_bytes))
	
	
def main():
	print("1:test_encrypt 2:test_decrypt")
	if input("input:") == '1':
		test_encrypt()
	else:
		test_decrypt()
	
def main1():
	# can't use the same one AESUtil instance to decrypt after encrypted.
	util = AESUtil('secure'.encode('utf-8'))
	util.encrypt_file('a.jpg','aa.enc')
	util = AESUtil('secure'.encode('utf-8'))
	util.decrypt_file('aa.enc','aaa.jpg')
if __name__ == '__main__':
	main1()
	