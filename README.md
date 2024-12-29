# RadGraph NER & Relation Extraction Project

This project focuses on developing a Named Entity Recognition (NER) and Relation Extraction pipeline using the RadGraph dataset.

---

## Setup Instructions

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/your-repo/radgraph-ner.git
   cd radgraph-ner
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the radgraph package in development mode:
   ```bash
   python setup.py develop
   ```

---

## Data Preprocessing

Ensure raw JSON files are placed in the `data/raw/` directory:

```plaintext
data/
├── raw/
│   ├── section_findings.json
│   └── section_impression.json
```

Then run the preprocessing script:
```bash
python scripts/preprocess.py
```

This script loads the raw JSON, creates a Hugging Face `Dataset` object, and saves it to `data/processed/`.

---

## Dataset: RadGraph-XL

Using **RadGraph-XL**, a large-scale expert-annotated dataset for entity and relation extraction in radiology reports. The dataset covers multiple anatomy-modality pairs (chest CT, abdomen/pelvis CT, brain MR, and chest X-rays) and includes over 410k entities/relations labeled by board-certified radiologists.

- **Download**: [Stanford Center for Artificial Intelligence in Medicine & Imaging (AIMI)](https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1)
- **Paper**: [RadGraph-XL: A Large-Scale Expert-Annotated Dataset for Entity and Relation Extraction from Radiology Reports (ACL 2024)](https://aclanthology.org/2024.findings-acl.765)

This dataset was introduced by Delbrouck et al., 2024 and has been shown to surpass previous approaches by up to 52% in extracting clinical entities and relations from radiology reports.

---

## Exploratory Data Analysis (EDA)

- See `notebooks/eda.ipynb` for details on entity distribution, report length analysis, and example highlights.

---

## Key Dataset Insights

### **Entity Type Distribution**
| **Entity Type**                             | **Count**     |
|---------------------------------------------|---------------|
| Observation::definitely present             | 2,440,911     |
| Anatomy::definitely present                 | 2,456,763     |
| Observation::definitely absent              | 396,044       |
| Observation::uncertain                      | 265,709       |
| Observation::measurement::definitely present| 6,393         |
| Anatomy::measurement::definitely present    | 14,307        |
| Anatomy::uncertain                          | 1,018         |
| Anatomy::definitely absent                  | 254           |
| Observation::measurement::uncertain         | 22            |
| Observation::measurement::definitely absent | 1             |

- **Handling Rare Classes**:
  - The rare class `Observation::measurement::definitely absent` (count: 1) was explicitly assigned to the test set to ensure inclusion in model evaluation.

### **Token Counts**
- **Total Tokens**: 15,815,652
- **Unique Tokens**: 33,855

---

## Train-Test Split Preparation

This step prepares train/val/test splits from the RadGraph dataset for model training. If stratification isn't feasible (e.g., due to rare entities), it falls back to a random split.

**Command**:
```bash
python scripts/train_test_split.py --input-file data/processed/radgraph.jsonl --output-dir data/splits --stratify
```

**Output**:
- `train.jsonl`: Training data
- `val.jsonl`: Validation data
- `test.jsonl`: Test data

---

## Tokenization Insights

A demonstration notebook [`notebooks/tokenization_demo.ipynb`](notebooks/tokenization_demo.ipynb) showcases:
- Differences between BPE, and WordPiece tokenization, vs general and domain tokenizers, illustrating the potential improvement in capturing medical terms within specialized vocabularies.
- Examples of tokenization applied to medical text in RADGRAPH.  For example, check out how ‘ACHALASIA’ is split across.
---

## Next Steps

1. Fine-tune pretrained models (e.g., Bio_ClinicalBERT, ClinicalBERT) on RadGraph for NER and relation extraction tasks.
2. Measure how tokenizer splits affect real NER metrics on the RadGraph dataset.
3. Consider exploring custom tokenization schemes for rare terms as a future experiment.

---

### **Style & Linting**

- **Recommended Tools**:
  - **Black**: Automatically formats your Python code to PEP 8 style.
  - **Flake8** / **Ruff**: Linting for code issues (unused imports, undefined vars).
  - **isort**: Sorts imports by sections (standard library, third-party, local).
  - **Pre-commit Hooks**: You can set up a `.pre-commit-config.yaml` to auto-run these on each commit.

**Initial Setup**:
```bash
pip install black flake8 isort
```

Run the tools:
```bash
black .
isort .
flake8 .
```