"""
BAMAT207: Applications of Probability and Statistics Project
Title: Beyond the Words: A Probabilistic and Bayesian Approach to SMS Spam Detection
Topic: Probability and Random Variables
Author: T. Harshith (25BCE2863)

Description:
This script performs end-to-end data processing, probabilistic calculations,
Bayes' Theorem verification, random variable expectation and variance analysis,
Multinomial Naive Bayes model training, rigorous evaluation, and interactive
real-time SMS spam prediction.
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. DATASET HANDLING
# ---------------------------------------------------------
def load_and_preprocess_data(data_path="data/SMSSpamCollection"):
    """
    Load the SMS Spam Collection dataset, check for nulls,
    remove duplicate rows, and encode labels (ham: 0, spam: 1).
    """
    print("=" * 70)
    print("STEP 1: DATASET HANDLING")
    print("=" * 70)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found at: {data_path}")

    # Read tab-separated file with no header
    df = pd.read_csv(data_path, sep="\t", names=["label", "message"], encoding="utf-8")
    
    print(f"[*] Initial Raw Dataset Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print("[*] Checking for missing values:")
    print(df.isnull().sum())
    
    # Check and remove duplicates
    duplicate_count = df.duplicated().sum()
    print(f"[*] Duplicate records found: {duplicate_count}")
    df_clean = df.drop_duplicates().reset_index(drop=True)
    print(f"[*] Dataset Dimensions after removing duplicates: {df_clean.shape[0]} rows")
    
    # Convert labels into numerical values: Spam = 1, Ham = 0
    df_clean["label_num"] = df_clean["label"].map({"ham": 0, "spam": 1})
    
    print("\n[*] Sample preprocessed rows:")
    print(df_clean[["label", "label_num", "message"]].head(5))
    
    return df_clean


# ---------------------------------------------------------
# 2. DATASET ANALYSIS & CLASS DISTRIBUTION
# ---------------------------------------------------------
def analyze_dataset_distribution(df, save_plot=True):
    """
    Compute prior probabilities P(Spam) and P(Ham) and visualize
    the class distribution using a bar chart.
    """
    print("\n" + "=" * 70)
    print("STEP 2: DATASET ANALYSIS & PRIOR PROBABILITIES")
    print("=" * 70)
    
    total_messages = len(df)
    spam_count = (df["label_num"] == 1).sum()
    ham_count = (df["label_num"] == 0).sum()
    
    p_spam = spam_count / total_messages
    p_ham = ham_count / total_messages
    
    print(f"Total Messages        : {total_messages}")
    print(f"Genuine Messages (Ham): {ham_count} ({p_ham * 100:.2f}%)")
    print(f"Spam Messages         : {spam_count} ({p_spam * 100:.2f}%)")
    print("-" * 50)
    print(f"Prior Probability P(Ham)  = {ham_count} / {total_messages} = {p_ham:.4f}")
    print(f"Prior Probability P(Spam) = {spam_count} / {total_messages} = {p_spam:.4f}")
    
    if save_plot:
        plt.figure(figsize=(7, 5))
        bars = plt.bar(["Genuine (Ham)", "Spam"], [ham_count, spam_count], color=["#2b5c8f", "#d9534f"], width=0.5)
        plt.title("SMS Dataset Class Distribution", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Message Category", fontsize=11)
        plt.ylabel("Number of Messages", fontsize=11)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Annotate counts and percentages on top of bars
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total_messages) * 100
            plt.annotate(
                f"{height}\n({percentage:.1f}%)",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )
        
        plt.ylim(0, max(ham_count, spam_count) * 1.15)
        plt.tight_layout()
        plot_path = os.path.join(PLOTS_DIR, "class_distribution.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f"[*] Class distribution bar chart saved to: {plot_path}")
        
    return p_spam, p_ham


# ---------------------------------------------------------
# 3. WORD-BASED CONDITIONAL PROBABILITY & BAYES' THEOREM
# ---------------------------------------------------------
def word_probability_analysis(df, p_spam, p_ham, words=None, save_plot=True):
    """
    Calculate conditional probabilities for suspicious words and verify
    via Bayes' Theorem:
      P(Spam | Word) = [P(Word | Spam) * P(Spam)] / P(Word)
    """
    print("\n" + "=" * 70)
    print("STEP 3: WORD-BASED PROBABILITY ANALYSIS & BAYES' THEOREM VERIFICATION")
    print("=" * 70)
    
    if words is None:
        words = ["free", "prize", "win", "urgent", "offer"]
        
    total_messages = len(df)
    total_spam = (df["label_num"] == 1).sum()
    total_ham = (df["label_num"] == 0).sum()
    
    results = []
    
    for word in words:
        # Match whole word case-insensitively
        pattern = rf"\b{re.escape(word)}\b"
        contains_word = df["message"].str.contains(pattern, case=False, regex=True)
        
        n_w = contains_word.sum()
        n_w_spam = (contains_word & (df["label_num"] == 1)).sum()
        n_w_ham = (contains_word & (df["label_num"] == 0)).sum()
        
        # Probabilities
        p_w = n_w / total_messages
        p_w_given_spam = n_w_spam / total_spam if total_spam > 0 else 0
        p_w_given_ham = n_w_ham / total_ham if total_ham > 0 else 0
        
        # Direct empirical calculation
        p_spam_given_w_empirical = n_w_spam / n_w if n_w > 0 else 0.0
        
        # Bayes' Theorem formulation:
        # P(Spam | W) = [P(W | Spam) * P(Spam)] / P(W)
        p_spam_given_w_bayes = (p_w_given_spam * p_spam) / p_w if p_w > 0 else 0.0
        
        diff = abs(p_spam_given_w_empirical - p_spam_given_w_bayes)
        verified = diff < 1e-9
        
        results.append({
            "Word": word,
            "Total_Occurrences": n_w,
            "Occurrences_in_Spam": n_w_spam,
            "Occurrences_in_Ham": n_w_ham,
            "P(Word)": p_w,
            "P(Word|Spam)": p_w_given_spam,
            "P(Spam|Word)_Empirical": p_spam_given_w_empirical,
            "P(Spam|Word)_Bayes": p_spam_given_w_bayes,
            "Verified": verified
        })
        
    results_df = pd.DataFrame(results)
    print(results_df[[
        "Word", "Total_Occurrences", "Occurrences_in_Spam",
        "P(Word|Spam)", "P(Spam|Word)_Empirical", "P(Spam|Word)_Bayes", "Verified"
    ]].to_string(index=False))
    
    print("\nDetailed Step-by-Step Bayes Verification:")
    for res in results:
        w = res["Word"]
        p_w = res["P(Word)"]
        p_w_s = res["P(Word|Spam)"]
        p_s_w = res["P(Spam|Word)_Bayes"]
        print(f" * Word '{w}':")
        print(f"   - P({w}) = {p_w:.4f}, P({w} | Spam) = {p_w_s:.4f}, P(Spam) = {p_spam:.4f}")
        print(f"   - Bayes: P(Spam | {w}) = [{p_w_s:.4f} * {p_spam:.4f}] / {p_w:.4f} = {p_s_w:.4f} ({p_s_w*100:.2f}%)")
        print(f"   - Empirical = {res['P(Spam|Word)_Empirical']:.4f} => Mathematical Equivalence Verified: {res['Verified']}")

    if save_plot:
        plt.figure(figsize=(8, 5))
        bars = plt.bar(
            results_df["Word"],
            results_df["P(Spam|Word)_Bayes"] * 100,
            color="#e67e22",
            edgecolor="#b95b12",
            width=0.55
        )
        plt.title("Probability of an SMS Being Spam Given Suspicious Words: P(Spam | Word)", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Suspicious Word Feature", fontsize=11)
        plt.ylabel("P(Spam | Word) (%)", fontsize=11)
        plt.ylim(0, 115)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        
        for bar in bars:
            height = bar.get_height()
            plt.annotate(
                f"{height:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )
            
        plt.tight_layout()
        plot_path = os.path.join(PLOTS_DIR, "word_probabilities.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f"\n[*] Word probability bar chart saved to: {plot_path}")
        
    return results_df


# ---------------------------------------------------------
# 4. RANDOM VARIABLE ANALYSIS (BERNOULLI DISTRIBUTION)
# ---------------------------------------------------------
def random_variable_analysis(p_spam):
    """
    Model the spam classification state as a Bernoulli random variable Y:
      Y = 1 if message is spam
      Y = 0 if message is ham
    Calculate Expectation E(Y), Variance Var(Y), and Standard Deviation SD(Y).
    """
    print("\n" + "=" * 70)
    print("STEP 4: RANDOM VARIABLE ANALYSIS (BERNOULLI PROCESS)")
    print("=" * 70)
    
    p = p_spam
    q = 1.0 - p
    
    # Expectation E(Y) = 1*p + 0*(1-p) = p
    e_y = p
    # Variance Var(Y) = E(Y^2) - [E(Y)]^2 = p - p^2 = p(1 - p)
    var_y = p * (1.0 - p)
    sd_y = np.sqrt(var_y)
    
    print("Random Variable Definition:")
    print("  Y ~ Bernoulli(p)")
    print("  where Y = 1 if message is Spam, and Y = 0 if message is Ham")
    print(f"  Parameter p = P(Y = 1) = P(Spam) = {p:.4f}")
    print(f"  Parameter q = P(Y = 0) = P(Ham)  = 1 - p = {q:.4f}")
    print("-" * 50)
    print(f"Expectation E(Y):")
    print(f"  E(Y) = sum(y * P(Y = y)) = (1 * p) + (0 * q) = p = {e_y:.4f}")
    print(f"Variance Var(Y):")
    print(f"  Var(Y) = E[(Y - E(Y))^2] = p * (1 - p) = {p:.4f} * {q:.4f} = {var_y:.4f}")
    print(f"Standard Deviation SD(Y):")
    print(f"  SD(Y) = sqrt(Var(Y)) = {sd_y:.4f}")
    
    return {"p": p, "q": q, "E(Y)": e_y, "Var(Y)": var_y, "SD(Y)": sd_y}


# ---------------------------------------------------------
# 5. DATA PREPARATION: TRAIN-TEST SPLIT & VECTORIZATION
# ---------------------------------------------------------
def prepare_data(df, test_size=0.20, random_state=42):
    """
    Split the dataset into 80% training and 20% testing sets using
    stratified sampling, then vectorize the SMS texts with CountVectorizer.
    """
    print("\n" + "=" * 70)
    print("STEP 5: DATA PREPARATION & STRATIFIED SPLIT")
    print("=" * 70)
    
    X = df["message"]
    y = df["label_num"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"Training set size: {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
    print(f"Testing set size : {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")
    print(f"Training Spam proportion: {(y_train == 1).mean() * 100:.2f}%")
    print(f"Testing Spam proportion : {(y_test == 1).mean() * 100:.2f}%")
    
    vectorizer = CountVectorizer(lowercase=True, stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"[*] CountVectorizer vocabulary size: {len(vectorizer.get_feature_names_out())} unique tokens")
    print(f"[*] X_train shape: {X_train_vec.shape}")
    print(f"[*] X_test shape : {X_test_vec.shape}")
    
    return vectorizer, X_train_vec, X_test_vec, X_train, X_test, y_train, y_test


# ---------------------------------------------------------
# 6. MODEL BUILDING: MULTINOMIAL NAIVE BAYES
# ---------------------------------------------------------
def train_naive_bayes_model(X_train_vec, y_train):
    """
    Instantiate and train the Multinomial Naive Bayes classifier.
    """
    print("\n" + "=" * 70)
    print("STEP 6: MODEL BUILDING (MULTINOMIAL NAIVE BAYES)")
    print("=" * 70)
    
    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_vec, y_train)
    print("[*] MultinomialNB model successfully trained!")
    print(f"[*] Learned class log-priors: {model.class_log_prior_}")
    print(f"[*] Prior probabilities: P(Ham)={np.exp(model.class_log_prior_[0]):.4f}, P(Spam)={np.exp(model.class_log_prior_[1]):.4f}")
    
    return model


# ---------------------------------------------------------
# 7. MODEL EVALUATION & ERROR ANALYSIS
# ---------------------------------------------------------
def evaluate_model(model, vectorizer, X_test, X_test_vec, y_test, save_plot=True):
    """
    Evaluate accuracy, precision, recall, F1-score, confusion matrix,
    and explicitly identify False Positives and False Negatives.
    """
    print("\n" + "=" * 70)
    print("STEP 7: MODEL EVALUATION & MISCLASSIFICATION ANALYSIS")
    print("=" * 70)
    
    y_pred = model.predict(X_test_vec)
    y_proba = model.predict_proba(X_test_vec)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Model Performance Metrics:")
    print(f"  - Accuracy : {acc:.4f} ({acc * 100:.2f}%)")
    print(f"  - Precision: {prec:.4f} ({prec * 100:.2f}%)")
    print(f"  - Recall   : {rec:.4f} ({rec * 100:.2f}%)")
    print(f"  - F1-Score : {f1:.4f}")
    print("\nConfusion Matrix:")
    print(f"                  Predicted Ham    Predicted Spam")
    print(f"  Actual Ham      {cm[0, 0]:<16} {cm[0, 1]}")
    print(f"  Actual Spam     {cm[1, 0]:<16} {cm[1, 1]}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Genuine (Ham)", "Spam"]))
    
    # Detailed Error Analysis
    results_df = pd.DataFrame({
        "message": X_test.values,
        "actual": y_test.values,
        "predicted": y_pred,
        "p_ham": y_proba[:, 0],
        "p_spam": y_proba[:, 1]
    })
    
    # False Positives: Actual Ham (0) but Predicted as Spam (1)
    false_positives = results_df[(results_df["actual"] == 0) & (results_df["predicted"] == 1)]
    # False Negatives: Actual Spam (1) but Predicted as Ham (0)
    false_negatives = results_df[(results_df["actual"] == 1) & (results_df["predicted"] == 0)]
    
    print("-" * 50)
    print(f"CRITICAL ERROR ANALYSIS:")
    print(f"1. False Positives (Genuine messages incorrectly classified as Spam): {len(false_positives)}")
    if len(false_positives) > 0:
        for idx, row in false_positives.head(3).iterrows():
            print(f"   [FP] P(Spam)={row['p_spam']:.4f} | Msg: \"{row['message']}\"")
    else:
        print("   None! The model did not falsely flag any genuine message.")
        
    print(f"\n2. False Negatives (Spam messages incorrectly classified as Genuine): {len(false_negatives)}")
    if len(false_negatives) > 0:
        for idx, row in false_negatives.head(3).iterrows():
            print(f"   [FN] P(Spam)={row['p_spam']:.4f} | Msg: \"{row['message']}\"")
            
    if save_plot:
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        plt.title("Confusion Matrix: Multinomial Naive Bayes", fontsize=13, fontweight="bold", pad=12)
        plt.colorbar()
        tick_marks = np.arange(2)
        plt.xticks(tick_marks, ["Genuine (Ham)", "Spam"], fontsize=10)
        plt.yticks(tick_marks, ["Genuine (Ham)", "Spam"], fontsize=10)
        
        # Annotate cells
        thresh = cm.max() / 2.0
        labels = [["TN", "FP"], ["FN", "TP"]]
        for i in range(2):
            for j in range(2):
                cell_text = f"{labels[i][j]}\n{cm[i, j]}"
                plt.text(
                    j, i, cell_text,
                    horizontalalignment="center",
                    verticalalignment="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontweight="bold",
                    fontsize=11
                )
                
        plt.ylabel("True Class", fontsize=11)
        plt.xlabel("Predicted Class", fontsize=11)
        plt.tight_layout()
        plot_path = os.path.join(PLOTS_DIR, "confusion_matrix.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f"\n[*] Confusion matrix plot saved to: {plot_path}")
        
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "cm": cm,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }


# ---------------------------------------------------------
# 8. REAL-TIME TESTING PREDICTION FUNCTION
# ---------------------------------------------------------
def predict_sms(message, model, vectorizer):
    """
    Predict whether an incoming message is Spam or Ham along with
    the posterior probabilities P(Spam | Message) and P(Ham | Message).
    """
    msg_vec = vectorizer.transform([message])
    prediction = model.predict(msg_vec)[0]
    probabilities = model.predict_proba(msg_vec)[0]
    
    p_ham = probabilities[0]
    p_spam = probabilities[1]
    label = "Spam" if prediction == 1 else "Genuine message (Ham)"
    
    print("-" * 65)
    print(f"SMS Input : \"{message}\"")
    print(f"Prediction: {label}")
    print(f"Probability Distribution:")
    print(f"  - P(Spam | Message) = {p_spam:.4f} ({p_spam * 100:.2f}%)")
    print(f"  - P(Ham | Message)  = {p_ham:.4f} ({p_ham * 100:.2f}%)")
    print("-" * 65)
    
    return {
        "message": message,
        "prediction": label,
        "p_spam": p_spam,
        "p_ham": p_ham
    }


# ---------------------------------------------------------
# MAIN EXECUTION ROUTINE
# ---------------------------------------------------------
def main():
    print("=" * 70)
    print("BAMAT207: APPLICATIONS OF PROBABILITY AND STATISTICS")
    print("PROJECT: BEYOND THE WORDS - A PROBABILISTIC & BAYESIAN APPROACH")
    print("AUTHOR: T. HARSHITH | REG NO: 25BCE2863")
    print("=" * 70)
    
    # 1. Dataset Handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "data", "SMSSpamCollection")
    df = load_and_preprocess_data(data_file)
    
    # 2. Dataset Analysis
    p_spam, p_ham = analyze_dataset_distribution(df, save_plot=True)
    
    # 3. Word-based Probability Analysis & Bayes' Theorem Verification
    suspicious_words = ["free", "prize", "win", "urgent", "offer"]
    word_probability_analysis(df, p_spam, p_ham, words=suspicious_words, save_plot=True)
    
    # 4. Random Variable Analysis
    random_variable_analysis(p_spam)
    
    # 5. Data Preparation
    vectorizer, X_train_vec, X_test_vec, X_train, X_test, y_train, y_test = prepare_data(df)
    
    # 6. Model Building
    model = train_naive_bayes_model(X_train_vec, y_train)
    
    # 7. Model Evaluation & Error Analysis
    eval_metrics = evaluate_model(model, vectorizer, X_test, X_test_vec, y_test, save_plot=True)
    
    # 8. Real-Time Testing Demo
    print("\n" + "=" * 70)
    print("STEP 8: REAL-TIME TESTING DEMONSTRATION")
    print("=" * 70)
    
    test_cases = [
        "Congratulations! You have won a free prize. Claim now.",
        "Hey, are you free this afternoon to study for the BAMAT207 exam?",
        "URGENT! Your mobile account has won an exclusive $1,000 cash offer. Call now to claim.",
        "Can you send me the lecture notes when you get home?",
        "Win a brand new car today! Free entry, text WIN to 80085 immediately."
    ]
    
    for test_msg in test_cases:
        predict_sms(test_msg, model, vectorizer)
        
    print("\n[*] All steps completed successfully!")

if __name__ == "__main__":
    main()
