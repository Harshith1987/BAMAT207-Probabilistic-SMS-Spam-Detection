# BAMAT207: Applications of Probability and Statistics
## Beyond the Words: A Probabilistic and Bayesian Approach to SMS Spam Detection
### An Empirical Study of Random Variables, Bayes' Theorem, and Multinomial Naive Bayes

**Course Code:** BAMAT207  
**Topic:** Probability and Random Variables  
**Deadline Date for Submission:** 27.10.2026  
**Repository Name:** `BAMAT207-Probabilistic-SMS-Spam-Detection`  

---

## 1. Project Scenario & Overview
In mobile and digital communications, unsolicited bulk messaging (Spam) compromises user trust, consumes network bandwidth, and frequently delivers malicious phishing attacks, lottery scams, and financial fraud. 

This project develops a complete, mathematically grounded Python system that classifies an incoming SMS message as either:
- **Spam ($Y = 1$)**
- **Genuine Message / Ham ($Y = 0$)**

The system models the underlying uncertainty using foundational principles of **probability theory**, **Bayes' theorem**, and **discrete random variables**, and combines them with a **Multinomial Naive Bayes** classifier to compute posterior prediction probabilities for real-time messages.

---

## 2. Theoretical Mathematical Foundations

### 2.1 Prior Probabilities
Let the universe of SMS messages be sample space $\Omega$, partitioned into two mutually exclusive and collectively exhaustive events:
- $S$: Message is Spam
- $H$: Message is Genuine (Ham)

$$\Omega = S \cup H \quad \text{and} \quad S \cap H = \emptyset$$

The prior probabilities are:
$$P(S) = \frac{N_{\text{spam}}}{N}, \quad P(H) = \frac{N_{\text{ham}}}{N}$$
$$P(S) + P(H) = 1.0$$

### 2.2 Conditional Probability & Bayes' Theorem
For any word feature $W$ occurring in an SMS message:

1. **Direct Empirical Conditional Probability**:
   $$P(S \mid W) = \frac{N_{S \cap W}}{N_W}$$
   *(The proportion of messages containing $W$ that are spam)*

2. **Bayes' Theorem Formulation**:
   $$P(S \mid W) = \frac{P(W \mid S) \cdot P(S)}{P(W)}$$
   where:
   - $P(W \mid S) = \frac{N_{S \cap W}}{N_S}$ is the **Likelihood** of the word appearing in spam.
   - $P(S)$ is the **Prior Probability** of spam.
   - $P(W) = \frac{N_W}{N}$ is the **Marginal Probability (Evidence)** of the word.

**Analytical Verification**:
$$\frac{P(W \mid S) \cdot P(S)}{P(W)} = \frac{\left(\frac{N_{S \cap W}}{N_S}\right) \cdot \left(\frac{N_S}{N}\right)}{\frac{N_W}{N}} = \frac{N_{S \cap W}}{N_W} = P(S \mid W)$$

### 2.3 Discrete Random Variable Analysis (Bernoulli Process)
Define the random variable $Y$:
$$Y = \begin{cases} 1, & \text{if message is Spam} \\ 0, & \text{if message is Ham} \end{cases}$$

Since $Y \in \{0, 1\}$, $Y \sim \text{Bernoulli}(p)$ with parameter $p = P(S)$ and $q = 1 - p = P(H)$.

- **Expectation (Expected Value) $\mathbb{E}[Y]$**:
  $$\mathbb{E}[Y] = \sum_{y \in \{0, 1\}} y \cdot P(Y = y) = (1 \cdot p) + (0 \cdot q) = p = P(\text{Spam})$$
- **Variance $\text{Var}(Y)$**:
  $$\text{Var}(Y) = \mathbb{E}[Y^2] - (\mathbb{E}[Y])^2 = (1^2 \cdot p + 0^2 \cdot q) - p^2 = p - p^2 = p(1 - p)$$
- **Standard Deviation $\sigma_Y$**:
  $$\sigma_Y = \sqrt{\text{Var}(Y)} = \sqrt{p(1 - p)}$$

### 2.4 Multinomial Naive Bayes Model
Given a feature vector $\mathbf{x} = (x_1, x_2, \dots, x_V)$ of word counts, Naive Bayes assumes conditional independence among words given the class $c \in \{0, 1\}$:
$$P(Y = c \mid \mathbf{x}) \propto P(Y = c) \prod_{i=1}^{V} P(w_i \mid Y = c)^{x_i}$$

Using **Laplace smoothing** ($\alpha = 1$) to prevent zero-frequency probabilities for unseen words:
$$\hat{P}(w_i \mid Y = c) = \frac{N_{c, i} + 1}{N_c + |V|}$$

---

## 3. Dataset Summary & Preprocessing

- **Dataset Name:** SMS Spam Collection
- **Source:** UCI Machine Learning Repository (ID: 228)
- **Raw Dimensions:** 5,572 messages
- **Missing Values:** 0
- **Duplicate Records Removed:** 403 duplicates
- **Clean Dimensions:** 5,169 unique messages

### Class Distribution:
| Class | Label | Numerical Code | Count | Percentage | Prior Probability |
|---|---|---|---|---|---|
| Genuine | Ham | 0 | 4,516 | 87.37% | $P(\text{Ham}) = 0.8737$ |
| Spam | Spam | 1 | 653 | 12.63% | $P(\text{Spam}) = 0.1263$ |
| **Total** | | | **5,169** | **100.0%** | **1.0000** |

---

## 4. Experimental Results

### 4.1 Suspicious Words Probability & Bayes' Theorem Verification
Probability calculations for the five required suspicious words:

| Word ($W$) | Total ($N_W$) | Spam ($N_{S \cap W}$) | Ham ($N_{H \cap W}$) | $P(W)$ | $P(W \mid S)$ | Empirical $P(S \mid W)$ | Bayes $P(S \mid W)$ | Verified? |
|---|---|---|---|---|---|---|---|---|
| **`free`** | 203 | 148 | 55 | 0.0393 | 0.2266 | **0.7291 (72.91%)** | **0.7291 (72.91%)** | **Yes** |
| **`prize`** | 73 | 73 | 0 | 0.0141 | 0.1118 | **1.0000 (100.0%)** | **1.0000 (100.0%)** | **Yes** |
| **`win`** | 55 | 49 | 6 | 0.0106 | 0.0750 | **0.8909 (89.09%)** | **0.8909 (89.09%)** | **Yes** |
| **`urgent`** | 62 | 57 | 5 | 0.0120 | 0.0873 | **0.9194 (91.94%)** | **0.9194 (91.94%)** | **Yes** |
| **`offer`** | 30 | 24 | 6 | 0.0058 | 0.0368 | **0.8000 (80.00%)** | **0.8000 (80.00%)** | **Yes** |

> **Key Insight:** In this dataset, the presence of the word `"prize"` yielded a **100.0%** posterior probability of being spam. Similarly, `"free"` increases the probability of an SMS being spam from the prior base rate of $12.63\%$ to $72.91\%$.

### 4.2 Random Variable Parameters
- **$\mathbb{E}[Y] = p = 0.1263$**
- **$\text{Var}(Y) = p(1 - p) = 0.1263 \times 0.8737 = 0.1104$**
- **$\text{SD}(Y) = \sqrt{0.1104} = 0.3322$**

### 4.3 Model Performance Evaluation (Test Set: $n = 1,034$)
- **Train/Test Split:** 80% Train ($n = 4,135$), 20% Test ($n = 1,034$) with **Stratified Sampling**
- **CountVectorizer Feature Vocabulary:** 7,414 unique tokens

| Metric | Score (Decimal) | Score (%) |
|---|---|---|
| **Overall Accuracy** | **0.9836** | **98.36%** |
| **Spam Precision** | **0.9597** | **95.97%** |
| **Spam Recall** | **0.9084** | **90.84%** |
| **Spam F1-Score** | **0.9333** | **93.33%** |

#### Confusion Matrix:
$$\begin{pmatrix} \text{True Ham (TN): } 898 & \text{False Spam (FP): } 5 \\ \text{False Ham (FN): } 12 & \text{True Spam (TP): } 119 \end{pmatrix}$$

#### Critical Error Analysis:
1. **False Positives ($FP = 5$):** Genuine messages incorrectly flagged as Spam.
   - *Example:* `"Are you free now?can i call now?"` (Triggered due to word `"free"`).
   - *Impact:* High risk because legitimate urgent communications can be lost to spam folders.
2. **False Negatives ($FN = 12$):** Spam messages incorrectly permitted as Ham.
   - *Example:* Spam with obfuscated telephone codes and non-standard alphanumeric phrasing.
   - *Impact:* Minor inconvenience to the user compared to lost genuine messages.

---

## 5. Real-Time Testing Demonstrations

| Input SMS Message | Predicted Class | $P(\text{Spam} \mid \text{Msg})$ | $P(\text{Ham} \mid \text{Msg})$ |
|---|---|---|---|
| `"Congratulations! You have won a free prize. Claim now."` | **Spam** | **1.0000 (100.00%)** | **0.0000 (0.00%)** |
| `"Hey, are you free this afternoon to study for the BAMAT207 exam?"` | **Genuine (Ham)** | **0.0006 (0.06%)** | **0.9994 (99.94%)** |
| `"URGENT! Your mobile account has won an exclusive $1,000 cash offer. Call now to claim."` | **Spam** | **1.0000 (100.00%)** | **0.0000 (0.00%)** |
| `"Can you send me the lecture notes when you get home?"` | **Genuine (Ham)** | **0.0028 (0.28%)** | **0.9972 (99.72%)** |
| `"Win a brand new car today! Free entry, text WIN to 80085 immediately."` | **Spam** | **0.9999 (99.99%)** | **0.0001 (0.01%)** |

---

## 6. Project Structure

```
sms_spam_detection/
│
├── Probabilistic_SMS_Spam_Detection.ipynb   # Complete Google Colab / Jupyter Notebook
├── sms_spam_detector.py                     # Standalone production Python script
├── requirements.txt                         # Dependency requirements
├── README.md                                # Academic project report & documentation
├── .gitignore                               # Git ignored files
│
├── data/
│   ├── SMSSpamCollection                    # Cleaned official UCI dataset
│   └── readme                               # Original dataset notes
│
└── plots/
    ├── class_distribution.png               # Prior probability bar chart
    ├── word_probabilities.png               # P(Spam | Word) comparison chart
    └── confusion_matrix.png                 # Test evaluation confusion matrix
```

---

## 7. How to Run

### Option A: Running the Standalone Python Script
1. Clone or open the project folder:
   ```bash
   cd sms_spam_detection
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python sms_spam_detector.py
   ```

### Option B: Running via Google Colab / Jupyter Notebook
1. Open [Google Colab](https://colab.research.google.com/).
2. Click **Upload** and select `Probabilistic_SMS_Spam_Detection.ipynb`.
3. Run all cells (`Runtime -> Run all`). All downloads, statistics, and charts will execute and display automatically.

---

## 8. GitHub Submission Guide

To submit this project via GitHub as required:
1. Open your terminal or Command Prompt in this folder:
   ```bash
   git init
   git add .
   git commit -m "Complete BAMAT207 Probabilistic SMS Spam Detection Project"
   ```
2. Link and push your commits:
   ```bash
   git remote add origin https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection.git
   git branch -M main
   git push -u origin main
   ```
3. Your submission link:
   `https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection`

---

## 9. Final Learning Outcomes Achieved
1. **Mathematical Rigor**: Demonstrated how empirical observation, conditional probabilities, and Bayes' Theorem directly govern AI inference.
2. **Random Variables**: Explored the Bernoulli formulation of binary classification and calculated analytical expectation and variance.
3. **Machine Learning Pipeline**: Implemented an end-to-end NLP workflow (text cleaning, CountVectorizer feature matrix generation, Multinomial Naive Bayes model training, and probability thresholding).
4. **Error Analysis**: Diagnosed the critical operational difference between False Positives (user friction) and False Negatives (spam leakage).
5. **Open Repository & Digital Profile**: Structured professional code, documentation, and notebooks suitable for a student engineering portfolio.
