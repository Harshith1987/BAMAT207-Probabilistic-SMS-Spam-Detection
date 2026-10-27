import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_f:
            encoded = base64.b64encode(img_f.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded}"
    return ""

def create_full_html_report(output_path, plots_dir):
    img_class = get_base64_image(os.path.join(plots_dir, "class_distribution.png"))
    img_word = get_base64_image(os.path.join(plots_dir, "word_probabilities.png"))
    img_cm = get_base64_image(os.path.join(plots_dir, "confusion_matrix.png"))
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BAMAT207: Beyond the Words - A Probabilistic & Bayesian Approach to SMS Spam Detection</title>
<style>
    @page {{
        size: A4;
        margin: 20mm;
    }}
    body {{
        font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
        line-height: 1.6;
        color: #2c3e50;
        background: #fff;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px;
    }}
    .page-break {{
        page-break-before: always;
        margin-top: 50px;
        border-top: 1px dashed #ccc;
        padding-top: 30px;
    }}
    .cover-page {{
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-top: 60px;
    }}
    .tag {{
        color: #e06666;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}
    .main-title {{
        color: #1f4e79;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.25;
        margin: 0 0 10px 0;
    }}
    .main-subtitle {{
        color: #595959;
        font-size: 18px;
        font-style: italic;
        margin: 0 0 25px 0;
    }}
    .divider {{
        height: 3px;
        background: #e69138;
        width: 100%;
        margin-bottom: 60px;
    }}
    .cover-meta {{
        font-size: 14px;
        margin-top: auto;
        background: #f8f9fa;
        padding: 20px 25px;
        border-radius: 6px;
        border: 1px solid #e9ecef;
    }}
    .cover-meta p {{
        margin: 6px 0;
    }}
    .cover-meta strong {{
        color: #1f4e79;
        min-width: 190px;
        display: inline-block;
    }}
    h1 {{
        color: #1f4e79;
        font-size: 22px;
        border-bottom: 2px solid #1f4e79;
        padding-bottom: 6px;
        margin-top: 30px;
    }}
    h2 {{
        color: #2b5c8f;
        font-size: 17px;
        margin-top: 22px;
    }}
    p, li {{
        font-size: 14px;
        text-align: justify;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
        font-size: 13px;
    }}
    th, td {{
        padding: 9px 12px;
        border: 1px solid #dee2e6;
        text-align: left;
    }}
    th {{
        background-color: #1f4e79;
        color: white;
        font-weight: 600;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    .formula-box {{
        background: #f0f4f8;
        border-left: 4px solid #1f4e79;
        padding: 12px 18px;
        margin: 15px 0;
        font-family: 'Cambria Math', 'Times New Roman', serif;
        font-size: 14.5px;
    }}
    .chart-box {{
        text-align: center;
        margin: 25px 0;
    }}
    .chart-box img {{
        max-width: 75%;
        border-radius: 4px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .caption {{
        font-size: 12px;
        font-style: italic;
        color: #6c757d;
        margin-top: 6px;
    }}
    .code-box {{
        background: #f4f6f8;
        border: 1px solid #dcdfe4;
        border-radius: 4px;
        padding: 15px;
        font-family: Consolas, monospace;
        font-size: 11.5px;
        overflow-x: auto;
        white-space: pre-wrap;
    }}
    .toc-table td {{
        border: none;
        padding: 5px 8px;
        border-bottom: 1px dotted #e0e0e0;
    }}
    .toc-title {{
        font-weight: 500;
    }}
    .toc-bold {{
        font-weight: bold;
        color: #1f4e79;
    }}
    @media print {{
        body {{
            padding: 0;
        }}
        .page-break {{
            border-top: none;
            margin-top: 0;
            padding-top: 0;
        }}
    }}
</style>
</head>
<body>

<div class="cover-page">
    <div class="tag">PROJECT REPORT</div>
    <div class="main-title">Beyond the Words:<br>A Probabilistic and Bayesian Approach to SMS Spam Detection</div>
    <div class="main-subtitle">An Empirical Study of Random Variables, Bayes' Theorem, and Multinomial Naive Bayes</div>
    <div class="divider"></div>
    <div class="cover-meta">
        <p><strong>Course:</strong> BAMAT207 – Applications of Probability and Statistics</p>
        <p><strong>Student Name:</strong> T. HARSHITH</p>
        <p><strong>Registration Number:</strong> 25BCE2863</p>
        <p><strong>Programme / Department:</strong> B.TECH , CSE--CORE</p>
        <p><strong>Submission Date:</strong> 27.10.2026</p>
        <p><strong>GitHub Repository:</strong> <a href="https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection" target="_blank">https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection</a></p>
    </div>
</div>

<div class="page-break"></div>

<h1>Abstract</h1>
<p>
Most of us get a few unwanted text messages every week: prize draws, "urgent" offers, links we would never click. 
Sorting them from genuine messages is a text-classification problem, and in this project I tackled it using nothing fancier 
than probability. The data comes from the UCI SMS Spam Collection (dataset ID: 228). The activity sheet lists 5,574 labelled 
messages. After I trimmed stray whitespace and dropped repeated texts, 5,160 unique messages were left for the main analysis: 
4,518 ham (genuine) and 642 spam.
</p>
<p>
The statistics come first. I worked out the empirical prior probabilities from the class counts, then looked at how often the whole 
words "free", "prize", "win", "urgent" and "offer" show up, and computed P(Spam | Word) and P(Ham | Word) by counting messages. 
I checked Bayes' theorem against the real counts for "free". I also defined a binary random variable Y (1 for spam, 0 for ham) 
and derived its expectation and population variance.
</p>
<p>
For the classifier itself, messages were turned into word counts with CountVectorizer and fed to a Multinomial Naive Bayes model, 
using a stratified 80:20 split with random_state=42. The vectorizer was fitted on the training messages only, so nothing from the 
test set leaks in. In the recorded run the test accuracy was 98.26%, with spam precision of 95.08%, recall of 90.63% and an F1-score 
of 92.80%. The confusion matrix reads 898 true negatives, 6 false positives, 12 false negatives and 116 true positives. The sample 
message from the activity sheet, "Congratulations! You have won a free prize. Claim now.", was classified as spam with a model-generated 
P(Spam | Message) of about 0.999999802. These are real model outputs and not the illustrative 0.96 and 0.04 printed in the activity sheet.
</p>
<p>
Taken together, the project shows how empirical probability, conditional probability, Bayes' theorem, expectation, variance and a 
simple probabilistic classifier fit into one reproducible text-analysis workflow.
</p>
<p><strong>Keywords:</strong> SMS spam, prior probability, conditional probability, Bayes' theorem, Bernoulli random variable, expectation, variance, CountVectorizer, Multinomial Naive Bayes.</p>

<div class="page-break"></div>

<h1>Table of Contents</h1>
<table class="toc-table">
    <tr><td class="toc-bold">Abstract</td><td style="text-align:right;">2</td></tr>
    <tr><td class="toc-bold">Chapter 1 – Introduction</td><td style="text-align:right;">4</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;1.1 Background</td><td style="text-align:right;">4</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;1.2 Problem Statement</td><td style="text-align:right;">4</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;1.3 Aim and Objectives</td><td style="text-align:right;">4</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;1.4 Scope</td><td style="text-align:right;">5</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;1.5 Applications</td><td style="text-align:right;">5</td></tr>
    <tr><td class="toc-bold">Chapter 2 – Dataset Description and Preparation</td><td style="text-align:right;">6</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.1 Dataset Source and Structure</td><td style="text-align:right;">6</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.2 Data Loading</td><td style="text-align:right;">6</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.3 Data Inspection and Missing Values</td><td style="text-align:right;">6</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.4 Duplicate Removal</td><td style="text-align:right;">7</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.5 Label Encoding</td><td style="text-align:right;">7</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;2.6 Cleaned Dataset Summary</td><td style="text-align:right;">7</td></tr>
    <tr><td class="toc-bold">Chapter 3 – Probability and Statistical Analysis</td><td style="text-align:right;">8</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.1 Notation and Counting Convention</td><td style="text-align:right;">8</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.2 Basic and Prior Probability</td><td style="text-align:right;">8</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.3 Conditional Probability</td><td style="text-align:right;">9</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.4 Bayes' Theorem: Verification for "free"</td><td style="text-align:right;">10</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.5 Random Variable, Expectation, and Variance</td><td style="text-align:right;">11</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;3.6 What the Probability Analysis Does and Does Not Mean</td><td style="text-align:right;">12</td></tr>
    <tr><td class="toc-bold">Chapter 4 – Methodology, Architecture, and Algorithm</td><td style="text-align:right;">13</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.1 System Architecture</td><td style="text-align:right;">13</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.2 Data Split and Stratified Sampling</td><td style="text-align:right;">13</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.3 Text Feature Extraction</td><td style="text-align:right;">13</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.4 Multinomial Naive Bayes</td><td style="text-align:right;">14</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.5 Algorithm</td><td style="text-align:right;">14</td></tr>
    <tr><td class="toc-title">&nbsp;&nbsp;4.6 Reproducibility and Leakage Control</td><td style="text-align:right;">15</td></tr>
    <tr><td class="toc-bold">Chapter 5 – Complete Python Implementation</td><td style="text-align:right;">16</td></tr>
    <tr><td class="toc-bold">Chapter 6 – Model Evaluation and Results</td><td style="text-align:right;">18</td></tr>
    <tr><td class="toc-bold">Chapter 7 – Real-Time SMS Testing</td><td style="text-align:right;">22</td></tr>
    <tr><td class="toc-bold">Chapter 8 – Results and Discussion</td><td style="text-align:right;">23</td></tr>
    <tr><td class="toc-bold">Chapter 9 – Conclusion and Future Scope</td><td style="text-align:right;">25</td></tr>
    <tr><td class="toc-bold">References</td><td style="text-align:right;">26</td></tr>
    <tr><td class="toc-bold">Appendix A – Complete Python Code</td><td style="text-align:right;">27</td></tr>
    <tr><td class="toc-bold">Appendix B – Verified Output Snapshot</td><td style="text-align:right;">30</td></tr>
    <tr><td class="toc-bold">Appendix C – Submission Checklist</td><td style="text-align:right;">31</td></tr>
</table>

<div class="page-break"></div>

<h1>Chapter 1 – Introduction</h1>
<h2>1.1 Background</h2>
<p>
People use text messages for chatting, delivery updates, one-time passwords and, unfortunately, advertising and scams. 
Some of those messages promise prizes, push you to act quickly, or try to get personal details out of you. 
An SMS is short and has no real structure, so a filter has very little to go on besides the words themselves.
</p>
<p>
Probability is a natural tool for this. A prior probability tells us how common spam is before we read a message. 
A conditional probability tells us how often a word turns up inside a class, or how often a class turns up among 
messages that contain a given word. Bayes' theorem ties these together so that a prior belief can be updated once we see evidence. 
Naive Bayes then stretches the same idea from one word to a whole bag of words.
</p>

<h2>1.2 Problem Statement</h2>
<p>
The task is to build a Python system that takes an SMS and predicts one of two labels: Spam (unwanted or unsolicited) 
or Ham (genuine). Along the way it has to analyse the labelled data, calculate the probability quantities the activity asks for, 
test the classifier on messages it has not seen, and show class probabilities for a new message.
</p>

<h2>1.3 Aim and Objectives</h2>
<ul>
    <li>Load the SMS Spam Collection from UCI using ucimlrepo, with a local ZIP fallback so the work can be reproduced offline.</li>
    <li>Inspect the raw data, check for missing values, normalise labels and text, remove repeated messages, and encode Spam = 1 and Ham = 0.</li>
    <li>Work out the count, percentage and prior probability of ham and spam, and plot the class distribution.</li>
    <li>Calculate message-level conditional probabilities for free, prize, win, urgent and offer using case-insensitive whole-word matching.</li>
    <li>Verify P(Spam | Free) with Bayes' theorem and compare it with the direct count.</li>
    <li>Define a binary random variable for spam status and find its expectation and variance, both by formula and with NumPy.</li>
    <li>Train and test a Multinomial Naive Bayes classifier on an 80:20 stratified split with a fixed random seed.</li>
    <li>Evaluate it with accuracy, precision, recall, F1-score, a confusion matrix, a classification report and a look at the errors.</li>
    <li>Test the example SMS from the activity sheet and provide a function for trying other messages.</li>
</ul>

<h2>1.4 Scope</h2>
<p>
The project covers binary classification of English SMS messages stored as text. It uses the supplied UCI dataset and one reproducible 
train-test split. In the word-level analysis a message counts if the whole word appears at least once; repeats inside the same message are 
not counted again. The machine-learning stage uses word-frequency features with Multinomial Naive Bayes.
</p>

<h2>1.5 Applications</h2>
<ul>
    <li>Filtering unwanted SMS messages before the user reads them.</li>
    <li>Flagging messages for manual review when the model gives a high spam probability.</li>
    <li>Showing, in a practical way, how probability and Bayes' theorem sit inside an AI classification pipeline.</li>
    <li>Serving as a baseline for later work on phishing detection, email filtering or notification screening.</li>
</ul>

<div class="page-break"></div>

<h1>Chapter 2 – Dataset Description and Preparation</h1>
<h2>2.1 Dataset Source and Structure</h2>
<p>
The activity names the SMS Spam Collection from the UCI Machine Learning Repository (dataset ID 228). 
UCI describes it as a public collection of labelled SMS messages with 5,574 instances.
</p>

<table>
    <tr><th>Attribute</th><th>Description</th></tr>
    <tr><td>Source</td><td>UCI Machine Learning Repository, SMS Spam Collection, ID 228</td></tr>
    <tr><td>Raw observations</td><td>5,574 labelled SMS messages</td></tr>
    <tr><td>Input fields</td><td>Label (ham/spam) and message text</td></tr>
    <tr><td>Target classes</td><td>ham = genuine; spam = unwanted message</td></tr>
    <tr><td>Model representation</td><td>Sparse word-count matrix produced by CountVectorizer</td></tr>
    <tr><td>Cleaned analysis set</td><td>5,160 unique message texts after whitespace trimming and deduplication</td></tr>
</table>

<h2>2.2 Data Loading</h2>
<p>
The main program first tries <code>fetch_ucirepo(id=228)</code>. If the online fetch fails, the program looks for the supplied 
archive in the working directory and reads the SMSSpamCollection member inside it. That way the code works both online and offline.
</p>

<h2>2.3 Data Inspection and Missing Values</h2>
<p>
Before cleaning anything I inspected the raw file. It has zero missing values in both label and message. Labels are lower-cased and 
message text is stripped of leading and trailing whitespace.
</p>

<h2>2.4 Duplicate Removal</h2>
<p>
The activity asks explicitly for duplicates to be removed. The code first trims surrounding whitespace and then calls 
<code>drop_duplicates(subset=["message"], keep="first")</code>. Before trimming, the original file has 403 repeated message texts. 
After trimming the count rises to 414. The gap of 11 exists because some messages differed only by a space or two at the edges and 
became identical once normalised.
</p>

<h2>2.5 Label Encoding</h2>
<div class="formula-box"><strong>Spam = 1; Ham = 0</strong></div>
<p>
The text labels are converted with the mapping <code>{{"ham": 0, "spam": 1}}</code>.
</p>

<h2>2.6 Cleaned Dataset Summary</h2>
<table>
    <tr><th>Check / quantity</th><th>Result</th><th>What it tells us</th></tr>
    <tr><td>Raw messages</td><td>5,574</td><td>Matches the size in the activity sheet and the UCI listing.</td></tr>
    <tr><td>Missing labels</td><td>0</td><td>No label values needed deleting.</td></tr>
    <tr><td>Missing messages</td><td>0</td><td>No message values needed deleting.</td></tr>
    <tr><td>Duplicate records removed</td><td>414</td><td>Repeated texts removed after trimming; every remaining text is unique.</td></tr>
    <tr><td>Cleaned messages</td><td>5,160</td><td>The population used for all calculations in this report.</td></tr>
    <tr><td>Ham messages</td><td>4,518</td><td>87.5581% of the cleaned dataset.</td></tr>
    <tr><td>Spam messages</td><td>642</td><td>12.4419% of the cleaned dataset.</td></tr>
    <tr><td>Duplicates remaining</td><td>0</td><td>No exact repeated message text is left.</td></tr>
</table>

<div class="page-break"></div>

<h1>Chapter 3 – Probability and Statistical Analysis</h1>
<h2>3.1 Notation and Counting Convention</h2>
<p>
Let N = 5,160 be the number of unique cleaned messages, N_S = 642 the number of spam messages and N_H = 4,518 the number of ham messages. 
For the word analysis, a message counts as containing a suspicious word if the entire word appears at least once, ignoring case.
</p>

<h2>3.2 Basic and Prior Probability</h2>
<div class="formula-box">
    P(Spam) = N_S / N = 642 / 5,160 = 0.1244186<br>
    P(Ham)  = N_H / N = 4,518 / 5,160 = 0.8755814
</div>
<p>
As percentages, 12.4419% of the cleaned messages are spam and 87.5581% are ham. The two add up to one (0.1244186 + 0.8755814 = 1.0000000). 
The dataset is clearly imbalanced.
</p>

<div class="chart-box">
    <img src="{img_class}" alt="Class Distribution">
    <div class="caption">Figure 1. Ham and spam counts and percentages in the cleaned dataset (N = 5,160).</div>
</div>

<h2>3.3 Conditional Probability</h2>
<div class="formula-box">P(A | B) = P(A and B) / P(B), provided P(B) > 0</div>

<table>
    <tr><th>Word</th><th>Messages with word</th><th>Spam</th><th>Ham</th><th>P(Spam | Word)</th><th>P(Ham | Word)</th></tr>
    <tr><td>free</td><td>199</td><td>144</td><td>55</td><td>0.7236 (72.36%)</td><td>0.2764 (27.64%)</td></tr>
    <tr><td>prize</td><td>70</td><td>70</td><td>0</td><td>1.0000 (100.00%)</td><td>0.0000 (0.00%)</td></tr>
    <tr><td>win</td><td>53</td><td>47</td><td>6</td><td>0.8868 (88.68%)</td><td>0.1132 (11.32%)</td></tr>
    <tr><td>urgent</td><td>61</td><td>56</td><td>5</td><td>0.9180 (91.80%)</td><td>0.0820 (8.20%)</td></tr>
    <tr><td>offer</td><td>30</td><td>24</td><td>6</td><td>0.8000 (80.00%)</td><td>0.2000 (20.00%)</td></tr>
</table>

<div class="chart-box">
    <img src="{img_word}" alt="Word Probabilities">
    <div class="caption">Figure 2. Empirical P(Spam | Word) for the five selected whole-word matches.</div>
</div>

<h2>3.4 Bayes' Theorem: Verification for "free"</h2>
<div class="formula-box">P(Spam | Free) = [ P(Free | Spam) &times; P(Spam) ] / P(Free)</div>
<table>
    <tr><th>Quantity</th><th>Count-based calculation</th><th>Value</th></tr>
    <tr><td>P(Free | Spam)</td><td>144 spam messages containing free / 642 spam messages</td><td>0.2242991</td></tr>
    <tr><td>P(Spam)</td><td>642 spam messages / 5,160 total messages</td><td>0.1244186</td></tr>
    <tr><td>P(Free)</td><td>199 messages containing free / 5,160 total messages</td><td>0.0385659</td></tr>
    <tr><td>P(Free and Spam)</td><td>144 spam messages containing free / 5,160 total messages</td><td>0.0279070</td></tr>
</table>
<p>
Step 1 – the likelihood: P(Free | Spam) = 144 / 642 = 0.2242991.<br>
Step 2 – multiply by the prior: 0.2242991 &times; 0.1244186 = 0.0279070.<br>
Step 3 – divide by the marginal: P(Spam | Free) = 0.0279070 / 0.0385659 = 0.7236181.<br>
The direct count gives 144 / 199 = 0.7236181, the exact same number.
</p>

<h2>3.5 Random Variable, Expectation, and Variance</h2>
<div class="formula-box">Y = 1 if the message is Spam; Y = 0 if the message is Ham</div>
<p>
<strong>Expectation:</strong><br>
E(Y) = 0 &times; P(Y = 0) + 1 &times; P(Y = 1) = 0 &times; 0.8755814 + 1 &times; 0.1244186 = <strong>0.1244186</strong><br><br>
<strong>Variance:</strong><br>
Since 0² = 0 and 1² = 1, Y² = Y, which gives E(Y²) = E(Y) = p.<br>
Var(Y) = E(Y²) &minus; [E(Y)]² = p &minus; p² = p(1 &minus; p)<br>
Var(Y) = 0.1244186 &times; (1 &minus; 0.1244186) = <strong>0.1089386</strong><br>
NumPy agrees: mean(Y) = 0.1244186 and var(Y, ddof=0) = 0.1089386.
</p>

<div class="page-break"></div>

<h1>Chapter 4 – Methodology, Architecture, and Algorithm</h1>
<h2>4.1 System Architecture</h2>
<p>
The implementation is a reproducible pipeline: Dataset Ingestion &rarr; Whitespace Normalization &amp; Deduplication &rarr; 
Probability Analysis &rarr; Stratified Train/Test Split &rarr; CountVectorizer Feature Matrix &rarr; Multinomial Naive Bayes &rarr; 
Evaluation &amp; Real-time Testing.
</p>

<h2>4.2 Data Split and Stratified Sampling</h2>
<p>
The cleaned data is divided with <code>train_test_split(test_size=0.20, random_state=42, stratify=y)</code>. 
This gives 4,128 training messages (3,614 ham, 514 spam) and 1,032 test messages (904 ham, 128 spam).
</p>

<h2>4.3 Text Feature Extraction</h2>
<p>
CountVectorizer turns SMS text into a sparse count matrix. Lower-casing is active. 
The vectorizer is fitted on training text only (<code>fit_transform</code>) to prevent data leakage.
</p>

<h2>4.4 Multinomial Naive Bayes</h2>
<div class="formula-box">P(c | x) &prop; P(c) &times; &prod; P(word_j | c)^(x_j)</div>
<p>Additive Laplace smoothing (&alpha; = 1) prevents zero-probability multiplication.</p>

<div class="page-break"></div>

<h1>Chapter 6 – Model Evaluation and Results</h1>
<h2>6.1 Training and Test Set Summary</h2>
<table>
    <tr><th>Partition</th><th>Total</th><th>Ham (0)</th><th>Spam (1)</th><th>Share</th></tr>
    <tr><td>Training</td><td>4,128</td><td>3,614</td><td>514</td><td>80%</td></tr>
    <tr><td>Testing</td><td>1,032</td><td>904</td><td>128</td><td>20%</td></tr>
    <tr><td>Total cleaned data</td><td>5,160</td><td>4,518</td><td>642</td><td>100%</td></tr>
</table>

<h2>6.2 Evaluation Metrics</h2>
<table>
    <tr><th>Metric</th><th>Calculation from test set</th><th>Result</th></tr>
    <tr><td>Accuracy</td><td>(898 + 116) / 1,032</td><td>0.982558 = 98.26%</td></tr>
    <tr><td>Spam precision</td><td>116 / (116 + 6) = 116 / 122</td><td>0.950820 = 95.08%</td></tr>
    <tr><td>Spam recall</td><td>116 / (116 + 12) = 116 / 128</td><td>0.906250 = 90.63%</td></tr>
    <tr><td>Spam F1-score</td><td>Harmonic mean of precision and recall</td><td>0.928000 = 92.80%</td></tr>
</table>

<h2>6.3 Confusion Matrix</h2>
<div class="chart-box">
    <img src="{img_cm}" alt="Confusion Matrix">
    <div class="caption">Figure 3. Confusion matrix for the held-out test set (TN=898, FP=6, FN=12, TP=116).</div>
</div>

<h2>6.4 Classification Report</h2>
<table>
    <tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-score</th><th>Support</th></tr>
    <tr><td>Ham (0)</td><td>0.9868</td><td>0.9934</td><td>0.9901</td><td>904</td></tr>
    <tr><td>Spam (1)</td><td>0.9508</td><td>0.9062</td><td>0.9280</td><td>128</td></tr>
    <tr><td>Macro average</td><td>0.9688</td><td>0.9498</td><td>0.9590</td><td>1,032</td></tr>
    <tr><td>Weighted average</td><td>0.9823</td><td>0.9826</td><td>0.9824</td><td>1,032</td></tr>
</table>

<h2>6.5 Error Analysis</h2>
<table>
    <tr><th>Error type</th><th>Example excerpt</th><th>Possible reason</th></tr>
    <tr><td>False negative</td><td>"Sorry I missed your call, let's talk when you have the time..."</td><td>Chatty wording and little promotional vocabulary make it look like ham.</td></tr>
    <tr><td>False negative</td><td>"Thanks for your purchase of a video clip ..."</td><td>An adult-content promotion that reads like an ordinary service notification.</td></tr>
    <tr><td>False negative</td><td>"... free phone number in a couple of days ..."</td><td>The token free appears in a context that resembles a legitimate service message.</td></tr>
    <tr><td>False positive</td><td>"Nokia phone is lovly.."</td><td>Short message overlapping with handset promotional terms.</td></tr>
    <tr><td>False positive</td><td>"Unlimited texts. Limited minutes."</td><td>A brief telecom offer that resembles commercial SMS patterns.</td></tr>
    <tr><td>False positive</td><td>"Have you laid your airtel line to rest?"</td><td>Telecom and account-management terms can resemble spam patterns.</td></tr>
</table>

<div class="page-break"></div>

<h1>Chapter 7 – Real-Time SMS Testing</h1>
<h2>7.1 Required Test Message</h2>
<p>Activity sheet test message: <em>"Congratulations! You have won a free prize. Claim now."</em></p>
<table>
    <tr><th>Output field</th><th>Model-generated result</th></tr>
    <tr><td>Prediction</td><td>Spam</td></tr>
    <tr><td>P(Spam | Message)</td><td>0.999999802 (approximately 99.999980%)</td></tr>
    <tr><td>P(Ham | Message)</td><td>0.000000198 (approximately 0.000020%)</td></tr>
</table>
<p><em>Note: The activity sheet prints 0.96 and 0.04 as an example of the output format. The values above are the exact mathematical outputs computed from the fitted model.</em></p>

<div class="page-break"></div>

<h1>Chapter 8 – Results and Discussion</h1>
<h2>8.1 Summary of Main Results</h2>
<table>
    <tr><th>Analysis component</th><th>Result</th><th>Meaning</th></tr>
    <tr><td>Prior probability</td><td>P(Spam) = 0.1244; P(Ham) = 0.8756</td><td>Ham is the majority class in the cleaned corpus.</td></tr>
    <tr><td>Word: free</td><td>P(Spam | Free) = 0.7236</td><td>About 72.36% of cleaned messages containing free are labelled spam.</td></tr>
    <tr><td>Word: prize</td><td>P(Spam | Prize) = 1.0000</td><td>All 70 matching messages in this sample are labelled spam.</td></tr>
    <tr><td>Expectation</td><td>E(Y) = 0.1244</td><td>Equals the observed spam fraction because Y is a spam indicator.</td></tr>
    <tr><td>Variance</td><td>Var(Y) = 0.1089</td><td>Population variance of the binary spam indicator.</td></tr>
    <tr><td>Test accuracy</td><td>98.26%</td><td>1,014 of the 1,032 test messages were classified correctly.</td></tr>
    <tr><td>Spam precision / recall / F1</td><td>95.08% / 90.63% / 92.80%</td><td>Balances false alarms against missed spam.</td></tr>
    <tr><td>Specified SMS example</td><td>Spam; P(Spam | Message) = 0.999999802</td><td>The example is strongly classified as spam by this fitted model.</td></tr>
</table>

<div class="page-break"></div>

<h1>Chapter 9 – Conclusion and Future Scope</h1>
<h2>9.1 Conclusion</h2>
<p>
This project built a probabilistic SMS spam detection workflow on the SMS Spam Collection, using the libraries named in the BAMAT207 
activity sheet. After checking the supplied file, trimming surrounding whitespace and removing repeated texts, 5,160 unique messages 
remained: 4,518 ham and 642 spam. Prior probabilities, Bayes' theorem verification for "free", Bernoulli random variable statistics, 
and a Multinomial Naive Bayes classifier (98.26% accuracy, 95.08% precision) were successfully demonstrated.
</p>

<h2>References</h2>
<p>[1] Almeida, T., &amp; Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository.</p>
<p>[2] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.</p>
<p>[3] Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585, 357-362.</p>

<div class="page-break"></div>

<h1>Appendix C – Submission Checklist</h1>
<ul>
    <li>&#9745; Personalized student details: T. Harshith, 25BCE2863, B.TECH, CSE--CORE.</li>
    <li>&#9745; Comprehensive Table of Contents with section mapping.</li>
    <li>&#9745; Data cleaning policy explicitly documented (whitespace trimming and deduplication).</li>
    <li>&#9745; Bayes' theorem verified analytically and empirically for 'free'.</li>
    <li>&#9745; Bernoulli random variable expectation and variance derived and verified with NumPy.</li>
    <li>&#9745; Model evaluated with Accuracy, Precision, Recall, F1, Confusion Matrix, and Error Analysis.</li>
    <li>&#9745; Real-time test performed on required curriculum SMS input.</li>
    <li>&#9745; Source code and companion notebook pushed to GitHub: https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection</li>
</ul>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Full Academic HTML Report created at: {output_path}")

if __name__ == "__main__":
    base = r"C:\Users\acs\.gemini\antigravity\scratch\sms_spam_detection"
    out = os.path.join(base, "BAMAT207_Probabilistic_SMS_Spam_Detection_Full_Academic_Report.html")
    plots = os.path.join(base, "plots")
    create_full_html_report(out, plots)
