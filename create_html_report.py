import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_f:
            encoded = base64.b64encode(img_f.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded}"
    return ""

def create_html_report(output_path, plots_dir):
    img_class = get_base64_image(os.path.join(plots_dir, "class_distribution.png"))
    img_word = get_base64_image(os.path.join(plots_dir, "word_probabilities.png"))
    img_cm = get_base64_image(os.path.join(plots_dir, "confusion_matrix.png"))
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BAMAT207 Project Report: Probabilistic SMS Spam Detection</title>
<style>
    @page {{
        margin: 20mm;
        size: A4;
    }}
    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        line-height: 1.6;
        color: #2c3e50;
        background: #fff;
        max-width: 900px;
        margin: 0 auto;
        padding: 30px;
    }}
    .header {{
        text-align: center;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }}
    h1 {{
        color: #1f4e79;
        font-size: 24px;
        margin: 0 0 10px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    h2 {{
        color: #595959;
        font-size: 16px;
        font-weight: 600;
        margin: 0;
    }}
    .meta-box {{
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 15px 20px;
        margin-bottom: 30px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        font-size: 14px;
    }}
    .meta-item {{
        display: flex;
    }}
    .meta-label {{
        font-weight: bold;
        color: #1f4e79;
        min-width: 160px;
    }}
    h3 {{
        color: #1f4e79;
        border-bottom: 1.5px solid #dce4ec;
        padding-bottom: 6px;
        margin-top: 35px;
        font-size: 18px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18px 0;
        font-size: 13.5px;
    }}
    th, td {{
        padding: 10px 12px;
        border: 1px solid #dee2e6;
        text-align: left;
    }}
    th {{
        background-color: #1f4e79;
        color: white;
        font-weight: 600;
    }}
    tr:nth-child(even) {{
        background-color: #fbfcfd;
    }}
    .math-block {{
        background: #fdfefe;
        border-left: 4px solid #1f4e79;
        padding: 12px 18px;
        margin: 15px 0;
        font-family: 'Cambria Math', 'Times New Roman', serif;
        font-size: 15px;
    }}
    .chart-container {{
        text-align: center;
        margin: 25px 0;
    }}
    .chart-container img {{
        max-width: 80%;
        height: auto;
        border-radius: 4px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .caption {{
        font-size: 12px;
        font-style: italic;
        color: #6c757d;
        margin-top: 6px;
    }}
    .badge {{
        background: #28a745;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }}
    @media print {{
        body {{
            padding: 0;
            max-width: 100%;
        }}
        .chart-container img {{
            max-width: 70%;
        }}
    }}
</style>
</head>
<body>

<div class="header">
    <h1>BAMAT207: Applications of Probability and Statistics</h1>
    <h2>Beyond the Words: A Probabilistic & Bayesian Approach to SMS Spam Detection</h2>
</div>

<div class="meta-box">
    <div class="meta-item"><span class="meta-label">Course:</span> Applications of Probability and Statistics</div>
    <div class="meta-item"><span class="meta-label">Topic:</span> Probability and Random Variables</div>
    <div class="meta-item"><span class="meta-label">Student Name / ID:</span> Harshith (Harshith1987)</div>
    <div class="meta-item"><span class="meta-label">Submission Date:</span> 27.10.2026</div>
    <div class="meta-item" style="grid-column: span 2;">
        <span class="meta-label">GitHub Repository:</span> 
        <a href="https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection" target="_blank">
            https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection
        </a>
    </div>
</div>

<h3>1. Executive Summary & Problem Formulation</h3>
<p>
    Unsolicited mobile communications (SMS spam) pose serious risks including identity theft, credential phishing, and financial fraud. 
    This project builds a mathematically rigorous, probabilistic system that classifies incoming SMS messages into 
    <strong>Spam (Y = 1)</strong> or <strong>Genuine / Ham (Y = 0)</strong>.
</p>
<p>
    The system grounds every stage in probability theory: prior probabilities are extracted from sample space partitions; 
    word features are evaluated using empirical conditional probabilities and verified via Bayes' Theorem; 
    the target state is modeled as a discrete Bernoulli random variable with analytical expectation and variance; 
    and a Multinomial Naive Bayes model is trained and evaluated using accuracy, precision, recall, F1-score, and confusion matrix auditing.
</p>

<h3>2. Dataset Handling & Class Distribution</h3>
<p>
    The project utilizes the <em>SMS Spam Collection</em> from the UCI Machine Learning Repository (ID: 228). 
    403 duplicate records were removed to prevent probability skewness.
</p>

<table>
    <tr>
        <th>Metric / Parameter</th>
        <th>Value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Raw Messages</td>
        <td>5,572</td>
        <td>Full UCI Corpus</td>
    </tr>
    <tr>
        <td>Missing Values</td>
        <td>0</td>
        <td>Clean dataset with complete labels and text</td>
    </tr>
    <tr>
        <td>Duplicate Records Removed</td>
        <td>403</td>
        <td>Removed redundant duplicate messages</td>
    </tr>
    <tr>
        <td>Clean Sample Space Size (N)</td>
        <td>5,169</td>
        <td>Total unique messages for probability estimation</td>
    </tr>
    <tr>
        <td>Prior Probability P(Ham)</td>
        <td>0.8737 (4,516 msgs)</td>
        <td>87.37% baseline probability of receiving genuine SMS</td>
    </tr>
    <tr>
        <td>Prior Probability P(Spam)</td>
        <td>0.1263 (653 msgs)</td>
        <td>12.63% baseline probability of receiving spam SMS</td>
    </tr>
</table>

<div class="chart-container">
    <img src="{img_class}" alt="Class Distribution">
    <div class="caption">Figure 1: SMS Dataset Class Distribution (Genuine Ham vs Spam)</div>
</div>

<h3>3. Word-Based Probability Analysis & Bayes' Theorem Verification</h3>
<p>
    We evaluate five curriculum suspicious keywords: <code>free</code>, <code>prize</code>, <code>win</code>, <code>urgent</code>, and <code>offer</code>. 
    We calculate the conditional probability P(Spam | Word) using both empirical observation and Bayes' Theorem:
</p>

<div class="math-block">
    <strong>Bayes' Theorem Formulation:</strong><br>
    P(Spam | Word) = [ P(Word | Spam) &times; P(Spam) ] / P(Word)<br>
    <strong>Analytical Equivalence:</strong><br>
    [ (N<sub>S &cap; W</sub> / N<sub>S</sub>) &times; (N<sub>S</sub> / N) ] / (N<sub>W</sub> / N) = N<sub>S &cap; W</sub> / N<sub>W</sub>
</div>

<table>
    <tr>
        <th>Word (W)</th>
        <th>Total (N<sub>W</sub>)</th>
        <th>Spam (N<sub>S</sub>)</th>
        <th>P(W | Spam)</th>
        <th>Empirical P(Spam | W)</th>
        <th>Bayes P(Spam | W)</th>
        <th>Verified</th>
    </tr>
    <tr>
        <td><strong>free</strong></td>
        <td>203</td>
        <td>148</td>
        <td>0.2266</td>
        <td>72.91%</td>
        <td>72.91%</td>
        <td><span class="badge">Verified</span></td>
    </tr>
    <tr>
        <td><strong>prize</strong></td>
        <td>73</td>
        <td>73</td>
        <td>0.1118</td>
        <td>100.00%</td>
        <td>100.00%</td>
        <td><span class="badge">Verified</span></td>
    </tr>
    <tr>
        <td><strong>win</strong></td>
        <td>55</td>
        <td>49</td>
        <td>0.0750</td>
        <td>89.09%</td>
        <td>89.09%</td>
        <td><span class="badge">Verified</span></td>
    </tr>
    <tr>
        <td><strong>urgent</strong></td>
        <td>62</td>
        <td>57</td>
        <td>0.0873</td>
        <td>91.94%</td>
        <td>91.94%</td>
        <td><span class="badge">Verified</span></td>
    </tr>
    <tr>
        <td><strong>offer</strong></td>
        <td>30</td>
        <td>24</td>
        <td>0.0368</td>
        <td>80.00%</td>
        <td>80.00%</td>
        <td><span class="badge">Verified</span></td>
    </tr>
</table>

<div class="chart-container">
    <img src="{img_word}" alt="Word Probabilities">
    <div class="caption">Figure 2: Conditional Probability P(Spam | Word) for Suspicious Keywords</div>
</div>

<h3>4. Random Variable Analysis (Bernoulli Process)</h3>
<p>
    Let Y be the discrete binary random variable defining the message classification state:
    Y = 1 if Spam, and Y = 0 if Ham. Therefore, Y follows a Bernoulli distribution: 
    <strong>Y ~ Bernoulli(p)</strong> where p = P(Spam) = 0.1263.
</p>

<div class="math-block">
    &bull; <strong>Expectation E(Y):</strong> E(Y) = &sum; y &times; P(Y = y) = (1 &times; p) + (0 &times; (1 - p)) = p = <strong>0.1263</strong><br>
    &bull; <strong>Variance Var(Y):</strong> Var(Y) = E[Y<sup>2</sup>] - (E[Y])<sup>2</sup> = p(1 - p) = 0.1263 &times; 0.8737 = <strong>0.1104</strong><br>
    &bull; <strong>Standard Deviation SD(Y):</strong> SD(Y) = &radic;Var(Y) = &radic;0.1104 = <strong>0.3322</strong>
</div>

<h3>5. Model Building & Evaluation (Multinomial Naive Bayes)</h3>
<p>
    The dataset was split using an <strong>80/20 stratified split</strong> (4,135 training, 1,034 testing samples). 
    Features were extracted using <code>CountVectorizer</code> (7,414 unique word tokens). 
    A <code>MultinomialNB</code> model was trained with Laplace Add-1 smoothing (&alpha; = 1.0).
</p>

<table>
    <tr>
        <th>Performance Metric</th>
        <th>Score (Decimal)</th>
        <th>Score (%)</th>
    </tr>
    <tr>
        <td><strong>Accuracy</strong></td>
        <td>0.9836</td>
        <td><strong>98.36%</strong></td>
    </tr>
    <tr>
        <td><strong>Precision (Spam)</strong></td>
        <td>0.9597</td>
        <td><strong>95.97%</strong></td>
    </tr>
    <tr>
        <td><strong>Recall (Spam)</strong></td>
        <td>0.9084</td>
        <td><strong>90.84%</strong></td>
    </tr>
    <tr>
        <td><strong>F1-Score (Spam)</strong></td>
        <td>0.9333</td>
        <td><strong>0.9333</strong></td>
    </tr>
</table>

<div class="chart-container">
    <img src="{img_cm}" alt="Confusion Matrix">
    <div class="caption">Figure 3: Confusion Matrix on 1,034 Held-out Test Samples</div>
</div>

<p>
    <strong>Error Breakdown:</strong>
    <br>&bull; <strong>False Positives (5):</strong> Genuine messages misclassified as spam (e.g., <em>"Are you free now?can i call now?"</em> due to "free"). High precision (95.97%) ensures minimal legitimate messages are misrouted.
    <br>&bull; <strong>False Negatives (12):</strong> Spam messages misclassified as genuine due to rare or non-standard character sequences.
</p>

<h3>6. Real-Time Inference Demonstrations</h3>
<table>
    <tr>
        <th>Incoming SMS Message</th>
        <th>Predicted Class</th>
        <th>P(Spam | Message)</th>
        <th>P(Ham | Message)</th>
    </tr>
    <tr>
        <td>"Congratulations! You have won a free prize. Claim now."</td>
        <td><strong style="color: #d9534f;">Spam</strong></td>
        <td>1.0000 (100.00%)</td>
        <td>0.0000 (0.00%)</td>
    </tr>
    <tr>
        <td>"Hey, are you free this afternoon to study for the BAMAT207 exam?"</td>
        <td><strong style="color: #2b5c8f;">Genuine (Ham)</strong></td>
        <td>0.0006 (0.06%)</td>
        <td>0.9994 (99.94%)</td>
    </tr>
    <tr>
        <td>"URGENT! Your mobile account has won an exclusive $1,000 cash offer."</td>
        <td><strong style="color: #d9534f;">Spam</strong></td>
        <td>1.0000 (100.00%)</td>
        <td>0.0000 (0.00%)</td>
    </tr>
    <tr>
        <td>"Can you send me the lecture notes when you get home?"</td>
        <td><strong style="color: #2b5c8f;">Genuine (Ham)</strong></td>
        <td>0.0028 (0.28%)</td>
        <td>0.9972 (99.72%)</td>
    </tr>
    <tr>
        <td>"Win a brand new car today! Free entry, text WIN to 80085 immediately."</td>
        <td><strong style="color: #d9534f;">Spam</strong></td>
        <td>0.9999 (99.99%)</td>
        <td>0.0001 (0.01%)</td>
    </tr>
</table>

<h3>7. Submission Information</h3>
<p>
    <strong>GitHub Repository Link:</strong><br>
    <a href="https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection" target="_blank">
        https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection
    </a>
</p>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML Report successfully created at: {output_path}")

if __name__ == "__main__":
    base_dir = r"C:\Users\acs\.gemini\antigravity\scratch\sms_spam_detection"
    plots_dir = os.path.join(base_dir, "plots")
    out_file = os.path.join(base_dir, "BAMAT207_Project_Report.html")
    create_html_report(out_file, plots_dir)
