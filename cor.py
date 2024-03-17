from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

cars = pd.read_pickle('cars.pickle')

cars.hist(bins=20)

iris = datasets.load_iris() #wczytywanie danych
X = np.array(cars.drop({'cena','id'}, axis=1))
y = np.array(cars['cena'])
X = StandardScaler().fit_transform(X) #standaryzacja danych

df = pd.DataFrame(np.hstack((X,y[:, np.newaxis])),
columns= cars.loc[:, ~cars.columns.isin(['cena'])].columns)

print(np.unique(y))
#unikalne wartości w wektorze y – w ten sposób można sprawdzić, jakie
#klasy znajdują się w wektorze y i jakie są ich etykiet

from sklearn.decomposition import PCA
import pandas as pd
pca = PCA(n_components = 2)
#wyznaczone zostaną tylko dwie pierwsze składowe główne
principal_components = pca.fit_transform(X)
pca_df = pd.DataFrame(data = (np.hstack((principal_components,
y[:, np.newaxis]))),
columns = ['PC1', 'PC2', 'target numerical'])

from matplotlib import pyplot as plt
fig = plt.figure(figsize = (8,8)) #określenie wymiarów obrazu
ax = fig.add_subplot(1,1,1) #obraz ma się składać z jednego wykresu

ax.set_xlabel('Pierwsza składowa główna (PC1)', fontsize = 15)
#podpis osi X
ax.set_ylabel('Druga składowa główna (PC2)', fontsize = 15)
#podpis osi Y
ax.set_title('Rzut obiektów na płaszczyznę PC1-PC2', fontsize = 20)
#tytuł wykresu
targets = [0,1,2] #lista etykiet, które znajdują się w zbiorze danych
colors = ['r', 'g', 'b']
#lista kolorów, które posłużą do oznaczenia obiektów należących do
#różnych klas
for target, color in zip(targets,colors):
 indicesToKeep = pca_df['target numerical'] == target
 ax.scatter(pca_df.loc[indicesToKeep, 'PC1'],
pca_df.loc[indicesToKeep, 'PC2'],
c = color, s = 50)
ax.legend(targets, title = 'Gatunek irysa') #legenda
ax.grid() #włączenie siatki na tle wykres

plt.show()