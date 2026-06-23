# =====================================================
# HYBRID IDS PROJECT
# Classical ML vs VQC vs QCNN
# FIXED & REWRITTEN VERSION
# =====================================================

import os
import time
import joblib
import numpy as np
import pandas as pd
import pennylane as qml
import pennylane.numpy as qnp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, label_binarize
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_curve,
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


# =====================================================
# SETTINGS
# =====================================================

N_QUBITS      = 10
N_LAYERS      = 3
EPOCHS        = 30
BATCH_SIZE    = 32
SAMPLE_SIZE   = 15000
LEARNING_RATE = 0.05

# VQC weight layout: N_LAYERS x N_QUBITS x 3 rotations = flat size
VQC_N_WEIGHTS  = N_LAYERS * N_QUBITS * 3
# QCNN weight layout: one RY per qubit in conv layer = flat size
QCNN_N_WEIGHTS = N_QUBITS

USE_SAVED_RESULTS = True # set True to skip training and load cached results

os.makedirs("results", exist_ok=True)
os.makedirs("models",  exist_ok=True)


# =====================================================
# DATA LOADING & PREPROCESSING
# =====================================================

print("=" * 60)
print("Loading dataset...")
print("=" * 60)

df = pd.read_csv("data/iot_combined.csv")

POSSIBLE_LABELS = ["Label", "label", "Attack", "attack", "Category", "Class"]
target_col = next((c for c in POSSIBLE_LABELS if c in df.columns), None)

if target_col is None:
    raise ValueError(f"Label column not found. Columns: {list(df.columns)}")

print(f"Target column: {target_col}")

y_raw = df[target_col]
X_raw = df.drop(columns=[target_col])

X_raw = X_raw.select_dtypes(include=[np.number])
X_raw = X_raw.replace([np.inf, -np.inf], np.nan).fillna(0)

class_names = sorted(y_raw.unique().tolist())
label_map   = {c: i for i, c in enumerate(class_names)}
y_encoded   = y_raw.map(label_map)

n_classes = len(class_names)
print(f"Classes ({n_classes}): {class_names}")

scaler   = MinMaxScaler()
X_scaled = scaler.fit_transform(X_raw)
X_scaled = X_scaled[:, :N_QUBITS]   # keep only N_QUBITS features

X_sample, _, y_sample, _ = train_test_split(
    X_scaled, y_encoded,
    train_size=SAMPLE_SIZE,
    stratify=y_encoded,
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X_sample, y_sample,
    test_size=0.2,
    stratify=y_sample,
    random_state=42,
)

X_train = np.array(X_train, dtype=np.float64)
X_test  = np.array(X_test,  dtype=np.float64)
y_train = np.array(y_train, dtype=np.int64)
y_test  = np.array(y_test,  dtype=np.int64)

y_test_bin = label_binarize(y_test, classes=list(range(n_classes)))

print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")


# =====================================================
# HELPERS
# =====================================================

def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum()


def cross_entropy_loss(logits, y_batch):
    """Numerically stable softmax cross-entropy for qnp arrays."""
    shifted = logits - qnp.max(logits, axis=1, keepdims=True)
    exp_l   = qnp.exp(shifted)
    probs   = exp_l / qnp.sum(exp_l, axis=1, keepdims=True)
    nll     = -qnp.log(probs[range(len(y_batch)), y_batch] + 1e-9)
    return qnp.mean(nll)


# =====================================================
# LOAD SAVED RESULTS (optional fast path)
# =====================================================

if USE_SAVED_RESULTS and os.path.exists("results/final_results.pkl"):
    print("\nLoading saved results...")
    results         = joblib.load("results/final_results.pkl")
    classical_preds = joblib.load("results/classical_preds.pkl")
    classical_probs = joblib.load("results/classical_probs.pkl")
    vqc_preds       = joblib.load("results/vqc_preds.pkl")
    vqc_probs       = joblib.load("results/vqc_probs.pkl")
    qcnn_preds      = joblib.load("results/qcnn_preds.pkl")
    qcnn_probs      = joblib.load("results/qcnn_probs.pkl")
    training_times  = joblib.load("results/training_times.pkl")

else:

    results         = {}
    classical_preds = {}
    classical_probs = {}
    training_times  = {}

    # =================================================
    # CLASSICAL ML
    # =================================================

    print("\n" + "=" * 60)
    print("Training Classical Models")
    print("=" * 60)

    classical_models = {
        "Logistic Regression": LogisticRegression(max_iter=500),
        "Decision Tree":       DecisionTreeClassifier(),
        "Random Forest":       RandomForestClassifier(n_estimators=100),
        "SVM":                 SVC(probability=True),
        "XGBoost":             XGBClassifier(eval_metric="mlogloss", verbosity=0),
    }

    for name, model in classical_models.items():
        print(f"\n--- {name} ---")
        t0 = time.time()
        model.fit(X_train, y_train)
        training_times[name] = time.time() - t0

        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)
        acc   = accuracy_score(y_test, preds)

        print(f"Accuracy : {acc:.4f}")
        print(classification_report(y_test, preds,
                                    target_names=class_names,
                                    zero_division=0))

        results[name]         = acc
        classical_preds[name] = preds
        classical_probs[name] = probs
        joblib.dump(model, f"models/{name.replace(' ', '_')}.pkl")

    # =================================================
    # QUANTUM DEVICE
    # =================================================

    dev = qml.device("lightning.qubit", wires=N_QUBITS)

    # =================================================
    # VQC
    #
    # ROOT CAUSE of the previous crash:
    #   PennyLane's autograd tracer wraps the weight array
    #   in a box object. When the weights are 3-D, multi-index
    #   access like weights[layer, i, 0] triggers __getitem__
    #   on the box with a tuple index, which the tracer cannot
    #   handle and raises "too many indices for array".
    #
    # FIX: store weights as a FLAT 1-D array and compute
    #   a single integer index inside the circuit.
    #   flat_index = layer * N_QUBITS * 3 + qubit * 3 + rot
    # =================================================

    print("\n" + "=" * 60)
    print("Training VQC")
    print("=" * 60)

    @qml.qnode(dev, interface="autograd")
    def vqc_circuit(x, weights):
        """
        weights : flat 1-D array, length = N_LAYERS * N_QUBITS * 3
        index   : weights[layer * N_QUBITS * 3 + qubit * 3 + rot_id]
        """
        for layer in range(N_LAYERS):
            base = layer * N_QUBITS * 3
            # Data re-uploading every layer
            for i in range(N_QUBITS):
                qml.RY(x[i] * np.pi, wires=i)
            # Trainable Rot gates – ONE flat index per parameter
            for i in range(N_QUBITS):
                idx = base + i * 3
                qml.Rot(weights[idx],
                        weights[idx + 1],
                        weights[idx + 2],
                        wires=i)
            # Ring CNOT entanglement
            for i in range(N_QUBITS):
                qml.CNOT(wires=[i, (i + 1) % N_QUBITS])

        return [qml.expval(qml.PauliZ(i)) for i in range(n_classes)]

    def vqc_cost(weights, X_batch, y_batch):
        logits = qnp.array([vqc_circuit(x, weights) for x in X_batch])
        return cross_entropy_loss(logits, y_batch)

    # Flat 1-D initialisation
    vqc_weights = qnp.array(
        np.random.uniform(0, 2 * np.pi, VQC_N_WEIGHTS),
        requires_grad=True,
    )

    vqc_opt = qml.AdamOptimizer(LEARNING_RATE)
    t0 = time.time()

    for epoch in range(EPOCHS):
        idx = np.random.permutation(len(X_train))
        for start in range(0, len(X_train), BATCH_SIZE):
            batch_idx = idx[start: start + BATCH_SIZE]
            X_batch   = X_train[batch_idx]
            y_batch   = y_train[batch_idx].tolist()   # plain list → no grad

            # Lambda ensures only vqc_weights is differentiated
            vqc_weights = vqc_opt.step(
                lambda w: vqc_cost(w, X_batch, y_batch),
                vqc_weights,
            )
            # Re-wrap to preserve requires_grad after optimizer step
            vqc_weights = qnp.array(vqc_weights, requires_grad=True)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  VQC epoch {epoch + 1}/{EPOCHS}")

    training_times["VQC"] = time.time() - t0

    vqc_preds = []
    vqc_probs = []
    for x in X_test:
        logits = np.array(vqc_circuit(x, vqc_weights))
        prob   = softmax(logits)
        vqc_probs.append(prob)
        vqc_preds.append(int(np.argmax(prob)))

    vqc_acc = accuracy_score(y_test, vqc_preds)
    print(f"VQC Accuracy: {vqc_acc:.4f}")
    print(classification_report(y_test, vqc_preds,
                                 target_names=class_names,
                                 zero_division=0))
    results["VQC"] = vqc_acc

    # =================================================
    # QCNN – same flat-weight pattern for consistency
    # =================================================

    print("\n" + "=" * 60)
    print("Training QCNN")
    print("=" * 60)

    @qml.qnode(dev, interface="autograd")
    def qcnn_circuit(x, weights):
        """
        weights : flat 1-D array, length = N_QUBITS
        Conv layer: stride-2 CNOT pairs, one RY per qubit.
        """
        for i in range(N_QUBITS):
            qml.RY(x[i] * np.pi, wires=i)

        for i in range(0, N_QUBITS - 1, 2):
            qml.CNOT(wires=[i, i + 1])
            qml.RY(weights[i],     wires=i)
            qml.RY(weights[i + 1], wires=i + 1)

        return [qml.expval(qml.PauliZ(i)) for i in range(n_classes)]

    def qcnn_cost(weights, X_batch, y_batch):
        logits = qnp.array([qcnn_circuit(x, weights) for x in X_batch])
        return cross_entropy_loss(logits, y_batch)

    qcnn_weights = qnp.array(
        np.random.uniform(0, 2 * np.pi, QCNN_N_WEIGHTS),
        requires_grad=True,
    )

    qcnn_opt = qml.AdamOptimizer(LEARNING_RATE)
    t0 = time.time()

    for epoch in range(EPOCHS):
        idx = np.random.permutation(len(X_train))
        for start in range(0, len(X_train), BATCH_SIZE):
            batch_idx = idx[start: start + BATCH_SIZE]
            X_batch   = X_train[batch_idx]
            y_batch   = y_train[batch_idx].tolist()

            qcnn_weights = qcnn_opt.step(
                lambda w: qcnn_cost(w, X_batch, y_batch),
                qcnn_weights,
            )
            qcnn_weights = qnp.array(qcnn_weights, requires_grad=True)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  QCNN epoch {epoch + 1}/{EPOCHS}")

    training_times["QCNN"] = time.time() - t0

    qcnn_preds = []
    qcnn_probs = []
    for x in X_test:
        logits = np.array(qcnn_circuit(x, qcnn_weights))
        prob   = softmax(logits)
        qcnn_probs.append(prob)
        qcnn_preds.append(int(np.argmax(prob)))

    qcnn_acc = accuracy_score(y_test, qcnn_preds)
    print(f"QCNN Accuracy: {qcnn_acc:.4f}")
    print(classification_report(y_test, qcnn_preds,
                                  target_names=class_names,
                                  zero_division=0))
    results["QCNN"] = qcnn_acc

    # =================================================
    # SAVE
    # =================================================

    joblib.dump(results,         "results/final_results.pkl")
    joblib.dump(classical_preds, "results/classical_preds.pkl")
    joblib.dump(classical_probs, "results/classical_probs.pkl")
    joblib.dump(vqc_preds,       "results/vqc_preds.pkl")
    joblib.dump(vqc_probs,       "results/vqc_probs.pkl")
    joblib.dump(qcnn_preds,      "results/qcnn_preds.pkl")
    joblib.dump(qcnn_probs,      "results/qcnn_probs.pkl")
    joblib.dump(training_times,  "results/training_times.pkl")
    print("\nAll results saved to results/")


# =====================================================
# HELPER ACCESSORS
# =====================================================

def get_preds(name):
    if name in classical_preds:
        return classical_preds[name]
    return vqc_preds if name == "VQC" else qcnn_preds


def get_probs(name):
    if name in classical_probs:
        return classical_probs[name]
    return vqc_probs if name == "VQC" else qcnn_probs


# =====================================================
# PLOTS
# =====================================================

print("\n" + "=" * 60)
print("Generating plots...")
print("=" * 60)

COLORS = plt.cm.tab10.colors

# 1. Accuracy bar chart
fig, ax = plt.subplots(figsize=(10, 5))
names = list(results.keys())
accs  = [results[n] for n in names]
bars  = ax.bar(names, accs, color=COLORS[:len(names)], edgecolor="black")
for bar, acc in zip(bars, accs):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            f"{acc:.3f}",
            ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.set_ylim(0, 1.05)
ax.set_ylabel("Accuracy")
ax.set_title("Model Accuracy Comparison", fontsize=13, fontweight="bold")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig("results/accuracy.png", dpi=150)
plt.close()
print("  Saved: results/accuracy.png")

# 2. Confusion matrices
for name in results:
    preds = get_preds(name)
    cm    = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    plt.colorbar(im, ax=ax)
    tick_marks = np.arange(n_classes)
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.set_xticklabels(class_names, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(class_names, fontsize=8)
    thresh = cm.max() / 2.0
    for i in range(n_classes):
        for j in range(n_classes):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center", fontsize=7,
                    color="white" if cm[i, j] > thresh else "black")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title(f"Confusion Matrix — {name}", fontsize=12, fontweight="bold")
    plt.tight_layout()
    fname = f"results/confusion_{name.replace(' ', '_')}.png"
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"  Saved: {fname}")

# 3. ROC curves
for name in results:
    probs = np.array(get_probs(name))
    fig, ax = plt.subplots(figsize=(8, 6))
    for i, cls in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], probs[:, i])
        ax.plot(fpr, tpr, label=cls, linewidth=1.5)
    ax.plot([0, 1], [0, 1], "k--", linewidth=0.8)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curves — {name}", fontsize=12, fontweight="bold")
    ax.legend(fontsize=7, loc="lower right")
    plt.tight_layout()
    fname = f"results/roc_{name.replace(' ', '_')}.png"
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"  Saved: {fname}")

# 4. Training time bar chart
fig, ax = plt.subplots(figsize=(10, 5))
t_names = list(training_times.keys())
t_vals  = [training_times[n] for n in t_names]
bars    = ax.bar(t_names, t_vals, color=COLORS[:len(t_names)], edgecolor="black")
for bar, t in zip(bars, t_vals):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{t:.1f}s",
            ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.set_ylabel("Time (seconds)")
ax.set_title("Training Time Comparison", fontsize=13, fontweight="bold")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig("results/training_time.png", dpi=150)
plt.close()
print("  Saved: results/training_time.png")


# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n" + "=" * 60)
print("FINAL ACCURACY SUMMARY")
print("=" * 60)
for model_name, acc in sorted(results.items(), key=lambda x: -x[1]):
    bar   = "█" * int(acc * 40)
    ttime = training_times.get(model_name, 0)
    print(f"  {model_name:<22} {acc:.4f}  {bar}  ({ttime:.1f}s)")

print("\nAll outputs saved in the results/ folder.")