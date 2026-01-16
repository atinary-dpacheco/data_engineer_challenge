# Technical Challenge: The Scientific Data Bridge

## 1. Introduction & Context
Atinary Technologies is building the "Data Backbone" for the future of chemistry R&D. We operate an automated laboratory that generates high-fidelity experimental data, which we harmonize with global datasets like the **Open Reaction Database (ORD)**.

Your mission is to process a "raw" binary dataset and transform it into a standardized format. This task simulates the real-world challenge of integrating diverse scientific sources where the same concepts are recorded with different structures and styles.

## 2. The Dataset
You are provided with a binary Protobuf file (`ord_challenge_subset.pb.gz`) containing a mixture of Buchwald-Hartwig reactions from two distinct sources. You can explore these datasets on the ORD website:

*   **AstraZeneca ELN:** [Dataset ord-00005539...](https://research.open-reaction-database.org/dataset/ord-00005539a1e04c809a9a78647bea649c)
*   **Merck/Chemistry Informer HTE:** [Dataset ord-026684...](https://research.open-reaction-database.org/dataset/ord-026684a62f91469db49c7767d16c39fb)

## 3. The Task: Semantic Extraction & Harmonization
Your goal is to flatten this hierarchical Protobuf data into a single **CSV file**. You may use any tools or libraries (e.g., RDKit, Pandas, etc.) to achieve this.

### Part A: The Extraction Challenge
A Buchwald-Hartwig reaction involves the coupling of two primary molecules. You must implement the methodology to identify and extract them from the generic `inputs` list in the ORD schema:

1.  **Aryl Halide:** Typically a molecule that contains a **halogen atom** (Chlorine, Bromine, or Iodine) attached to an **aromatic ring** (a benzene-like structure). 
2.  **Amine:** Typically a molecule containing at least one **Nitrogen atom**.

**Note on Ambiguity:** In some cases, a single molecule might contain both a halogen and a nitrogen atom. Your logic must decide how to assign these roles when multiple candidates exist for a single reaction.

### Part B: Key Information Requirements
Your final CSV should capture the following core information for each reaction:
*   **Reaction ID**
*   **Aryl Halide:** SMILES string and Amount (mass/volume/moles).
*   **Amine:** SMILES string and Amount (mass/volume/moles).
*   **Catalyst:** SMILES string (labeled in metadata) and Amount.
*   **Desired Product:** SMILES string (labeled with the `is_desired_product` flag).
*   **Yield Percentage:** Resolve the yield regardless of whether it was recorded as a "UPLC Analysis" (Merck) or a "Product Measurement" (AstraZeneca).
*   **Reaction Conditions:** Include the Temperature and the Reaction Time.

### Part C: Systems Design (Conceptual)
*   **Database Architecture:** Propose a long-term database schema for this data using **DBML** (Database Markup Language).
*   **Unstructured Data:** Researchers record a free-text **Procedure Description** (step-by-step instructions) and **Analysis Notes**. For future AI/LLM training, how would you architect the storage of this unstructured text so it remains linked to the quantitative results while remaining efficiently searchable?

---

## 4. Required Deliverables
Please provide a folder containing:

1.  **`extraction_script.py`**: Your Python code used to parse the `.pb.gz` file and execute your extraction logic.
2.  **`processed_data.csv`**: Your final standardized dataset containing the key information requested above.
3.  **`schema.dbml`**: Your proposed database structure.
4.  **`DESIGN.md`**: A short document (max 1 page) addressing:
    *   **Extraction Methodology:** How did you programmatically identify the Aryl Halide and the Amine? 
    *   **Data Representation:** How did you choose to represent amounts and conditions in the CSV? Why is your chosen format suitable for Machine Learning?
    *   **Search Logic:** How would you query for "Reactions > 80°C" if units are mixed (Kelvin vs. Celsius)?
    *   **Unstructured Data:** Your proposal for storing Procedure and Analysis text.

---

## 5. Evaluation Criteria
*   **Analytical Reasoning:** How you translated high-level descriptions into a robust programmatic search for chemical components.
*   **Data Integrity:** Successful capture of yield values and amounts across inconsistent datasets.
*   **Systems Thinking:** A DBML schema that shows a clear understanding of how to structure scientific entities for both ML and data-licensing purposes.
*   **Pragmatism:** Your ability to handle "real-world" messy data (missing units, ambiguous roles) and your rationale for the final CSV structure.

***

### Evaluation Guide for the Hiring Manager:

1.  **The "Amount" Representation:** Since you didn't force them to separate values and units, check how they did it.
    *   *The "String" Path:* They put `"10 mg"` in a column. (Fine for a quick script, but bad for ML).
    *   *The "ML" Path:* They separated them into `amount_value` and `amount_unit` or normalized everything to a standard unit. This shows they are thinking about the end-user (the ML model).
2.  **The Chemical Logic:** Look at how they identified the Aryl Halide vs. Amine. Did they use a specialized library like RDKit, or did they write a clever string heuristic? How did they handle molecules that could be both?
3.  **The Yield Resolution:** Verify they found the yield in both the Merck (Analyses) and AstraZeneca (Products) blocks.
4.  **The Procedure Storage:** Does their proposal for unstructured text suggest they understand that large blocks of text don't belong in a standard relational table? (Look for mentions of Blob storage, JSONB, or Vector DBs).