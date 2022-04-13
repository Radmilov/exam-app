import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

def produceGraphForStudentAndExams(exams):
    data = {'Predmeti': exams.keys(), 'Ocene': exams.values()}
    df = pd.DataFrame(data=data)
    print(df['Ocene'].value_counts())
    predmetCount = {}
    for predmet in df['Predmeti']:
        predmet = predmet[0:2]
        if predmet in predmetCount:
            predmetCount[predmet] = predmetCount[predmet] + 1
        else:
            predmetCount[predmet] = 1
    print(predmetCount)
    ocena_avg = []
    ocena_avg.append(0)
    print(df['Ocene'])
    for ocena in df['Ocene']:
        print(ocena)
        ocena_avg.append((sum(ocena_avg) + ocena) / (len(ocena_avg)+1))

    print(ocena_avg)
    fig, axs = plt.subplot_mosaic([['upper left', 'upper right'],
                                  ['down', 'down']])

    #Broj ocena
    brojOcena = df['Ocene'].value_counts()
    axs['upper left'].pie(brojOcena.values, labels=brojOcena.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90)
    axs['upper left'].axis('equal')

    #Broj ocena po oznaci predmeta
    y_pos = np.arange(len(predmetCount))
    axs['upper right'].barh(y_pos, predmetCount.values(), align='center')
    axs['upper right'].set_yticks(y_pos, labels=predmetCount.keys())
    axs['upper right'].set_xlabel('Broj ocena')
    axs['upper right'].set_title('Ocene po grupi predmeta')


    axs['down'].plot(ocena_avg, label="Kretanje prosecne ocene sa brojem ocena")
    plt.show()
    buf = BytesIO()
    plt.savefig('dz10graf.png')
    buf.seek(0)
    return buf

