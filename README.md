# EconoCausal

## Dynamic Pricing via Double Machine Learning

EconoCausal is an advanced **Causal Machine Learning and Prescriptive AI** system designed to help businesses make better promotional and pricing decisions.

Traditional Machine Learning models are primarily designed to predict outcomes and correlations. However, prediction alone cannot answer an important business question:

> **"What would happen if we changed the treatment or intervention for this particular customer?"**

EconoCausal addresses this problem using **Double Machine Learning (DML)** and causal inference techniques to estimate the effect of different discounts on customer purchasing behavior.

The system goes beyond predicting who is likely to purchase. It estimates how a customer's probability of purchasing could change under different discount treatments and uses those causal estimates to optimize a limited marketing budget.

---

# 🎯 Problem Statement

Consider a company trying to reduce customer churn or increase purchases through discounts.

A conventional Machine Learning model might identify a customer with a high probability of churning and recommend a discount.

However, that customer might have stayed even without the discount.

Giving the discount in that situation wastes marketing budget.

Traditional predictive Machine Learning cannot directly answer:

```text
Would this customer have purchased
IF we gave them a discount?
```

EconoCausal addresses this problem by estimating **Individual Treatment Effects (ITE)** using causal Machine Learning.

---

# 💡 Project Idea

The system analyzes historical campaign data and estimates the causal impact of different discount levels.

For example:

```text
Customer
   │
   ├── No Discount
   │       ↓
   │   Purchase Probability
   │
   ├── $10 Discount
   │       ↓
   │   Purchase Probability
   │
   └── $20 Discount
           ↓
       Purchase Probability
```

The difference between these potential outcomes provides an estimate of the customer's treatment effect.

This allows the system to identify customers who are potentially **persuadable** — customers whose behavior is estimated to change because of the promotional treatment.

---

# 🚀 Main Objectives

The main objectives of EconoCausal are:

1. Move beyond correlation-based predictive Machine Learning.
2. Model causal relationships in customer campaign data.
3. Identify treatment, outcome, and confounding variables.
4. Construct a causal Directed Acyclic Graph (DAG).
5. Apply Propensity Score Matching to balance observational data.
6. Train Double Machine Learning models.
7. Estimate Individual Treatment Effects (ITE).
8. Compare the estimated effects of different discounts.
9. Optimize marketing budget allocation.
10. Provide an interactive dashboard for causal analysis.
11. Perform causal refutation tests.
12. Detect changes in underlying customer behavior through data-drift monitoring.

---

# 🧠 Core Concepts

## Treatment

The treatment represents the intervention applied to a customer.

Example:

```text
Discount Amount
```

Possible treatment levels may include:

```text
No Discount
$10 Discount
$20 Discount
```

---

## Outcome

The outcome represents the business result that we want to measure.

Example:

```text
Purchase
```

or

```text
Revenue
```

---

## Confounders

Confounders are variables that may influence both treatment assignment and the outcome.

Examples may include:

```text
Customer Age
Previous Purchases
Customer Tenure
Historical Spending
Engagement
Location
```

The project uses causal inference techniques to account for relevant confounding variables.

---

# 🔬 Causal Inference Engine

The central component of EconoCausal uses:

* **EconML**
* **DoWhy**
* Double Machine Learning
* Propensity Score Matching

The project specification specifically proposes using DoWhy for causal graphing and EconML for Double Machine Learning.

---

# 🔗 Causal DAG

A Directed Acyclic Graph (DAG) is used to represent assumed causal relationships.

A simplified example:

```text
Previous Purchases ──────┐
                         ▼
Customer Characteristics → Discount → Purchase
                         │
                         └──────────→ Purchase
```

The DAG helps identify:

* Treatment
* Outcome
* Confounders
* Adjustment variables
* Causal assumptions

---

# ⚖️ Propensity Score Matching

Historical campaign data is observational rather than necessarily coming from a randomized experiment.

Propensity Score Matching helps create more comparable treatment and control groups based on observed customer characteristics.

The general process is:

```text
Historical Customer Data
          │
          ▼
Estimate Propensity Scores
          │
          ▼
Match Similar Customers
          │
          ▼
Balanced Treatment / Control Groups
          │
          ▼
Causal Effect Estimation
```

This approach is intended to reduce imbalance caused by observed confounding variables.

---

# 🤖 Double Machine Learning

The project uses **Double / Debiased Machine Learning** to estimate treatment effects while using Machine Learning models for nuisance functions.

Potential base estimators include:

* Random Forest
* LightGBM

The project specification proposes these models as base estimators for the DML pipeline.

A simplified conceptual workflow is:

```text
Customer Features
       │
       ├───────────────┐
       ▼               ▼
Treatment Model    Outcome Model
       │               │
       └───────┬───────┘
               ▼
       Double Machine
          Learning
               │
               ▼
       Treatment Effect
               │
               ▼
             ITE
```

---

# 📈 Individual Treatment Effect

The Individual Treatment Effect represents the estimated difference between a customer's potential outcome under treatment and under an alternative treatment.

Conceptually:

```text
ITE = Y(1) - Y(0)
```

For different discount levels, the system can estimate treatment effects such as:

```text
Effect of $10 Discount
Effect of $20 Discount
```

This allows the dashboard to focus on **incremental impact**, rather than simply predicting purchase probability.

---

# 🎯 Customer Segmentation Based on Causal Effect

The system can use estimated treatment effects to distinguish different customer responses.

Conceptually:

```text
                 Treatment Effect
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
     Persuadable    Unaffected    Negative/
                                  Low Response
```

A key target described in the project specification is the **Persuadable** group: customers whose estimated behavior changes because of the promotional treatment.

---

# 💰 Prescriptive Optimization

After estimating treatment effects, EconoCausal moves from causal analysis to **prescriptive decision-making**.

The optimization component uses **SciPy** to allocate a fixed marketing budget.

Example:

```text
Available Budget = $5,000

Customer A → $10 Discount
Customer B → $20 Discount
Customer C → No Discount
Customer D → $10 Discount
...
```

The optimizer attempts to determine an allocation that maximizes the selected business objective while respecting the available budget.

The project specification explicitly defines this component as an optimization solver that takes causal predictions and a fixed budget and assigns personalized discounts.

---

# 📊 Uplift Analysis

The dashboard visualizes causal uplift using:

* Uplift curves
* Qini curves
* Treatment-effect distributions
* Budget allocation analysis

The Qini and uplift analysis is intended to help evaluate whether causal targeting provides useful incremental impact compared with a random rollout.

---

# 🖥️ Dashboard

EconoCausal includes a web-based dashboard built around:

* React
* Plotly

The dashboard provides an interface for:

### Data Upload

Users can upload historical campaign data.

### Budget Configuration

Users can specify the available marketing budget.

### Causal Analysis

The dashboard displays treatment-effect estimates.

### Uplift Visualization

Interactive Qini and uplift curves provide visual analysis of the causal model.

### Prescription Table

The system presents the recommended allocation generated by the optimization engine.

Conceptually:

```text
┌───────────────────────────────────────────────┐
│                 EconoCausal                   │
├───────────────────────────────────────────────┤
│ Upload Data       │ Budget: $5,000             │
├───────────────────┼───────────────────────────┤
│                   │                            │
│ Causal Analysis   │ Uplift / Qini Curve        │
│                   │                            │
├───────────────────┴───────────────────────────┤
│              Discount Prescription            │
├──────────┬──────────────┬─────────────────────┤
│ Customer │ Treatment    │ Estimated Effect    │
├──────────┼──────────────┼─────────────────────┤
│ C001     │ $10          │ ...                 │
│ C002     │ $20          │ ...                 │
│ C003     │ No Discount  │ ...                 │
└──────────┴──────────────┴─────────────────────┘
```

---

# 🔍 Causal Refutation

A major component of EconoCausal is causal validation.

The project specification calls for **DoWhy Refutation Tests** to audit whether the estimated causal effect remains reliable under alternative checks.

The purpose is to investigate whether the estimated causal relationship is sensitive to potential issues in the analysis.

Possible checks include:

* Random common cause
* Placebo treatment
* Data subset validation
* Other appropriate refutation strategies

The results should be interpreted together with the assumptions and limitations of the observational dataset.

---

# 📉 Data Drift Detection

Customer behavior can change over time.

For example:

```text
Historical Customer Behavior
            ↓
       Model Training
            ↓
       New Customer Data
            ↓
      Drift Detection
            ↓
       ┌────┴────┐
       │         │
     Stable    Drift
                 │
                 ▼
              Warning
```

The project specification includes an automated data-drift detector that warns when the underlying customer behavior changes.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │ Historical Campaign  │
                    │        Data          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Preprocessing    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Causal DAG / DoWhy   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Propensity Matching  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Double ML / EconML   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Individual Treatment │
                    │       Effects        │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌─────────────────┐    ┌──────────────────┐
          │ Uplift / Qini   │    │ SciPy Optimizer  │
          │    Analysis     │    │                  │
          └────────┬────────┘    └────────┬─────────┘
                   │                      │
                   └──────────┬───────────┘
                              ▼
                    ┌──────────────────────┐
                    │ REST API             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ React + Plotly       │
                    │     Dashboard        │
                    └──────────────────────┘
```

---

# 📅 Development Plan

The original project specification divides development into four weeks.

## Week 1 — Causal Graphing & Dashboard

### Causal ML

* Prepare mock retail dataset.
* Identify treatment variables.
* Identify outcome variables.
* Identify confounders.
* Build causal DAG using DoWhy.

### Frontend

* Initialize React application.
* Create data-upload interface.
* Create budget configuration interface.

---

## Week 2 — Double Machine Learning

### Causal ML

* Train EconML DML models.
* Use Random Forest or LightGBM as base estimators.
* Estimate Individual Treatment Effects.

### Visualization

* Integrate Plotly.
* Build uplift curves.
* Build Qini curves.
* Compare causal targeting with random rollout.

---

## Mid-Project Review

### Causal Audit

Perform DoWhy refutation tests to investigate the robustness of the estimated causal effects.

### Data Load Validation

Ensure that the dashboard can dynamically filter and visualize thousands of customer ITE scores.

---

## Week 3 — Prescriptive Optimization

### Backend

* Develop SciPy optimization pipeline.
* Define marketing budget constraint.
* Allocate personalized discounts.
* Maximize the selected revenue/business objective.

### Frontend

Create a prescription table containing:

* Customer
* Treatment
* Discount amount
* Estimated treatment effect
* Relevant business metrics

---

## Week 4 — API & Packaging

### Backend

* Wrap the causal engine in a REST API.
* Add automated data-drift detection.
* Generate warnings when customer behavior changes.

### Frontend

* Improve dashboard design.
* Add natural-language summaries.
* Present budget allocation results.
* Display efficiency comparisons.

---

# 📁 Project Structure

```text
EconoCausal/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   │
│   ├── causal/
│   │   ├── dag.py
│   │   ├── propensity.py
│   │   ├── dml.py
│   │   ├── treatment_effect.py
│   │   └── refutation.py
│   │
│   ├── optimization/
│   │   └── budget_optimizer.py
│   │
│   ├── preprocessing/
│   │   └── preprocess.py
│   │
│   ├── drift/
│   │   └── detector.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── charts/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── reports/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_causal_graph.ipynb
│   ├── 03_dml_model.ipynb
│   └── 04_optimization.ipynb
│
├── tests/
│
├── README.md
└── .gitignore
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Pandas
* NumPy
* SciPy

## Causal Machine Learning

* EconML
* DoWhy
* Scikit-learn

## Machine Learning

* Random Forest
* LightGBM

## Optimization

* SciPy Optimization

## Frontend

* React
* Plotly.js

## Development

* Git
* GitHub
* VS Code
* Jupyter Notebook

---

# 🚀 Installation

## Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd EconoCausal
```

---

## Backend Setup

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

---

## Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# ▶️ Running the Application

## Start Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

The API will run locally.

---

## Start Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Open the displayed local development URL in your browser.

---

# 🔄 End-to-End Workflow

```text
Upload Historical Campaign Data
             ↓
       Data Preprocessing
             ↓
       Define Causal DAG
             ↓
      Identify Confounders
             ↓
    Propensity Score Matching
             ↓
     Double ML Estimation
             ↓
      Estimate Customer ITE
             ↓
       Uplift Analysis
             ↓
     Budget Optimization
             ↓
 Personalized Prescription
             ↓
       Dashboard Results
             ↓
       Drift Monitoring
```

---

# 📊 Expected Outputs

EconoCausal is designed to produce:

* Causal DAG
* Propensity scores
* Balanced treatment/control groups
* Individual Treatment Effects
* Average treatment effects where appropriate
* Uplift curves
* Qini curves
* Customer-level treatment estimates
* Personalized discount allocations
* Budget utilization analysis
* Causal refutation results
* Data-drift warnings

---

# 💼 Business Use Case

A marketing director has a fixed promotional budget.

For example:

```text
Marketing Budget = $5,000
```

Instead of giving every customer the same discount, EconoCausal analyzes estimated causal effects and determines how the available budget can be allocated across customers.

The system can distinguish between:

```text
Customer likely to purchase anyway
              ↓
        No additional incentive

Customer influenced by discount
              ↓
        Potentially persuadable

Customer with limited response
              ↓
        Lower expected incremental impact
```

This changes the decision-making process from:

```text
"Who is likely to buy?"
```

to:

```text
"Who is likely to change their behavior
because of the intervention?"
```

---

# ⚠️ Limitations

Causal Machine Learning does not automatically prove causality.

The quality of causal estimates depends on:

* Data quality
* Treatment definition
* Outcome definition
* Confounder measurement
* Causal assumptions
* Propensity score overlap
* Model specification
* Sample size
* Distribution shifts

Observational data may contain unmeasured confounding variables that cannot be completely addressed using the available data.

Therefore, causal estimates should be interpreted together with their assumptions, diagnostics, and refutation results.

---

# 🔮 Future Scope

Possible future improvements include:

* Continuous treatment modeling for flexible discount amounts
* Advanced heterogeneous treatment-effect models
* Causal Forests
* Double Machine Learning extensions
* Multi-treatment causal inference
* Time-varying treatment effects
* Online experimentation integration
* Automated causal graph discovery
* Advanced drift monitoring
* Real-time campaign optimization
* Cloud deployment
* Role-based enterprise dashboard
* Advanced revenue optimization

---

# 🌟 Why EconoCausal?

EconoCausal demonstrates the transition:

```text
Traditional Analytics
        ↓
Predictive Machine Learning
        ↓
Causal Machine Learning
        ↓
Prescriptive AI
```

Instead of stopping at prediction, the project attempts to estimate the impact of interventions and use those estimates to support constrained business decisions.

The project specification describes this as moving beyond predictive AI toward **Causal and Prescriptive AI**.

---

# 📌 Project Information

| Category         | Details                                    |
| ---------------- | ------------------------------------------ |
| Project          | EconoCausal                                |
| Domain           | Economics & Causal AI                      |
| Focus            | Dynamic Pricing / Promotional Optimization |
| Core Method      | Double Machine Learning                    |
| Causal Framework | EconML + DoWhy                             |
| Optimization     | SciPy                                      |
| Visualization    | React + Plotly                             |
| Backend          | Python REST API                            |
| Frontend         | React                                      |
| Status           | In Development                             |

---

# 👩‍💻 Author

**Anisha N**


---

# 📄 License

This project is developed for educational, research, portfolio, and demonstration purposes.

---

## ⭐ Project Goal

**EconoCausal aims to demonstrate how causal inference and machine learning can be combined to estimate intervention effects and transform those estimates into data-driven, budget-constrained business decisions.**
