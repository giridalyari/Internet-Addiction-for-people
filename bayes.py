import category_encoders as ce
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import RobustScaler

import basic

# create dataframe
df = basic.create_ml_dataframe()
df = df[["Age", "Gender", "Student", "Confident", "Happy", "Addicted"]]
priori = (df["Addicted"].value_counts()/len(df) * 100).tolist()

# Declare feature vector and target variable
X = df.drop(['Addicted'], axis=1)
y = df['Addicted']

# Split X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# encode remaining variables with one-hot encoding
encoder = ce.OneHotEncoder(cols=["Age", "Gender", "Student", "Confident", "Happy"])
X_train = encoder.fit_transform(X_train)
X_test = encoder.transform(X_test)

# Feature scaling
scaler = RobustScaler()
cols = X_train.columns
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_train = pd.DataFrame(X_train, columns=[cols])
X_test = pd.DataFrame(X_test, columns=[cols])

# Instantiate the model
gnb = GaussianNB()

# fit the model
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)

# Predict the results
y_pred_train = gnb.predict(X_train)
print(f"Accuracy score: {accuracy_score(y_train, y_pred_train)}")

# check null accuracy score
null_accuracy_list = (y_test.value_counts()).tolist()
null_accuracy = null_accuracy_list[0]/(null_accuracy_list[0]+null_accuracy_list[1])
print(f"Null accuracy: {null_accuracy}")

# Print the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
cm_matrix = pd.DataFrame(data=cm, columns=['Actual Positive:1', 'Actual Negative:0'],
                         index=['Predict Positive:1', 'Predict Negative:0'])

sns.heatmap(cm_matrix, annot=True, linewidths=0.5, linecolor="red", fmt=".0f")
plt.show()
