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
		bar[i] = int(x0 * 1000 % 3 + 1)
	return bar.astype(np.uint8)

def buka(gb_stegano, x0, baris, kolom, banyak_bit):
	waktu_awal = time.time()
	s = Image.open(gb_stegano)
	nbit_lsb = banyak_bit
	br, kr = baris, kolom

	ms = np.array(s)


	ms_flat = ms.reshape(ms.size)

	ambils = log(x0, nbit_lsb+1)
	print(ambils)

	jmlkum = np.cumsum(ambils)
	print(jmlkum[nbit_lsb-1], jmlkum[nbit_lsb])

	selisih_bit_terakhir = jmlkum[nbit_lsb] - br * kr * 8
	print(selisih_bit_terakhir)
	# ~ print jmlkum

	# ~ for i in range(nbit_rahasia):
		# ~ if jmlkum[i] > nbit_rahasia:
			# ~ nbit_lsb = i
			# ~ break
		# ~ else:
			# ~ nbit_lsb = nbit_rahasia

	# ~ print nbit_lsb
	# ~ print

	lsb_string = ''
	for i in range(nbit_lsb):
		# ~ ambil nbit_lsb
		nbit = ambils[i]
		
		#~ print nbit
		topeng = 2 ** nbit - 1
		
		#~ print 'nilai piksel:', ms_flat[i], format(ms_flat[i], '08b')
		ambil_bit = ms_flat[i] & topeng
		#~ print ambil_bit, format(ambil_bit, '08b')
		
		# jangan semua bit yang disimpan
		sl = 8 - nbit
		
		ambil_bin = format(ambil_bit, '08b')
			
		
		lsb_string = lsb_string + str(ambil_bin[sl:])
		#~ print 'string_rahasia:', lsb_string
		#~ print '-'*20, '\n'

	#~ banyak_piksel = int(len(lsb_string)/8)
	banyak_piksel = br * kr
	mbuka = np.zeros(banyak_piksel)
	for i in range(banyak_piksel):
		string_pixel = lsb_string[:8]
		mbuka[i] = int(string_pixel, 2)
		lsb_string = lsb_string[8:]
	print(lsb_string)
	mbuka_reshape = mbuka.reshape(br, kr).astype(np.uint8)

	print(mbuka_reshape)
	Image.fromarray(mbuka_reshape).save('terbuka.png')
	print()
	print('Alhamdulillah file berhasil terbuka dengan nama: terbuka.png')
	print('waktu buka:', time.time() - waktu_awal,' detik.')

try:
	buka('cover_stegano.png', 0.123, 100, 100, 39280)
except ValueError:
	print('-'*30)
	print('nbit_lsb nya kurang tepat,')
	print('file belum berhasil terbuka.')
