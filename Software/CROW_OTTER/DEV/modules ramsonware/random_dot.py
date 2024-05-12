from matplotlib import pyplot as plt
import random


def random_colors(number):
    alphabet = "0123456789ABCDEF"
    colors = []
    for _ in range(number):
        color = ['#']

        for _ in range(6):
            symbol = random.choice(alphabet)
            color.append(symbol)
        print(color)

def showplot(x,y,c):
    
    _,ax=plt.subplots(1, 1, figsize=(7,7),dpi=72)
    ax.scatter(x,y, s=100)

    plt.show()
    plt.close()



n = 5
x = list(random.sample(range(1,100),n))
y = list(random.sample(range(1,100),n))
c = random_colors(n)

#showplot(x,y,c)