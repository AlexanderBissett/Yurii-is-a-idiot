import subprocess

Data = subprocess.check_output(['wmic', 'process', 'list', 'brief'])
a = str(Data)

try:
    for i in range(len(a)):
        line = a.split("\\r\\r\\n")[i]
        line = line.split()
        print(line[1])
except IndexError as e:
    print("All Done")