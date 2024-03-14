import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from regresion import cars



# Wykres histogramu
plt.hist(cars['id_marki'], bins=10, edgecolor='k')
plt.title('Histogram Rozkładu Kolumny')
plt.xlabel('Wartości')
plt.ylabel('Liczność')
plt.show()


# Wykres gęstości
sns.kdeplot(cars['id_marki'], shade=True)
plt.title('Wykres Gęstości Rozkładu Kolumny')
plt.xlabel('Wartości')
plt.ylabel('Gęstość')
plt.show()
