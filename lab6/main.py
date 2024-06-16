import cv2
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)       # NumPy буде показувати всі елементи масиву без скорочень


def new_size_wm(img, height, wight):
    # цикл для збільшення watermark доки по вертикалі
    while True:
        img = np.concatenate((img, img), axis=0)
        if img.shape[0] > height:
            break

    # цикл для збільшення watermark доки по горизонталі
    while True:
        img = np.concatenate((img, img), axis=1)
        if img.shape[1] > wight:
            break

    # підганяємо під розміри контейнера
    img = img[:height, :wight]
    return img


def container_with_WM(container, watermark, bit):
    height_c, wight_c, _ = container.shape      # _ - кількість каналів
    height_w, wight_w = watermark.shape

    # ----------------------------------
    if height_w > height_c or wight_w > wight_c:
        watermark = watermark[:height_c, :wight_c]

    if height_w < height_c or wight_w < wight_c:
        watermark = new_size_wm(watermark, height_c, wight_c)


    # ----------------------------------
    # перетворюємо в масив з {0,1}(для пікселя кожного піксель)
    # 10110100(180) AND 00000001 > 00000000
    k = watermark & 1
    # потоки
    r, g, b = cv2.split(container)

    # перставляємо інтенсивність синього коляру у 8 бітах
    b_unpacked = np.unpackbits(b[:, :, np.newaxis], axis=2)

    # змінюємо певний біт кожного пікселя синього каналу на відповідний біт
    b_unpacked[:, :, -bit] = watermark[:, :]

    # перетворюємо бітове представлення в int8
    b_packed = np.packbits(b_unpacked, axis=2)
    b_new = b_packed.reshape(b_packed.shape[0], b_packed.shape[1])


    img_with_WM = cv2.merge((r, g, b_new))
    return img_with_WM


def WM_with_container(container, bit):
    # за останнім біт і є піксель WM
    _, _, b_with_WM = cv2.split(container)
    unpacked_b = np.unpackbits(b_with_WM[:, :, np.newaxis], axis=2)
    WM = unpacked_b[:, :, -bit]
    return WM


def text_to_bit(text):

    text_TO_1_0 = ''.join(format(ord(symbol), '08b') for symbol in text)
    return text_TO_1_0


def container_with_text(container, text, bit):

    b_text = text_to_bit(text)
    height_c, wight_c, _ = container.shape
    length_text = len(b_text)

    # перевірка розміру тексту
    if height_c * wight_c < length_text:
        raise ValueError("Текст повинен бути меншим")

    r, g, b = cv2.split(container)
    b_unpacked = np.unpackbits(b[:, :, np.newaxis], axis=2)

    for i in range(b_unpacked.shape[0]):
        for j in range(b_unpacked.shape[1]):
            if b_text == '':
                break
            b_unpacked[i, j, -bit] = b_text[0]
            b_text = b_text[1:]

    # перетворюємо бітове представлення в int8
    b_packed = np.packbits(b_unpacked, axis=2)
    b_new = b_packed.reshape(b_packed.shape[0], b_packed.shape[1])


    img_with_WM = cv2.merge((r, g, b_new))
    return img_with_WM, length_text


def binary_to_text(binary_text):

    # строку поділяємо по 8 бітів
    symbols = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]

    # з 8 бітів в символ ASCII
    text = ''.join([chr(int(symbol, 2)) for symbol in symbols])

    return text


def text_with_img(container, length_text):
    _, _, b_mod = cv2.split(container)
    b_mod_unpacked = np.unpackbits(b_mod[:, :, np.newaxis], axis=2)
    text_from_im = b_mod_unpacked[:, :, -1].flatten()
    encrypted_text = text_from_im[:length_text]
    encrypted_text_str = ''.join(map(str, encrypted_text))
    return binary_to_text(encrypted_text_str)

# ----------------------------------
WM_img = cv2.imread('WM.png', cv2.IMREAD_GRAYSCALE)
_, wm_binary = cv2.threshold(WM_img, 155, 255, cv2.THRESH_BINARY)

input_img = cv2.imread('InputImage.png')
input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)

b_image = cv2.imread('hot_dog.png')
b_image = cv2.cvtColor(b_image, cv2.COLOR_BGR2RGB)

s_image = cv2.imread('pizza.jpg')
s_image = cv2.cvtColor(s_image, cv2.COLOR_BGR2RGB)

im, l = container_with_text(input_img, 'ASDHSADH', 1)
text_with_img(im, l)
# print(text_with_img(im, l))

images = []

for bit_value in range(1, 9):
    image_with_text = container_with_WM(input_img, wm_binary, bit_value)
    images.append(image_with_text)

plt.figure(figsize=(16, 12))

for n in range(8):
    plt.subplot(3, 3, n + 1)
    plt.imshow(images[n])
    plt.title(f'біт: {n + 1}')
    plt.axis('off')

wms = []
for n, image in enumerate(images):
    wm = WM_with_container(image, n + 1)
    wms.append(wm)

plt.figure(figsize=(16, 12))

for n in range(8):
    plt.subplot(3, 3, n + 1)
    plt.imshow(wms[n], cmap='gray')
    plt.title(f'біт: {n + 1}')
    plt.axis('off')

big = container_with_WM(b_image, wm_binary, 1)
big_WM = WM_with_container(test_big, 1)
small = container_with_WM(s_image, wm_binary, 1)
small_WM = WM_with_container(test_small, 1)
plt.figure(figsize=(16, 12))
plt.subplot(2, 3, 1)
plt.imshow(b_image)

plt.subplot(2, 3, 2)
plt.imshow(big)

plt.subplot(2, 3, 3)
plt.imshow(big_WM, cmap="gray")

plt.subplot(2, 3, 4)
plt.imshow(s_image)

plt.subplot(2, 3, 5)
plt.imshow(small)

plt.subplot(2, 3, 6)
plt.imshow(small_WM, cmap="gray")










