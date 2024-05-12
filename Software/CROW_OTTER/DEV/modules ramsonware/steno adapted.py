import png
import base64
import os
from cryptography.fernet import Fernet

ENDOFMESSAGE = "0100100101010101010101100100111101010010010001010011100101000111010101000101010101010110010101000101010100110000010001100100100001010010010100110100010100111101"


def encode_message_as_bytestring(message):
	b64 = message.encode("utf8")
	bytes_ = base64.encodebytes(b64)
	bytestring = "".join(["{:08b}".format(x) for x in bytes_])
	bytestring += ENDOFMESSAGE
	return bytestring


def get_pixels_from_image(fname):
	img = png.Reader(fname).read()
	pixels = img[2]
	return pixels


def encode_pixels_with_message(pixels, bytestring):
	'''modifies pixels to encode the contents from bytestring'''

	enc_pixels = []
	string_i = 0
	for row in pixels:
		enc_row = []
		for i, char in enumerate(row):
			if string_i >= len(bytestring): 
				pixel = row[i]
			else:
				if row[i] % 2 != int(bytestring[string_i]):
					if row[i] == 0:
						pixel = 1
					else:
						pixel = row[i] - 1
				else:
					pixel = row[i]
			enc_row.append(pixel)
			string_i += 1

		enc_pixels.append(enc_row)
	return enc_pixels


def write_pixels_to_image(pixels, fname):
	png.from_array(pixels, 'RGB').save(fname)


def decode_pixels(pixels):
	bytestring = []
	for row in pixels:
		for c in row:
			bytestring.append(str(c % 2))
	bytestring = ''.join(bytestring)
	message = decode_message_from_bytestring(bytestring)
	return message


def decode_message_from_bytestring(bytestring):
	bytestring = bytestring.split(ENDOFMESSAGE)[0]
	message = int(bytestring, 2).to_bytes(len(bytestring) // 8, byteorder='big')
	message = base64.decodebytes(message).decode("utf8")
	return message


def main():

    # This builds the encryption key. (Vital for dencryption.)
	key = Fernet.generate_key()

	text_key = key.decode('utf-8')
	print (text_key)
	in_image = f'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64\\HACKED.png'
	in_message = text_key

	print("-ENCODING-")
	pixels = get_pixels_from_image(in_image)
	bytestring = encode_message_as_bytestring(in_message)
	epixels = encode_pixels_with_message(pixels, bytestring)
	write_pixels_to_image(epixels, in_image + "-enc.png")

	#--------------------------------------------------------
	#--------------------------------------------------------

	# This will open it and read the file.
	with open (r'C:\Users\udgo1\OneDrive\Escritorio\df\df.txt', 'rb') as f:
		content = f.read()
	
	# This will use they key to encrypt what was read.
	content_encripted = Fernet(key).encrypt(content)
	
	# This will write over the file with the same information but encrypted. 
	with open (r'C:\Users\udgo1\OneDrive\Escritorio\df\df.txt', 'wb') as f:
		f.write(content_encripted)

	#--------------------------------------------------------
	#--------------------------------------------------------
		
	print("-DECODING-")
	pixels = get_pixels_from_image(in_image + "-enc.png")
	text = decode_pixels (pixels)
	b_text = text.encode('ascii')
	print (text)
	print (b_text)
	

	#--------------------------------------------------------
	#--------------------------------------------------------

	with open (r'C:\Users\udgo1\OneDrive\Escritorio\df\df.txt', 'rb') as f:                        # Open the list and read it
		content_encripted = f.read()
	content = Fernet(b_text).decrypt(content_encripted)    # Use the key to decrypt the files
	with open (r'C:\Users\udgo1\OneDrive\Escritorio\df\df.txt', 'wb') as f:                        # Writte over the files with the decrypted data.
		f.write(content)

if __name__ == "__main__":
	main()