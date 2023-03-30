import json
import yaml
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

params = yaml.safe_load(open('params.yaml'))

# split dataset
df = pandas.read_csv("./data/clean.csv")
X=df['x'].to_numpy()
y=df['y'].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# fit model
predictor = LogisticRegression(solver=params['solver'])
predictor.fit(X=X_train.reshape(-1,1), y=y_train)

# eval train
pred_labels = predictor.predict(X_test.reshape(-1,1))
true_labels = y_test
acc = accuracy_score(y_pred=pred_labels, y_true=true_labels)
metrics = {'train_acc': acc}
with open('metrics.json', 'w') as f:
    json.dump(metrics, f)