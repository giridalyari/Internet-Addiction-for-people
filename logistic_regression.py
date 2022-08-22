import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import basic

df = basic.create_ml_dataframe()
df = df[["Age", "Gender", "Student", "Confident", "Happy", "Addicted"]]

# Replace string values with integers
df["Age"].replace({"0-15": 0, "16-19": 1, "20-24": 2, "28 +": 3}, inplace=True)
df["Gender"].replace({"kobieta": 0, "mężczyzna": 1}, inplace=True)
df["Confident"].replace({"not confident": 0, "semi-confident": 1, "confident": 2}, inplace=True)
df["Happy"].replace({"not happy": 0, "semi-happy": 1, "happy": 2}, inplace=True)
df["Addicted"].replace({"not addicted": 0, "semi-addicted": 1, "addicted": 2}, inplace=True)

X = df.drop(['Addicted'], axis=1)
y = df['Addicted']

# Split the dataset into training (70%) and testing (30%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Instantiate the model
log_regression = LogisticRegression()

# Fit the model using the training data
log_regression.fit(X_train, y_train)

# Define metrics
y_pred = log_regression.predict_proba(X_test)[::, 1]
fpr, tpr, _ = metrics.roc_curve(y_test, y_pred)

# Create ROC curve
plt.plot(fpr, tpr)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
