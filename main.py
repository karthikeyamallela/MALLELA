import argparse
import copy
import json
import os
import sys
import time

if sys.version_info >= (3, 14):
    raise RuntimeError(
        "This project should be run with Python 3.10-3.13 because PyTorch is "
        "not installed for Python 3.14 here. Use `py -3.10 main.py`."
    )

import torch

from deployment.convert_int8 import convert_int8
from models.mpt_model import get_model
from models.qat_model import apply_qat
from utils.evaluate import evaluate_model
from utils.preprocess import (
    build_fold_loaders,
    build_stratified_folds,
    load_data,
    load_unseen_data,
)
from utils.train import train_model

OUTPUT_DIR = "outputs"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "summary.json")
TEXT_SUMMARY_PATH = os.path.join(OUTPUT_DIR, "summary.txt")
EVALUATION_PATH = os.path.join(OUTPUT_DIR, "evaluation_details.json")
KFOLD_PATH = os.path.join(OUTPUT_DIR, "kfold_summary.json")


def _print_summary(summary, cached=False):
    if cached:
        print("\nUsing cached results from previous run.")
    print("\n=== PERFORMANCE COMPARISON ===")
    print(f"FP32 Accuracy : {summary['fp32_acc']:.2f}%")
    print(f"MPT Accuracy  : {summary['mpt_acc']:.2f}%")
    print(f"QAT Accuracy  : {summary['qat_acc']:.2f}%")
    if summary.get("unseen_mpt_acc") is not None:
        print(f"Unseen MPT Accuracy : {summary['unseen_mpt_acc']:.2f}%")
    print(f"\nFP32 Size : {summary['fp32_size_mb']:.2f} MB")
    print(f"INT8 Size : {summary['int8_size_mb']:.2f} MB")
    print(f"\nFP32 Time : {summary['fp32_time_s']:.2f}s")
    print(f"MPT Time  : {summary['mpt_time_s']:.2f}s")
    if summary.get("kfold_mean_acc") is not None:
        print(f"K-Fold Mean Accuracy : {summary['kfold_mean_acc']:.2f}%")


def _save_summary(summary):
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with open(TEXT_SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("Crop Disease MPT/QAT Summary\n")
        f.write(f"FP32 Accuracy: {summary['fp32_acc']:.2f}%\n")
        f.write(f"MPT Accuracy: {summary['mpt_acc']:.2f}%\n")
        f.write(f"QAT Accuracy: {summary['qat_acc']:.2f}%\n")
        if summary.get("unseen_mpt_acc") is not None:
            f.write(f"Unseen MPT Accuracy: {summary['unseen_mpt_acc']:.2f}%\n")
        f.write(f"FP32 Size: {summary['fp32_size_mb']:.2f} MB\n")
        f.write(f"INT8 Size: {summary['int8_size_mb']:.2f} MB\n")
        f.write(f"FP32 Time: {summary['fp32_time_s']:.2f}s\n")
        f.write(f"MPT Time: {summary['mpt_time_s']:.2f}s\n")
        if summary.get("kfold_mean_acc") is not None:
            f.write(f"K-Fold Mean Accuracy: {summary['kfold_mean_acc']:.2f}%\n")


def _save_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def run_kfold_validation(data_dir, k_folds=5):
    folds, samples, class_names = build_stratified_folds(data_dir, k_folds=k_folds)
    fold_results = []
    num_classes = len(class_names)

    for fold_idx, val_indices in enumerate(folds, start=1):
        print(f"\n=== K-FOLD {fold_idx}/{k_folds} ===")
        train_loader, val_loader = build_fold_loaders(samples, val_indices)
        fold_model = get_model(num_classes)
        fold_model = train_model(fold_model, train_loader, epochs=1)
        fold_metrics = evaluate_model(
            fold_model,
            val_loader,
            class_names=class_names,
            return_details=True,
            title=f"KFold-{fold_idx}",
        )
        fold_results.append(
            {
                "fold": fold_idx,
                "accuracy": fold_metrics["accuracy"],
                "macro_f1": fold_metrics["macro_f1"],
            }
        )

    mean_acc = sum(item["accuracy"] for item in fold_results) / len(fold_results)
    mean_f1 = sum(item["macro_f1"] for item in fold_results) / len(fold_results)
    kfold_summary = {
        "k_folds": k_folds,
        "mean_accuracy": mean_acc,
        "mean_macro_f1": mean_f1,
        "folds": fold_results,
    }
    _save_json(KFOLD_PATH, kfold_summary)
    return kfold_summary


def run_pipeline(force_run=False, unseen_dir="dataset_unseen", run_kfold=False, k_folds=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(SUMMARY_PATH) and not force_run:
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            summary = json.load(f)
        _print_summary(summary, cached=True)
        print(f"\nSaved summary file: {TEXT_SUMMARY_PATH}")
        return

    print("\n=== STEP 1: DATA LOADING ===")
    train_loader, test_loader, num_classes, class_names, class_to_idx = load_data("dataset")
    print("Classes:", num_classes)

    print("\n=== STEP 2: BASELINE (FP32) ===")
    model = get_model(num_classes)
    start = time.time()
    model = train_model(model, train_loader)
    fp32_time = time.time() - start
    fp32_details = evaluate_model(
        model,
        test_loader,
        class_names=class_names,
        return_details=True,
        title="FP32",
    )
    fp32_acc = fp32_details["accuracy"]
    torch.save(model.state_dict(), os.path.join(OUTPUT_DIR, "model_fp32.pth"))

    print("\n=== STEP 3: MPT TRAINING ===")
    start = time.time()
    model = train_model(model, train_loader)
    mpt_time = time.time() - start
    mpt_details = evaluate_model(
        model,
        test_loader,
        class_names=class_names,
        return_details=True,
        title="MPT",
    )
    mpt_acc = mpt_details["accuracy"]
    torch.save(model.state_dict(), os.path.join(OUTPUT_DIR, "model_mpt.pth"))
    mpt_model_for_unseen = copy.deepcopy(model).to("cpu").eval()

    print("\n=== STEP 4: QAT ===")
    fp32_fallback_model = copy.deepcopy(model)
    model = apply_qat(model)
    model = train_model(model, train_loader)

    print("\n=== STEP 5: INT8 CONVERSION ===")
    model = convert_int8(model, fallback_model=fp32_fallback_model)
    qat_details = evaluate_model(
        model,
        test_loader,
        class_names=class_names,
        return_details=True,
        title="QAT/INT8",
    )
    qat_acc = qat_details["accuracy"]
    torch.save(model, os.path.join(OUTPUT_DIR, "model_int8.pth"))

    unseen_details = None
    unseen_loader = load_unseen_data(unseen_dir, class_to_idx=class_to_idx)
    if unseen_loader is not None:
        print(f"\n=== STEP 6: UNSEEN DATASET EVALUATION ({unseen_dir}) ===")
        unseen_details = evaluate_model(
            mpt_model_for_unseen,
            unseen_loader,
            class_names=class_names,
            return_details=True,
            title="Unseen(MPT)",
        )
    else:
        print(f"\nNo unseen dataset found at '{unseen_dir}'. Skipping domain-shift check.")

    kfold_summary = None
    if run_kfold:
        print(f"\n=== STEP 7: {k_folds}-FOLD VALIDATION ===")
        kfold_summary = run_kfold_validation("dataset", k_folds=k_folds)

    fp32_size = os.path.getsize(os.path.join(OUTPUT_DIR, "model_fp32.pth")) / (1024 * 1024)
    int8_size = os.path.getsize(os.path.join(OUTPUT_DIR, "model_int8.pth")) / (1024 * 1024)

    summary = {
        "fp32_acc": fp32_acc,
        "mpt_acc": mpt_acc,
        "qat_acc": qat_acc,
        "unseen_mpt_acc": unseen_details["accuracy"] if unseen_details else None,
        "fp32_size_mb": fp32_size,
        "int8_size_mb": int8_size,
        "fp32_time_s": fp32_time,
        "mpt_time_s": mpt_time,
        "kfold_mean_acc": kfold_summary["mean_accuracy"] if kfold_summary else None,
    }

    evaluation_bundle = {
        "class_names": class_names,
        "fp32": fp32_details,
        "mpt": mpt_details,
        "qat_int8": qat_details,
        "unseen_mpt": unseen_details,
    }

    _save_summary(summary)
    _save_json(EVALUATION_PATH, evaluation_bundle)
    _print_summary(summary, cached=False)
    print(f"\nSaved summary file: {TEXT_SUMMARY_PATH}")
    print(f"Saved evaluation details: {EVALUATION_PATH}")
    if kfold_summary:
        print(f"Saved K-Fold summary: {KFOLD_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force-run",
        action="store_true",
        help="Run full training again and overwrite cached summary.",
    )
    parser.add_argument(
        "--unseen-dir",
        default="dataset_unseen",
        help="Optional unseen dataset directory for domain-shift evaluation.",
    )
    parser.add_argument(
        "--run-kfold",
        action="store_true",
        help="Run stratified K-fold validation after main training.",
    )
    parser.add_argument(
        "--kfolds",
        type=int,
        default=5,
        help="Number of folds for K-fold validation.",
    )
    args = parser.parse_args()
    run_pipeline(
        force_run=args.force_run,
        unseen_dir=args.unseen_dir,
        run_kfold=args.run_kfold,
        k_folds=args.kfolds,
    )
