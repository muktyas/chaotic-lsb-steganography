import cv2
import os

if not os.path.isdir('png'):
  os.mkdir('png')


for file in os.listdir('.'):
  # print(file)
  
  if file.endswith('.tif'):
    filename, ext = os.path.splitext(file)
    gb = cv2.imread(file)
    if (gb[:, :, 0] == gb[:, :, 1]).all():
      gb1 = gb[:, :, 0]
    else:
      gb1 = gb
    cv2.imwrite(f'./png/{filename}.png', gb1)
    print(f'{filename}.png saved on folder png.')
