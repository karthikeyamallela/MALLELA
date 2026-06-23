import matplotlib.pyplot as plt

models = [
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "SVM",
    "XGBoost",
    "VQC"
]

accuracy = [
    0.5617,
    0.6125,
    0.6558,
    0.5983,
    0.6467,
    0.3617
]

plt.figure()

plt.bar(models, accuracy)

plt.xlabel("Models")

plt.ylabel("Accuracy")

plt.title("Model Accuracy Comparison")

plt.xticks(rotation=30)

plt.show()