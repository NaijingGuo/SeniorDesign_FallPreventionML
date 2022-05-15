import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

df = pd.read_csv('data_df.csv')
X = df.iloc[: , 1:-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1, test_size=0.2)
clf = MLPClassifier(solver = 'adam')
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test) 

from sklearn.metrics import accuracy_score
print("=====================================")
print("Accuracy Score of this model is:")
print(accuracy_score(y_test, y_pred))
from sklearn.metrics import classification_report
print(classification_report(y_true=y_test, y_pred= y_pred))

'''
MLP 1 hidden layer, 100 nodes
activation function: ReLU
solver: Adam
learning rate: 0.001
max epoch = 200
shuffle = True
'''
