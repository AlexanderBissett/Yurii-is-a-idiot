import sys, time

def main():
                  
		filename = input(" Please Input The File Name: ")
		size = input(" Please Input The Increase Size: ")
		mbkb = input(" Please Input The Unit (KB/MB): ")
		size = int(size)
		
		f = open(filename, "ab")
		if mbkb == "KB":
			b_size = size * 1024
		elif mbkb == "MB":
			b_size = size * 1048576
		else:
			print ("Please Use KB Or MB")
			sys.exit(0)
		
		BufSize = 256
		for i in range(b_size//BufSize):
			f.write(str.encode('0' * BufSize))
		f.close()
		time.sleep(1)
		sys.exit(0)

if __name__ == "__main__":
	main()
	