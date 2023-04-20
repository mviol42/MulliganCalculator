from statistics import mode
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np


def train():
    df = pd.read_csv("./hand.csv")
    df.head()
    X = df.drop('Kept', axis=1)
    y = df['Kept']

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.2, random_state=42)

    tf.random.set_seed(42)
    np.random.seed(31415)

    keras_model = train_keras(X_train, y_train)
    y_pred_k = keras_model.predict(X_test)
    eval('keras', y_test, y_pred_k)

    rf_model = train_random_forest(X_train, y_train)
    y_pred_rf = rf_model.predict_proba(X_test)[:, 1]
    eval('random forest', y_test, y_pred_rf)

    return keras_model


def train_keras(X_train, y_train):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        loss=tf.keras.losses.binary_crossentropy,
        optimizer=tf.keras.optimizers.Adam(lr=0.03),
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name='accuracy'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )

    model.fit(X_train, y_train, epochs=100)
    print(model.summary())

    return model


def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(max_depth=3, n_estimators=10)

    model.fit(X_train, y_train)

    return model


def eval(name, y_test, y_pred):
    fpr, tpr, thresholds_rf = roc_curve(y_test, y_pred)
    auc_reference = auc(fpr, tpr)

    plt.figure(1)
    plt.grid()
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, label='{} (area = {:.3f})'.format(name, auc_reference))
    # plt.plot(fpr_rf, tpr_rf, label='RF (area = {:.3f})'.format(auc_rf))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    train()
