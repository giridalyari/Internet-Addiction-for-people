import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import metrics

import basic
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

# create dataframe
df = basic.create_ml_dataframe()
df = df[["Age", "Gender", "Student", "Confident", "Happy", "Addicted"]]

# Replace string values with integers
df["Age"].replace({"0-15": 0, "16-19": 1, "20-24": 2, "28 +": 3}, inplace=True)
df["Gender"].replace({"kobieta": 0, "mężczyzna": 1}, inplace=True)
df["Confident"].replace({"not confident": 0, "semi-confident": 1, "confident": 2}, inplace=True)
df["Happy"].replace({"not happy": 0, "semi-happy": 1, "happy": 2}, inplace=True)
df["Addicted"].replace({"not addicted": 0, "semi-addicted": 1, "addicted": 2}, inplace=True)

correlation = df.corr()
print(correlation)

plt.figure(figsize=(10, 8))
plt.title('Correlation of Attributes')
a = sns.heatmap(correlation, square=True, annot=True, fmt='.2f', linecolor='white')
a.set_xticklabels(a.get_xticklabels(), rotation=90)
a.set_yticklabels(a.get_yticklabels(), rotation=30)
plt.show()

X = df.iloc[:, :-1]  # attribute
y = df.iloc[:, 5]  # labels

# Split X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Instantiate the model
knn = KNeighborsClassifier(n_neighbors=5, algorithm="ball_tree", metric="minkowski")
# Fit the model to the training set
knn.fit(X_train, y_train)
# Predict test-set results
y_pred = knn.predict(X_test)

# Visualize confusion matrix with seaborn heatmap
cm = confusion_matrix(y_test, y_pred)
cm_matrix = pd.DataFrame(data=cm, columns=['Actual Positive:1', 'Actual Negative:0'],
                         index=['Predict Positive:1', 'Predict Negative:0'])

sns.heatmap(cm_matrix, annot=True, linewidths=0.5, linecolor="red", fmt=".0f")
plt.show()

ac = round(accuracy_score(y_test, y_pred), 2)
print("\n\n")
print(ac)

fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred)

# Create ROC curve
plt.plot(fpr, tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
