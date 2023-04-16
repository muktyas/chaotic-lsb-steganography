import numpy as np
from PIL import Image
import time

# ~ r = np.array([[200,120]])
# ~ a = np.array([[100,50],[200,100],[150,10],[12,23],[23,34],[45,56],[67,78],[100,150]])

# ~ Image.fromarray(a.astype(np.uint8)).save('cover.png')
# ~ Image.fromarray(r.astype(np.uint8)).save('rahasia.png')

def log(x0, n):
	bar = np.zeros(n)
	for i in range(100):
		x0 = 3.9 * x0* (1 - x0)
	for i in range(n):
		x0 = 3.9 * x0* (1 - x0)
		bar[i] = x0 * 1000 % 3 + 1
	return bar.astype(np.uint8)

def sembunyikan(gb_rahasia, gb_cover, x0):
	waktu_awal = time.time()
	c = Image.open(gb_cover)
	r = Image.open(gb_rahasia)

	mc = np.array(c)
	mr = np.array(r)

	bc, kc = mc.shape
	br, kr = mr.shape

	mc_flat = mc.reshape(mc.size)
	mc_flat_asli = np.copy(mc_flat)
	mr_flat = mr.reshape(mr.size)

	mr_flat_bin = np.array([ format(i,'08b') for i in mr_flat ])

	#~ print mc_flat_asli
	#~ print mr_flat_bin
	mr_string = ''.join(mr_flat_bin)

	#~ print mr_string

	nbit_rahasia = 8 * br * kr
	ambils = log(x0, nbit_rahasia)
	#~ print ambils

	jmlkum = np.cumsum(ambils)
	#~ print jmlkum

	for i in range(nbit_rahasia):
		if jmlkum[i] > nbit_rahasia:
			nbit_lsb = i
			break
		else:
			nbit_lsb = nbit_rahasia

	#~ print nbit_lsb
	#~ print
	#~ print 'panjang mr_string:', len(mr_string)

	for i in range(nbit_lsb):
		# ~ nolkan beberapa bit terakhir
		nbit = ambils[i]
		
		#~ print nbit
		#~ print mc_flat[i], format(mc_flat[i],'08b')
		
		mc_flat[i] = mc_flat[i] >> nbit << nbit
		#~ print 'setelah dibuang ', nbit, 'menjadi', mc_flat[i], format(mc_flat[i],'08b')
		
		# ~ isi dengan string rahasia sebanyak n tadi
		bit_rahasia = mr_string[:nbit]
		int_rahasia = int(bit_rahasia, 2)
		
		#~ print bit_rahasia, int_rahasia
		
		mc_flat[i] = mc_flat[i] | int_rahasia
		
		mr_string = mr_string[nbit:]
		
		#~ print mc_flat[i]
		#~ print mr_string
			
		#~ print
	#~ print '#'*30
	#~ print mc_flat_asli[:10], mc_flat_asli[-5:]
	#~ print mc_flat[:10], mc_flat[-5:]
	#~ print mr_string
	#~ print
	print 'x0:', x0
	print 'baris, kolom:', br, kr
	print 'nbit_lsb:', nbit_lsb

	jadi = mc_flat.reshape(bc, kc).astype(np.uint8)
	stegano = Image.fromarray(jadi)
	stegano.save('stegano.png')
	print
	print 'waktu proses penyisipan:', time.time() - waktu_awal,' detik.'

sembunyikan('peppers_gray_100.png', 'cover.png', 0.123)