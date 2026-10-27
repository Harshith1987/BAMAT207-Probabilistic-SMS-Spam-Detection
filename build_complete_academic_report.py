import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.text = "BAMAT207 | Beyond the Words: A Probabilistic & Bayesian Approach to SMS Spam Detection"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.text = "Applications of Probability and Statistics - Student Project Report"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(128, 128, 128)

def build_full_report(output_docx, plots_dir):
    doc = Document()
    add_header_footer(doc)
    
    # ------------------ COVER PAGE ------------------
    for _ in range(3):
        doc.add_paragraph()
        
    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run("PROJECT REPORT")
    r_tag.font.name = "Arial"
    r_tag.font.size = Pt(11)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(224, 102, 102)
    
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Beyond the Words:\nA Probabilistic and Bayesian Approach to SMS Spam Detection")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(31, 78, 121)
    
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("An Empirical Study of Random Variables, Bayes' Theorem, and Multinomial Naive Bayes")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(89, 89, 89)
    
    p_divider = doc.add_paragraph()
    r_div = p_divider.add_run("―" * 55)
    r_div.font.color.rgb = RGBColor(230, 145, 56)
    
    for _ in range(3):
        doc.add_paragraph()
        
    p_req = doc.add_paragraph()
    r_req = p_req.add_run("Submitted in partial fulfilment of the requirements for\n")
    r_req.font.name = "Arial"
    r_req.font.size = Pt(10)
    r_course = p_req.add_run("BAMAT207 – Probability and Statistics")
    r_course.font.name = "Arial"
    r_course.font.size = Pt(11)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(31, 78, 121)
    
    doc.add_paragraph()
    
    p_meta = doc.add_paragraph()
    p_meta.add_run("Student name: ").font.bold = True
    p_meta.add_run("T. HARSHITH\n")
    p_meta.add_run("Registration number: ").font.bold = True
    p_meta.add_run("25BCE2863\n")
    p_meta.add_run("Programme / Department: ").font.bold = True
    p_meta.add_run("B.TECH, CSE--CORE\n")
    p_meta.add_run("GitHub Repository: ").font.bold = True
    p_meta.add_run("https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection")
    
    for run in p_meta.runs:
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        
    doc.add_page_break()
    
    # ------------------ ABSTRACT ------------------
    h_abs = doc.add_heading("Abstract", level=1)
    h_abs.runs[0].font.color.rgb = RGBColor(31, 78, 121)
    
    p_abs1 = doc.add_paragraph(
        "Most of us receive unwanted text messages every week: prize notifications, urgent promotional offers, "
        "and phishing links we would never knowingly click. Sorting malicious spam from genuine personal communications "
        "is a quintessential text-classification challenge. In this project, I address this problem using the mathematical "
        "rigor of probability theory and discrete random variables. The data originates from the UCI SMS Spam Collection "
        "(dataset ID: 228), containing 5,574 labeled messages. Following whitespace normalization and thorough deduplication, "
        "5,160 unique messages remained for primary empirical analysis: 4,518 genuine messages (ham) and 642 spam messages."
    )
    
    p_abs2 = doc.add_paragraph(
        "The statistical foundations are established first. I compute the empirical prior probabilities from the class frequencies, "
        "analyze the occurrence of five suspicious keywords (\"free\", \"prize\", \"win\", \"urgent\", and \"offer\"), and calculate "
        "the conditional probabilities P(Spam | Word) and P(Ham | Word) through whole-word boundary matching. I rigorously prove "
        "and verify Bayes' theorem against the empirical counts for \"free\". Furthermore, I formulate the spam classification state "
        "as a discrete Bernoulli random variable Y (Y = 1 for spam, Y = 0 for ham) and analytically derive its mathematical expectation "
        "and population variance."
    )
    
    p_abs3 = doc.add_paragraph(
        "For machine-learning classification, message texts are converted into bag-of-words count representations using CountVectorizer "
        "and supplied to a Multinomial Naive Bayes model under a stratified 80:20 train-test split (random_state=42). To maintain strict "
        "leakage control, the vectorizer is fitted strictly on training data. On the held-out test partition, the model achieves an overall "
        "accuracy of 98.26%, spam precision of 95.08%, recall of 90.63%, and an F1-score of 92.80%. The confusion matrix records 898 true "
        "negatives, 6 false positives, 12 false negatives, and 116 true positives. When tested on the required curriculum message, "
        "\"Congratulations! You have won a free prize. Claim now.\", the system classifies it as spam with a model-generated posterior "
        "P(Spam | Message) of 0.999999802. Together, the project provides a unified, fully reproducible workflow linking foundational "
        "probability theory, random variables, and AI text classification."
    )
    
    p_kw = doc.add_paragraph()
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.font.bold = True
    p_kw.add_run("SMS spam detection, Prior probability, Conditional probability, Bayes' theorem, Bernoulli random variable, Expectation, Variance, CountVectorizer, Multinomial Naive Bayes.")
    
    doc.add_page_break()
    
    # ------------------ TABLE OF CONTENTS ------------------
    h_toc = doc.add_heading("Table of Contents", level=1)
    h_toc.runs[0].font.color.rgb = RGBColor(31, 78, 121)
    
    toc_items = [
        ("Abstract", "2"),
        ("Chapter 1 – Introduction", "4"),
        ("  1.1 Background", "4"),
        ("  1.2 Problem Statement", "4"),
        ("  1.3 Aim and Objectives", "4"),
        ("  1.4 Scope", "5"),
        ("  1.5 Applications", "5"),
        ("Chapter 2 – Dataset Description and Preparation", "6"),
        ("  2.1 Dataset Source and Structure", "6"),
        ("  2.2 Data Loading & Offline Fallback", "6"),
        ("  2.3 Data Inspection and Missing Values", "6"),
        ("  2.4 Duplicate Removal & Normalization", "7"),
        ("  2.5 Label Encoding", "7"),
        ("  2.6 Cleaned Dataset Summary", "7"),
        ("Chapter 3 – Probability and Statistical Analysis", "8"),
        ("  3.1 Notation and Counting Convention", "8"),
        ("  3.2 Basic and Prior Probability", "8"),
        ("  3.3 Conditional Probability", "9"),
        ("  3.4 Bayes' Theorem: Verification for 'free'", "10"),
        ("  3.5 Random Variable, Expectation, and Variance", "11"),
        ("    3.5.1 Expectation", "11"),
        ("    3.5.2 Variance", "11"),
        ("  3.6 What the Probability Analysis Does and Does Not Mean", "12"),
        ("Chapter 4 – Methodology, Architecture, and Algorithm", "13"),
        ("  4.1 System Architecture", "13"),
        ("  4.2 Data Split and Stratified Sampling", "13"),
        ("  4.3 Text Feature Extraction", "13"),
        ("  4.4 Multinomial Naive Bayes", "14"),
        ("  4.5 Complete Algorithm", "14"),
        ("  4.6 Reproducibility and Leakage Control", "15"),
        ("Chapter 5 – Complete Python Implementation", "16"),
        ("  5.1 Runtime Environment and Dependencies", "16"),
        ("  5.2 Implementation Components", "16"),
        ("  5.3 Execution Sequence", "17"),
        ("  5.4 Expected Inputs and Outputs", "17"),
        ("Chapter 6 – Model Evaluation and Results", "18"),
        ("  6.1 Training and Test Set Summary", "18"),
        ("  6.2 Evaluation Metrics", "18"),
        ("  6.3 Confusion Matrix", "19"),
        ("  6.4 Classification Report", "20"),
        ("  6.5 In-Depth Error Analysis (FP vs FN)", "20"),
        ("Chapter 7 – Real-Time SMS Testing", "22"),
        ("  7.1 Required Test Message Demonstration", "22"),
        ("  7.2 Interactive Testing Procedure", "22"),
        ("Chapter 8 – Results and Discussion", "23"),
        ("  8.1 Summary of Main Findings", "23"),
        ("  8.2 Linking Statistics to the Classifier", "23"),
        ("  8.3 Strengths of the Probabilistic Approach", "24"),
        ("  8.4 Limitations and Validity Considerations", "24"),
        ("Chapter 9 – Conclusion and Future Scope", "25"),
        ("  9.1 Conclusion", "25"),
        ("  9.2 Future Scope", "25"),
        ("References", "26"),
        ("Appendix A – Complete Python Source Code", "27"),
        ("Appendix B – Verified Output Snapshot", "30"),
        ("Appendix C – Submission Checklist", "31")
    ]
    
    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (title, page) in enumerate(toc_items):
        r = t_toc.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.text = title
        c1.text = page
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if "Chapter" in title or "Appendix" in title or "Abstract" in title or "References" in title:
            c0.paragraphs[0].runs[0].font.bold = True
            c1.paragraphs[0].runs[0].font.bold = True
            
    doc.add_page_break()
    
    # ------------------ CHAPTER 1 ------------------
    doc.add_heading("Chapter 1 – Introduction", level=1)
    doc.add_heading("1.1 Background", level=2)
    doc.add_paragraph(
        "Mobile Short Message Service (SMS) remains one of the most widely adopted personal and commercial communication "
        "channels globally. People rely on SMS messages for conversational chatting, banking one-time passwords (OTPs), parcel "
        "delivery notifications, and critical two-factor authentication alerts. Unfortunately, the universal reach and high open "
        "rates of SMS have made it a lucrative vector for malicious actors deploying deceptive marketing, fake lottery notifications, "
        "advance-fee scams, and credential phishing links.\n\n"
        "Unlike rich emails, an SMS message is intrinsically short (typically constrained to 160 characters), lacks rich header metadata, "
        "and possesses minimal syntactic structure. Consequently, automated spam filtering must extract strong probabilistic signals directly "
        "from the distribution of words. Probability theory provides the foundational mathematical framework for this task: prior "
        "probabilities quantify base-rate risks before inspecting text, conditional probabilities measure how specific tokens alter suspicion, "
        "and Bayes' theorem enables dynamic belief updating upon observing textual evidence."
    )
    
    doc.add_heading("1.2 Problem Statement", level=2)
    doc.add_paragraph(
        "The objective is to design, implement, and evaluate a Python-based probabilistic classification system capable of classifying "
        "an incoming SMS message into one of two mutually exclusive classes: Spam (unwanted/malicious, Y = 1) or Ham (genuine, Y = 0). "
        "The system must perform rigorous dataset hygiene, calculate exact prior and conditional probabilities, verify Bayes' theorem, "
        "model classification uncertainty via a Bernoulli random variable, train a Multinomial Naive Bayes classifier on word count representations, "
        "and output calibrated posterior class probabilities for real-time testing."
    )
    
    doc.add_heading("1.3 Aim and Objectives", level=2)
    objs = [
        "Load the SMS Spam Collection from the UCI Machine Learning Repository (dataset ID 228) with reliable offline fallback support.",
        "Perform data cleaning: detect missing values, normalize casing and whitespace, remove redundant messages, and encode labels (Spam = 1, Ham = 0).",
        "Compute empirical prior probabilities P(Spam) and P(Ham), and visualize the class distribution.",
        "Calculate message-level conditional probabilities for five suspicious keywords: 'free', 'prize', 'win', 'urgent', and 'offer' using whole-word boundary matching.",
        "Verify P(Spam | free) using Bayes' theorem and prove its analytical equivalence to empirical ratios.",
        "Define the classification state as a Bernoulli random variable Y and compute its expectation and population variance.",
        "Construct an 80:20 stratified train-test split, extract word-count features with CountVectorizer, and train a Multinomial Naive Bayes classifier.",
        "Evaluate the classifier using Accuracy, Precision, Recall, F1-score, Confusion Matrix, and detailed error auditing.",
        "Test the model on curriculum sample messages (including 'Congratulations! You have won a free prize. Claim now.') and provide an interactive testing interface."
    ]
    for ob in objs:
        doc.add_paragraph(f"• {ob}")
        
    doc.add_heading("1.4 Scope", level=2)
    doc.add_paragraph(
        "The project focuses on binary classification of English SMS messages using the benchmark UCI repository. Word-level probability "
        "computations use case-insensitive whole-word boundary matching where multiple occurrences within a single message increment the count once. "
        "The machine-learning pipeline uses discrete word-frequency features with Multinomial Naive Bayes and Laplace smoothing."
    )
    
    doc.add_heading("1.5 Applications", level=2)
    apps = [
        "Carrier-level and mobile OS spam filtering to shield subscribers from deceptive messages.",
        "Security triage systems prioritizing high-risk SMS messages for manual compliance and fraud reviews.",
        "Educational illustration bridging formal mathematical probability and practical AI machine-learning pipelines.",
        "Extensible baseline for modern phishing, smishing, and malicious URL detection systems."
    ]
    for ap in apps:
        doc.add_paragraph(f"• {ap}")
        
    doc.add_page_break()
    
    # ------------------ CHAPTER 2 ------------------
    doc.add_heading("Chapter 2 – Dataset Description and Preparation", level=1)
    doc.add_heading("2.1 Dataset Source and Structure", level=2)
    doc.add_paragraph(
        "The project utilizes the SMS Spam Collection from the UCI Machine Learning Repository (Dataset ID: 228). UCI documents the dataset "
        "as a collection of 5,574 labeled SMS messages gathered from mobile phone research sources. The dataset contains two fields: "
        "the class label ('ham' or 'spam') and the raw text message."
    )
    
    t_ds = doc.add_table(rows=6, cols=2)
    t_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    ds_rows = [
        ("Attribute", "Description"),
        ("Source", "UCI Machine Learning Repository, SMS Spam Collection (ID: 228)"),
        ("Raw Observations", "5,574 labeled SMS messages (5,572 in raw TSV)"),
        ("Input Fields", "Label (ham / spam) and Message text"),
        ("Target Classes", "Ham = genuine message; Spam = unwanted/malicious message"),
        ("Cleaned Dataset", "5,160 unique message texts after whitespace trimming and deduplication")
    ]
    for i, (k, v) in enumerate(ds_rows):
        r = t_ds.rows[i]
        r.cells[0].text, r.cells[1].text = k, v
        if i == 0:
            set_cell_background(r.cells[0], "1F4E79")
            set_cell_background(r.cells[1], "1F4E79")
            r.cells[0].paragraphs[0].runs[0].font.bold = True
            r.cells[1].paragraphs[0].runs[0].font.bold = True
            r.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            r.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            r.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
            r.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)
            if i % 2 == 1:
                set_cell_background(r.cells[0], "F9FBFD")
                set_cell_background(r.cells[1], "F9FBFD")
                
    doc.add_heading("2.2 Data Loading", level=2)
    doc.add_paragraph(
        "The implementation provides dual data-ingestion pathways. It first attempts to fetch the dataset programmatically via ucimlrepo(id=228). "
        "If internet connectivity is restricted, it seamlessly falls back to reading the local SMSSpamCollection archive. A standardize_dataset() "
        "helper maps varying column schemas consistently to standard 'label' and 'message' columns."
    )
    
    doc.add_heading("2.3 Data Inspection and Missing Values", level=2)
    doc.add_paragraph(
        "Initial exploration confirmed that the dataset contains zero null or missing values across both fields. Text messages were stripped "
        "of surrounding whitespace and labels were normalized to lowercase."
    )
    
    doc.add_heading("2.4 Duplicate Removal", level=2)
    doc.add_paragraph(
        "Deduplication is vital in text classification. In the raw dataset, 403 exact string duplicates were identified. Following whitespace "
        "trimming, this count rose to 414 duplicate records, indicating that 11 messages differed solely by peripheral spaces. Deduplication "
        "yielded 5,160 unique messages (4,518 ham and 642 spam). Crucially, no message text appeared with conflicting labels."
    )
    
    doc.add_heading("2.5 Label Encoding", level=2)
    doc.add_paragraph(
        "Labels are numerically encoded using the standard binary mapping:\n"
        "  Spam = 1, Ham = 0\n"
        "This numerical indicator variable serves as the foundation for the Bernoulli random variable modeling and scikit-learn evaluation."
    )
    
    doc.add_heading("2.6 Cleaned Dataset Summary", level=2)
    t_cl = doc.add_table(rows=7, cols=3)
    t_cl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cl_data = [
        ("Check / Quantity", "Result", "Statistical Interpretation"),
        ("Raw Messages", "5,574", "Full corpus from UCI repository"),
        ("Missing Values", "0", "No imputation needed"),
        ("Duplicates Removed", "414", "Deduplicated after whitespace trimming"),
        ("Cleaned Population (N)", "5,160", "Total unique messages for probability estimation"),
        ("Ham Messages", "4,518", "87.5581% of cleaned dataset"),
        ("Spam Messages", "642", "12.4419% of cleaned dataset")
    ]
    for i, (c1, c2, c3) in enumerate(cl_data):
        r = t_cl.rows[i]
        r.cells[0].text, r.cells[1].text, r.cells[2].text = c1, c2, c3
        if i == 0:
            for cell in r.cells:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            for cell in r.cells:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")
                    
    doc.add_page_break()
    
    # ------------------ CHAPTER 3 ------------------
    doc.add_heading("Chapter 3 – Probability and Statistical Analysis", level=1)
    doc.add_heading("3.1 Notation and Counting Convention", level=2)
    doc.add_paragraph(
        "Let N = 5,160 be the size of the sample space of unique cleaned messages, N_S = 642 the count of spam messages, and N_H = 4,518 the count "
        "of genuine ham messages. For word-level probability estimation, a message is counted if the whole word appears at least once using "
        "case-insensitive regex boundaries (\\bword\\b). Multiple occurrences within one message are treated as a single event."
    )
    
    doc.add_heading("3.2 Basic and Prior Probability", level=2)
    doc.add_paragraph(
        "The prior probability represents the unconditional likelihood of drawing a specific class at random:\n"
        "  P(Spam) = N_S / N = 642 / 5,160 = 0.1244186 (12.4419%)\n"
        "  P(Ham)  = N_H / N = 4,518 / 5,160 = 0.8755814 (87.5581%)\n"
        "  P(Spam) + P(Ham) = 1.0000000\n\n"
        "The class distribution is heavily imbalanced: genuine messages outnumber spam by a factor of 7 to 1."
    )
    
    # Class Plot
    cp_path = os.path.join(plots_dir, "class_distribution.png")
    if os.path.exists(cp_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(cp_path, width=Inches(4.8))
        c_p = doc.add_paragraph("Figure 1: Class Distribution of Cleaned SMS Messages")
        c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_p.runs[0].font.size = Pt(9)
        c_p.runs[0].font.italic = True
        
    doc.add_heading("3.3 Conditional Probability", level=2)
    doc.add_paragraph(
        "Conditional probability quantifies how the probability of an outcome updates given new evidence:\n"
        "  P(A | B) = P(A ∩ B) / P(B), provided P(B) > 0\n\n"
        "For each suspicious word W, P(Spam | W) denotes the proportion of messages containing W that are spam:"
    )
    
    t_wp = doc.add_table(rows=6, cols=6)
    t_wp.alignment = WD_TABLE_ALIGNMENT.CENTER
    wp_data = [
        ("Word (W)", "Total (N_W)", "Spam (N_S)", "Ham (N_H)", "P(Spam | Word)", "P(Ham | Word)"),
        ("free", "199", "144", "55", "0.7236 (72.36%)", "0.2764 (27.64%)"),
        ("prize", "70", "70", "0", "1.0000 (100.0%)", "0.0000 (0.00%)"),
        ("win", "53", "47", "6", "0.8868 (88.68%)", "0.1132 (11.32%)"),
        ("urgent", "61", "56", "5", "0.9180 (91.80%)", "0.0820 (8.20%)"),
        ("offer", "30", "24", "6", "0.8000 (80.00%)", "0.2000 (20.00%)")
    ]
    for i, row in enumerate(wp_data):
        for j, val in enumerate(row):
            cell = t_wp.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")
                    
    doc.add_paragraph(
        "\nDetailed Observations on Keywords:\n"
        "• 'free': 144 of 199 messages containing 'free' are spam (72.36%). Although heavily leaning towards spam, 55 messages are genuine, so 'free' alone is not definitive.\n"
        "• 'prize': All 70 messages containing 'prize' are spam (100.0%), making it an exceptional spam indicator in this dataset.\n"
        "• 'win': 47 of 53 messages are spam (88.68%), with 6 genuine instances.\n"
        "• 'urgent': 56 of 61 messages are spam (91.80%).\n"
        "• 'offer': 24 of 30 messages are spam (80.00%)."
    )
    
    # Word Plot
    wp_path = os.path.join(plots_dir, "word_probabilities.png")
    if os.path.exists(wp_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(wp_path, width=Inches(4.8))
        c_p = doc.add_paragraph("Figure 2: Empirical P(Spam | Word) for Suspicious Keywords")
        c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_p.runs[0].font.size = Pt(9)
        c_p.runs[0].font.italic = True

    doc.add_heading("3.4 Bayes' Theorem: Verification for 'free'", level=2)
    doc.add_paragraph(
        "Bayes' theorem inverts conditional probabilities:\n"
        "  P(Spam | free) = [ P(free | Spam) × P(Spam) ] / P(free)\n\n"
        "Step-by-step calculation:\n"
        "1. Likelihood: P(free | Spam) = 144 / 642 = 0.2242991\n"
        "2. Multiply by Prior: P(free | Spam) × P(Spam) = 0.2242991 × 0.1244186 = 0.0279070\n"
        "3. Divide by Marginal Evidence: P(Spam | free) = 0.0279070 / 0.0385659 = 0.7236181 (72.36%)\n\n"
        "Direct empirical check: 144 / 199 = 0.7236181. Both approaches yield identical numerical values, verifying Bayes' theorem."
    )

    doc.add_heading("3.5 Random Variable, Expectation, and Variance", level=2)
    doc.add_paragraph(
        "Let Y be the discrete Bernoulli random variable:\n"
        "  Y = 1 if message is Spam\n"
        "  Y = 0 if message is Ham\n\n"
        "Parameter: p = P(Spam) = 0.1244186, q = 1 - p = 0.8755814\n\n"
        "3.5.1 Expectation:\n"
        "  E(Y) = Σ y × P(Y = y) = (0 × q) + (1 × p) = p = 0.1244186\n\n"
        "3.5.2 Variance:\n"
        "  Since Y takes values {0, 1}, Y² = Y. Thus E(Y²) = E(Y) = p.\n"
        "  Var(Y) = E(Y²) - [E(Y)]² = p - p² = p(1 - p)\n"
        "  Var(Y) = 0.1244186 × 0.8755814 = 0.1089386\n\n"
        "NumPy verification: np.mean(Y) = 0.1244186 and np.var(Y, ddof=0) = 0.1089386."
    )

    doc.add_heading("3.6 What the Probability Analysis Does and Does Not Mean", level=2)
    doc.add_paragraph(
        "Word-level probabilities reflect empirical frequencies within this specific corpus. P(Spam | prize) = 100% does not mean every future "
        "prize message will be spam. Single-word rules are vulnerable to context shifts, motivating multi-token machine learning models."
    )
    
    doc.add_page_break()
    
    # ------------------ CHAPTER 4 ------------------
    doc.add_heading("Chapter 4 – Methodology, Architecture, and Algorithm", level=1)
    doc.add_heading("4.1 System Architecture", level=2)
    doc.add_paragraph(
        "The system follows a sequential pipeline: Data Ingestion -> Text Normalization & Deduplication -> Statistical & Random Variable Analysis "
        "-> Stratified Train-Test Split -> CountVectorizer Feature Matrix Generation -> Multinomial Naive Bayes Training -> Evaluation & Inference."
    )
    
    doc.add_heading("4.2 Data Split and Stratified Sampling", level=2)
    doc.add_paragraph(
        "The cleaned dataset of 5,160 messages is split into an 80% training set (4,128 messages: 3,614 ham, 514 spam) and a 20% test set "
        "(1,032 messages: 904 ham, 128 spam). Stratification ensures class balance is strictly preserved across both partitions."
    )
    
    doc.add_heading("4.3 Text Feature Extraction", level=2)
    doc.add_paragraph(
        "CountVectorizer converts raw text into a sparse token-count matrix. The vocabulary is fitted strictly on the training set (7,673 unique tokens) "
        "to prevent data leakage. The test set is transformed using this learned vocabulary."
    )
    
    doc.add_heading("4.4 Multinomial Naive Bayes", level=2)
    doc.add_paragraph(
        "Multinomial Naive Bayes assumes that word occurrences are conditionally independent given the class label c:\n"
        "  P(c | x) ∝ P(c) × ∏ P(word_j | c)^(x_j)\n"
        "Laplace smoothing (alpha = 1.0) is applied to prevent zero-probability multiplications for unseen tokens."
    )
    
    doc.add_heading("4.5 Complete Algorithm", level=2)
    steps = [
        "Load the UCI SMS Spam Collection dataset with offline fallback.",
        "Normalize whitespace and casing; remove 414 duplicate records.",
        "Encode labels numerically: Ham = 0, Spam = 1.",
        "Compute class priors P(Ham) and P(Spam); evaluate word-level conditional probabilities for 5 suspicious keywords.",
        "Verify Bayes' theorem analytically and empirically for 'free'.",
        "Derive expectation E(Y) and population variance Var(Y) of the Bernoulli random variable.",
        "Partition data into 80:20 stratified train/test sets with random_state=42.",
        "Fit CountVectorizer on training data; transform training and test text.",
        "Fit MultinomialNB on training features and labels.",
        "Evaluate model: compute Accuracy, Precision, Recall, F1, Confusion Matrix, and conduct Error Auditing.",
        "Test curriculum example and provide an interactive prediction CLI."
    ]
    for idx, s in enumerate(steps, start=1):
        doc.add_paragraph(f"{idx}. {s}")
        
    doc.add_heading("4.6 Reproducibility and Leakage Control", level=2)
    doc.add_paragraph(
        "Strict reproducibility is maintained: random_state is fixed at 42, deduplication precedes data splitting, and vocabulary construction "
        "is isolated to training observations."
    )
    
    doc.add_page_break()
    
    # ------------------ CHAPTER 5 ------------------
    doc.add_heading("Chapter 5 – Complete Python Implementation", level=1)
    doc.add_heading("5.1 Runtime Environment and Dependencies", level=2)
    doc.add_paragraph(
        "The project is implemented in Python 3.11/3.13 utilizing standard scientific packages:\n"
        "%pip install -q pandas numpy matplotlib scikit-learn ucimlrepo"
    )
    
    doc.add_heading("5.2 Implementation Components", level=2)
    t_fn = doc.add_table(rows=9, cols=2)
    t_fn.alignment = WD_TABLE_ALIGNMENT.CENTER
    fn_data = [
        ("Function / Component", "Purpose"),
        ("standardize_dataset()", "Normalizes downloaded UCI schema into uniform label and message columns."),
        ("load_sms_dataset()", "Retrieves UCI dataset ID 228 with seamless offline ZIP fallback."),
        ("clean_dataset()", "Handles missing values, strips whitespace, filters classes, removes duplicates, encodes labels."),
        ("message_contains_word()", "Performs case-insensitive whole-word matching using regular expressions."),
        ("calculate_word_probabilities()", "Computes word occurrence frequencies and empirical conditional probabilities."),
        ("train_and_evaluate()", "Executes stratified split, vectorizer fitting, Naive Bayes training, and test evaluation."),
        ("predict_sms()", "Outputs predicted label and posterior probabilities P(Spam|Msg) and P(Ham|Msg)."),
        ("interactive_test()", "Provides an interactive CLI loop accepting custom SMS inputs.")
    ]
    for i, (f, p) in enumerate(fn_data):
        r = t_fn.rows[i]
        r.cells[0].text, r.cells[1].text = f, p
        if i == 0:
            set_cell_background(r.cells[0], "1F4E79")
            set_cell_background(r.cells[1], "1F4E79")
            r.cells[0].paragraphs[0].runs[0].font.bold = True
            r.cells[1].paragraphs[0].runs[0].font.bold = True
            r.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            r.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            r.cells[0].paragraphs[0].runs[0].font.size = Pt(9)
            r.cells[1].paragraphs[0].runs[0].font.size = Pt(9)
            if i % 2 == 1:
                set_cell_background(r.cells[0], "F9FBFD")
                set_cell_background(r.cells[1], "F9FBFD")

    doc.add_heading("5.3 Execution Sequence", level=2)
    doc.add_paragraph(
        "Execution begins by loading and cleaning data, computing probability benchmarks, fitting the model pipeline, displaying metric summaries, "
        "and launching real-time inference."
    )
    
    doc.add_page_break()
    
    # ------------------ CHAPTER 6 ------------------
    doc.add_heading("Chapter 6 – Model Evaluation and Results", level=1)
    doc.add_heading("6.1 Training and Test Set Summary", level=2)
    t_spl = doc.add_table(rows=4, cols=5)
    t_spl.alignment = WD_TABLE_ALIGNMENT.CENTER
    spl_data = [
        ("Partition", "Total Messages", "Ham (0)", "Spam (1)", "Proportion"),
        ("Training Set", "4,128", "3,614", "514", "80%"),
        ("Testing Set", "1,032", "904", "128", "20%"),
        ("Total Cleaned", "5,160", "4,518", "642", "100%")
    ]
    for i, row in enumerate(spl_data):
        for j, val in enumerate(row):
            cell = t_spl.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")

    doc.add_heading("6.2 Evaluation Metrics", level=2)
    doc.add_paragraph(
        "Standard classification metrics are defined as:\n"
        "• Accuracy = (TP + TN) / Total\n"
        "• Precision = TP / (TP + FP)\n"
        "• Recall = TP / (TP + FN)\n"
        "• F1-Score = 2 × Precision × Recall / (Precision + Recall)"
    )
    
    t_met = doc.add_table(rows=5, cols=3)
    t_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    met_data = [
        ("Metric", "Calculation from Test Set", "Result"),
        ("Accuracy", "(898 + 116) / 1,032", "98.26% (0.982558)"),
        ("Spam Precision", "116 / (116 + 6) = 116 / 122", "95.08% (0.950820)"),
        ("Spam Recall", "116 / (116 + 12) = 116 / 128", "90.63% (0.906250)"),
        ("Spam F1-Score", "Harmonic mean of Precision and Recall", "92.80% (0.928000)")
    ]
    for i, row in enumerate(met_data):
        for j, val in enumerate(row):
            cell = t_met.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")

    doc.add_heading("6.3 Confusion Matrix", level=2)
    # Confusion plot
    cm_path = os.path.join(plots_dir, "confusion_matrix.png")
    if os.path.exists(cm_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(cm_path, width=Inches(4.5))
        c_p = doc.add_paragraph("Figure 3: Confusion Matrix on 1,032 Held-out Test Messages")
        c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_p.runs[0].font.size = Pt(9)
        c_p.runs[0].font.italic = True
        
    doc.add_heading("6.4 Classification Report", level=2)
    t_cr = doc.add_table(rows=5, cols=5)
    t_cr.alignment = WD_TABLE_ALIGNMENT.CENTER
    cr_data = [
        ("Class", "Precision", "Recall", "F1-Score", "Support"),
        ("Ham (0)", "0.9868", "0.9934", "0.9901", "904"),
        ("Spam (1)", "0.9508", "0.9062", "0.9280", "128"),
        ("Macro Average", "0.9688", "0.9498", "0.9590", "1,032"),
        ("Weighted Average", "0.9823", "0.9826", "0.9824", "1,032")
    ]
    for i, row in enumerate(cr_data):
        for j, val in enumerate(row):
            cell = t_cr.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")

    doc.add_heading("6.5 In-Depth Error Analysis (FP vs FN)", level=2)
    doc.add_paragraph(
        "The model generated 6 False Positives (Ham classified as Spam) and 12 False Negatives (Spam classified as Ham):"
    )
    t_err = doc.add_table(rows=7, cols=3)
    t_err.alignment = WD_TABLE_ALIGNMENT.CENTER
    err_data = [
        ("Error Type", "Message Excerpt", "Root Cause Analysis"),
        ("False Negative", "Sorry I missed your call, let's talk when you have time...", "Chatty conversational vocabulary with absence of commercial keywords."),
        ("False Negative", "Thanks for your purchase of a video clip...", "Adult service promotion phrased as a polite receipt."),
        ("False Negative", "... free phone number in a couple of days ...", "Word 'free' appears in service context where surrounding tokens lean ham."),
        ("False Positive", "Nokia phone is lovly..", "Brand name 'Nokia' strongly associated with prize handset spam."),
        ("False Positive", "Unlimited texts. Limited minutes.", "Telecom keywords mimic commercial promotional SMS phrasing."),
        ("False Positive", "Have you laid your airtel line to rest?", "Account management vocabulary mirrors spam notifications.")
    ]
    for i, row in enumerate(err_data):
        for j, val in enumerate(row):
            cell = t_err.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")

    doc.add_page_break()
    
    # ------------------ CHAPTER 7 ------------------
    doc.add_heading("Chapter 7 – Real-Time SMS Testing", level=1)
    doc.add_heading("7.1 Required Test Message Demonstration", level=2)
    doc.add_paragraph(
        "The project specification requires testing the benchmark input message:\n"
        "  \"Congratulations! You have won a free prize. Claim now.\""
    )
    
    t_rt = doc.add_table(rows=4, cols=2)
    t_rt.alignment = WD_TABLE_ALIGNMENT.CENTER
    rt_data = [
        ("Output Field", "Model-Generated Value"),
        ("Predicted Class", "Spam (1)"),
        ("P(Spam | Message)", "0.999999802 (approximately 99.99998%)"),
        ("P(Ham | Message)", "0.000000198 (approximately 0.00002%)")
    ]
    for i, (k, v) in enumerate(rt_data):
        r = t_rt.rows[i]
        r.cells[0].text, r.cells[1].text = k, v
        if i == 0:
            set_cell_background(r.cells[0], "1F4E79")
            set_cell_background(r.cells[1], "1F4E79")
            r.cells[0].paragraphs[0].runs[0].font.bold = True
            r.cells[1].paragraphs[0].runs[0].font.bold = True
            r.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            r.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            r.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
            r.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)
            
    doc.add_paragraph(
        "\nNote on Formats: The values 0.96 and 0.04 in the curriculum activity sheet are illustrative guidelines. "
        "The actual mathematical output produced by fitting MultinomialNB on CountVectorizer word counts yields 0.999999802."
    )
    
    doc.add_heading("7.2 Interactive Testing Procedure", level=2)
    doc.add_paragraph(
        "To test additional arbitrary messages, invoke predict_sms(message, vectorizer, model). Crucially, the fitted training "
        "vocabulary must be reused (vectorizer.transform), ensuring consistent high-dimensional feature projection."
    )
    
    doc.add_page_break()
    
    # ------------------ CHAPTER 8 ------------------
    doc.add_heading("Chapter 8 – Results and Discussion", level=1)
    doc.add_heading("8.1 Summary of Main Findings", level=2)
    t_sum = doc.add_table(rows=8, cols=3)
    t_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    sum_data = [
        ("Analysis Component", "Result", "Meaning"),
        ("Prior Probabilities", "P(Spam)=0.1244, P(Ham)=0.8756", "Imbalanced class distribution favoring genuine messages."),
        ("Word: free", "P(Spam | free) = 0.7236", "72.36% of messages containing 'free' are spam."),
        ("Word: prize", "P(Spam | prize) = 1.0000", "100.0% of messages containing 'prize' are spam."),
        ("Expectation E(Y)", "0.1244", "Equals observed spam fraction for Bernoulli random variable."),
        ("Variance Var(Y)", "0.1089", "Population variance p(1-p)."),
        ("Model Accuracy", "98.26%", "1,014 of 1,032 test messages correctly classified."),
        ("Curriculum Example", "Spam (P = 0.999999802)", "Strongly and correctly classified as spam.")
    ]
    for i, row in enumerate(sum_data):
        for j, val in enumerate(row):
            cell = t_sum.rows[i].cells[j]
            cell.text = val
            if i == 0:
                set_cell_background(cell, "1F4E79")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if i % 2 == 1:
                    set_cell_background(cell, "F9FBFD")

    doc.add_heading("8.2 Linking Statistics to the Classifier", level=2)
    doc.add_paragraph(
        "Prior probabilities establish the baseline risk. Single-word conditional probabilities illustrate localized belief shifts. "
        "Multinomial Naive Bayes scales this exact Bayesian reasoning to all tokens simultaneously by compounding evidence under the "
        "conditional-independence assumption."
    )
    
    doc.add_heading("8.3 Strengths of the Probabilistic Approach", level=2)
    strengths = [
        "Rigorous interpretability: predictions trace back to observable token counts and prior ratios.",
        "Computational efficiency: training and inference are near-instantaneous over sparse matrices.",
        "High precision: minimizing false alarms to protect genuine communications."
    ]
    for st in strengths:
        doc.add_paragraph(f"• {st}")
        
    doc.add_heading("8.4 Limitations and Validity Considerations", level=2)
    limits = [
        "Static vocabulary: historical SMS patterns may not fully capture modern obfuscations or typos.",
        "Conditional independence assumption: ignores word ordering and syntactic context.",
        "Overconfident posteriors: raw Naive Bayes probabilities tend toward 0.0 or 1.0."
    ]
    for lm in limits:
        doc.add_paragraph(f"• {lm}")
        
    doc.add_page_break()
    
    # ------------------ CHAPTER 9 ------------------
    doc.add_heading("Chapter 9 – Conclusion and Future Scope", level=1)
    doc.add_heading("9.1 Conclusion", level=2)
    doc.add_paragraph(
        "This project successfully developed an end-to-end probabilistic SMS spam detection workflow. Beginning from dataset hygiene "
        "and empirical counting, through Bayes' theorem verification and Bernoulli random variable modeling, up to an optimized "
        "Multinomial Naive Bayes classifier (98.26% accuracy, 95.08% precision), the study demonstrates how fundamental mathematical "
        "theorems drive modern artificial intelligence systems."
    )
    
    doc.add_heading("9.2 Future Scope", level=2)
    futures = [
        "Incorporate character-level n-grams to robustly classify deliberate obfuscations (e.g., 'f-r-e-e', 'pr!ze').",
        "Implement k-fold cross-validation to assess variance across data partitions.",
        "Apply Platt scaling or isotonic regression to calibrate posterior probabilities.",
        "Explore lightweight recurrent or transformer networks for sequential context modeling."
    ]
    for ft in futures:
        doc.add_paragraph(f"• {ft}")
        
    doc.add_heading("References", level=1)
    refs = [
        "[1] Almeida, T., & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84",
        "[2] UCI Machine Learning Repository. (n.d.). SMS Spam Collection (Dataset ID 228). https://archive.ics.uci.edu/dataset/228/sms+spam+collection",
        "[3] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "[4] Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.",
        "[5] McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56.",
        "[6] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95."
    ]
    for rf in refs:
        doc.add_paragraph(rf)
        
    doc.add_page_break()
    
    # ------------------ APPENDICES ------------------
    doc.add_heading("Appendix A – Complete Python Source Code", level=1)
    doc.add_paragraph(
        "Below is the complete executable implementation, featuring dataset loading, preprocessing, probability analysis, "
        "Bayes verification, Bernoulli random variable calculation, Naive Bayes training, evaluation, and interactive inference:"
    )
    
    code_path = os.path.join(os.path.dirname(output_docx), "sms_spam_detector.py")
    if os.path.exists(code_path):
        with open(code_path, "r", encoding="utf-8") as cf:
            code_text = cf.read()
        p_c = doc.add_paragraph()
        r_c = p_c.add_run(code_text[:4000] + "\n... [Code continues in sms_spam_detector.py on GitHub] ...")
        r_c.font.name = "Consolas"
        r_c.font.size = Pt(8)
        
    doc.add_page_break()
    
    doc.add_heading("Appendix B – Verified Output Snapshot", level=1)
    t_sn = doc.add_table(rows=11, cols=2)
    t_sn.alignment = WD_TABLE_ALIGNMENT.CENTER
    sn_data = [
        ("Output Metric / Quantity", "Recorded Value"),
        ("Raw Dataset Shape", "(5,574, 2)"),
        ("Cleaned Dataset Rows", "5,160"),
        ("Cleaned Class Counts", "4,518 Ham / 642 Spam"),
        ("Prior Probabilities", "P(Ham) = 0.8755814 / P(Spam) = 0.1244186"),
        ("P(Spam | free)", "0.7236181"),
        ("E(Y) / Var(Y)", "0.1244186 / 0.1089386"),
        ("Train / Test Split", "4,128 / 1,032"),
        ("Vocabulary Size", "7,673 tokens"),
        ("Accuracy / Precision / Recall / F1", "98.26% / 95.08% / 90.63% / 92.80%"),
        ("Curriculum Example Output", "Spam; P(Spam) = 0.999999802")
    ]
    for i, (k, v) in enumerate(sn_data):
        r = t_sn.rows[i]
        r.cells[0].text, r.cells[1].text = k, v
        if i == 0:
            set_cell_background(r.cells[0], "1F4E79")
            set_cell_background(r.cells[1], "1F4E79")
            r.cells[0].paragraphs[0].runs[0].font.bold = True
            r.cells[1].paragraphs[0].runs[0].font.bold = True
            r.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            r.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            r.cells[0].paragraphs[0].runs[0].font.size = Pt(9)
            r.cells[1].paragraphs[0].runs[0].font.size = Pt(9)
            
    doc.add_page_break()
    
    doc.add_heading("Appendix C – Submission Checklist", level=1)
    chks = [
        "☑ Personalized student details: T. Harshith, 25BCE2863, B.TECH, CSE--CORE.",
        "☑ Comprehensive Table of Contents with section mapping.",
        "☑ Data cleaning policy explicitly documented (whitespace trimming and deduplication).",
        "☑ Bayes' theorem verified analytically and empirically for 'free'.",
        "☑ Bernoulli random variable expectation and variance derived and verified with NumPy.",
        "☑ Model evaluated with Accuracy, Precision, Recall, F1, Confusion Matrix, and Error Analysis.",
        "☑ Real-time test performed on required curriculum SMS input.",
        "☑ Source code and companion notebook pushed to GitHub: https://github.com/Harshith1987/BAMAT207-Probabilistic-SMS-Spam-Detection"
    ]
    for chk in chks:
        doc.add_paragraph(chk)
        
    doc.save(output_docx)
    print("Full academic report created successfully at:", output_docx)

if __name__ == "__main__":
    base = r"C:\Users\acs\.gemini\antigravity\scratch\sms_spam_detection"
    out = os.path.join(base, "BAMAT207_Probabilistic_SMS_Spam_Detection_Full_Academic_Report.docx")
    plots = os.path.join(base, "plots")
    build_full_report(out, plots)
