from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_and_test_classifier(X, y):
    """
    Train and test SVM classifier with guaranteed 2-class support
    """

    # 🚨 SAFETY CHECK (VERY IMPORTANT)
    unique_classes = set(y)
    if len(unique_classes) < 2:
        raise ValueError("Classifier received only one class")

    # ✅ Stratified split to preserve class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        stratify=y,
        random_state=42
    )

    # Train SVM
    clf = SVC(kernel="rbf", gamma="scale")
    clf.fit(X_train, y_train)

    # Predict
    y_pred = clf.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

