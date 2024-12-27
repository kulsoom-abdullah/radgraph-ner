# RadGraph NER & Relation Extraction Project

This project focuses on developing a Named Entity Recognition (NER) and Relation Extraction pipeline using the RadGraph dataset.

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

## Data Preprocessing
Ensure raw JSON files are placed in the data/raw/ directory:

```kotlin
data/
├── raw/
│   ├── section_findings.json
│   └── section_impression.json
```

Then run the preprocessing script:

```bash
python scripts/preprocess.py
```
This script loads the raw JSON, creates a Hugging Face `Dataset` object, and saves it to `data/processed/`

## Dataset: RadGraph-XL

Using **RadGraph-XL**, a large-scale expert-annotated dataset for entity and relation extraction in radiology reports. The dataset covers multiple anatomy-modality pairs (chest CT, abdomen/pelvis CT, brain MR, and chest X-rays) and includes over 410k entities/relations labeled by board-certified radiologists.

- **Download**: [Stanford Center for Artificial Intelligence in Medicine & Imaging (AIMI)](https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1)
- **Paper**: [RadGraph-XL: A Large-Scale Expert-Annotated Dataset for Entity and Relation Extraction from Radiology Reports (ACL 2024)](https://aclanthology.org/2024.findings-acl.765)

This dataset was introduced by Delbrouck et al., 2024 and has been shown to surpass previous approaches by up to 52% in extracting clinical entities and relations from radiology reports.

## Exploratory Data Analysis (EDA)
-See `notebooks/eda.ipynb` for details on entity distribution, report length analysis, and example highlights.

## Key Dataset Insights
1. **Entity Type Distribution**:
   - Most common entity types:
     - `Observation::definitely present`: ~2.4M occurrences.
     - `Anatomy::definitely present`: ~2.45M occurrences.
   - Rare entity types include:
     - `Observation::measurement::definitely absent`: 1 occurrence.
     - `Observation::measurement::uncertain`: 22 occurrences.

2. **Report Length Distribution**:
   - Average report length: ~56 tokens (based on whitespace-separated words).
   - Most reports are between 30–100 tokens, with a few outliers >300 tokens.

3. **Entity Trends by Report Length**:
   - Longer reports are more likely to include rare entity types like `Observation::measurement::definitely present`.

4. **Highlighted Examples**:
   - Entities in reports are well-structured, covering a range of observations and anatomical terms.

---


### **Suggestions for Next Steps**
- **Tokenization**: Implement and analyze different tokenization schemes (e.g., BPE, WordPiece).
- **Training**: Prepare datasets for fine-tuning the NER model.
- **Testing**: Develop tests to validate preprocessing and tokenization logic.


---

###  **Style & Linting**

- **Recommended Tools**:
  - **Black**: Automatically formats your Python code to PEP 8 style.
  - **Flake8** / **Ruff**: Linting for code issues (unused imports, undefined vars).
  - **isort**: Sorts imports by sections (standard library, third-party, local).
  - **Pre-commit Hooks**: You can set up a `.pre-commit-config.yaml` to auto-run these on each commit.

**Initial Setup** (minimal approach):
```bash
pip install black flake8 isort
```
# Then you can run
```bash
black .
isort .
flake8 .
```