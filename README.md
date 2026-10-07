<p align="center">
  <img src="./neural-banner.gif" alt="Naveen Varma — Turning complexity into intelligence. A rotating 3D neural field and an animated Data → Model → Evaluate → Deploy pipeline." width="1120">
</p>

<p align="center">
  <a href="./neural-banner.png">View a still version of the banner</a>
</p>

<h1 align="center">Hi, I'm Naveen Varma.</h1>

<p align="center">
  <a href="https://github.com/naveenvarma999">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=2800&pause=900&color=B5F5D2&center=true&vCenter=true&width=640&lines=ML+Engineer+who+ships+models+to+production;Two-tower+recommenders+%C2%B7+fraud+detection+%C2%B7+vision;MLflow+%C2%B7+Docker+%C2%B7+FastAPI+%C2%B7+AWS;Open+to+ML+Engineer+and+MLOps+roles+in+the+UK" alt="ML Engineer who ships models to production. Open to ML Engineer and MLOps roles in the UK.">
  </a>
</p>

<p align="center">
  <strong>Machine Learning Engineering · Data Science · MLOps</strong><br>
  MSc Applied Data Science · University of Essex<br>
  Exploring the complete journey from raw data to useful ML systems.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/naveenvarma000/"><img src="https://img.shields.io/badge/LinkedIn-Connect-101B20?style=for-the-badge&amp;logo=linkedin&amp;logoColor=B5F5D2" alt="Connect on LinkedIn"></a>
  <a href="mailto:naveennallapu750@gmail.com"><img src="https://img.shields.io/badge/Email-Let%27s_talk-101B20?style=for-the-badge&amp;logo=gmail&amp;logoColor=B5F5D2" alt="Email Naveen"></a>
  <a href="https://leetcode.com/u/naveenvarma999/"><img src="https://img.shields.io/badge/LeetCode-Problem_solving-101B20?style=for-the-badge&amp;logo=leetcode&amp;logoColor=B5F5D2" alt="LeetCode profile"></a>
  <a href="https://threadline-naveen.duckdns.org"><img src="https://img.shields.io/badge/Live_demo-Threadline-B5F5D2?style=for-the-badge&amp;logo=amazonaws&amp;logoColor=101B20" alt="Threadline live demo"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Open_to_work-B5F5D2?style=flat-square&amp;labelColor=101B20" alt="Status: open to work">
  <img src="https://img.shields.io/badge/Based_in-Colchester,_UK-B5F5D2?style=flat-square&amp;labelColor=101B20" alt="Based in Colchester, UK">
  <img src="https://img.shields.io/badge/Focus-ML_Engineering_%C2%B7_MLOps-B5F5D2?style=flat-square&amp;labelColor=101B20" alt="Focus: ML Engineering and MLOps">
</p>

<p align="center">
  <a href="#about-me">About</a> &nbsp; / &nbsp;
  <a href="#featured-work">Work</a> &nbsp; / &nbsp;
  <a href="#experience">Experience</a> &nbsp; / &nbsp;
  <a href="#toolkit">Toolkit</a> &nbsp; / &nbsp;
  <a href="#github-observatory">Analytics</a> &nbsp; / &nbsp;
  <a href="#lets-connect">Contact</a>
</p>

---

## About me

[![Naveen Varma — ML engineer and Python developer. MSc Applied Data Science, University of Essex. Python, SQL, FastAPI, Django, Docker, Git and MLflow.](./cinematic-depth.gif)](mailto:naveennallapu750@gmail.com)

[Introduction](./chapter-1.png) · [Skills](./chapter-2.png) · [Approach](./chapter-3.png) · [LinkedIn](https://www.linkedin.com/in/naveenvarma000/)

```python
class Naveen:
    role      = "ML Engineer · MLOps"
    education = "MSc Applied Data Science, University of Essex"
    focus     = ["recommender systems", "fraud detection", "computer vision", "LLM serving"]
    ships_with = ["PyTorch", "scikit-learn", "MLflow", "FastAPI", "Docker", "AWS"]

    def approach(self):
        return "leakage-free validation → honest metrics → tested, monitored deployment"
```

## Featured work

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/naveenvarma999/threadline"><img src="./assets/card-threadline.svg" alt="Threadline: two-stage fashion recommender. 2.5x MAP@12 over a popularity baseline, 76 ms p50 latency, 6 Docker services on AWS." width="100%"></a>
      <p align="center"><a href="https://threadline-naveen.duckdns.org"><b>Live demo</b></a> · <a href="https://github.com/naveenvarma999/threadline">Code</a></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/naveenvarma999/fraudguard"><img src="./assets/card-fraudguard.svg" alt="FraudGuard: behavioural fraud detection. 0.550 average precision on unseen accounts, Brier score cut by 70%, 128 automated tests." width="100%"></a>
      <p align="center"><a href="https://github.com/naveenvarma999/fraudguard"><b>Code</b></a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="./assets/card-pneumonia.svg" alt="Pneumonia AI: MSc dissertation. ResNet50 with test-time augmentation, ROC-AUC 0.962, sensitivity 0.954, accuracy 0.888." width="100%">
      <p align="center"><sub>MSc dissertation · University of Essex</sub></p>
    </td>
    <td width="50%" valign="top">
      <img src="./assets/card-infergate.svg" alt="InferGate: LLM inference gateway with semantic cache, rate limiting, streaming and an eval gate in CI. In progress." width="100%">
      <p align="center"><sub>In progress</sub></p>
    </td>
  </tr>
</table>

<details>
<summary><b>How Threadline works</b> (click to expand)</summary>

```mermaid
flowchart LR
    U[React storefront] --> D[Django REST API + PostgreSQL]
    D --> F[FastAPI inference service<br/>p50 76 ms · cache + fallback]
    F --> R[Two-tower retrieval<br/>PyTorch + FAISS]
    R --> K[Gradient-boosting ranker<br/>38 point-in-time features]
    M[(MLflow Model Registry)] -. versions & promotes .-> F
    CI[GitHub Actions · 33 tests] -. deploys .-> AWS[AWS EC2 · 6 Docker services · HTTPS]
```

- **2.5× MAP@12** over a popularity baseline (0.128 vs 0.052), trained on 277K transactions
- Leakage-free, time-based validation; an ablation showed deep-learning features added under 1%
- Angular dashboard for model monitoring

</details>

<details>
<summary><b>How FraudGuard ships models safely</b> (click to expand)</summary>

```mermaid
flowchart LR
    T[Transactions] --> I[Duplicate-safe ingestion]
    I --> S[Production model scores]
    I --> C[Candidate model<br/>shadow scoring]
    L[Analyst labels] --> RT[Label-based retraining] --> C
    C --> G{Promotion gate<br/>unseen-account AP}
    G -- better --> A[Admin approval] --> S
    G -- worse --> K[Keep production model]
```

- **0.550 AP on unseen accounts** (95% bootstrap CI 0.426–0.653) across 523K transactions and 1,197 accounts
- Brier score cut **70%** through calibration; rollback in one step
- AWS EC2 with HTTPS, MFA and rate limiting · **128 automated tests**

</details>

## Experience

| Role | Where | When |
|---|---|---|
| **Data Scientist Intern** | AI Variant · Hyderabad, India | Jun – Dec 2024 |
| **MSc Applied Data Science** | University of Essex · Colchester, UK | Sep 2025 – present |

At AI Variant I worked across the full model lifecycle: data pipelines and feature engineering in Python and SQL, model training and tuning with experiments tracked in MLflow, and a Dockerised FastAPI service for predictions.

## Toolkit

### Languages & data

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" alt="Python" height="28">
  <img src="https://img.shields.io/badge/SQL-336791?style=for-the-badge" alt="SQL" height="28">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&amp;logo=postgresql&amp;logoColor=white" alt="PostgreSQL" height="28">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&amp;logo=pandas&amp;logoColor=white" alt="Pandas" height="28">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&amp;logo=numpy&amp;logoColor=white" alt="NumPy" height="28">
</p>

### Machine learning

<p>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&amp;logo=pytorch&amp;logoColor=white" alt="PyTorch" height="28">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&amp;logo=scikitlearn&amp;logoColor=white" alt="scikit-learn" height="28">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&amp;logo=tensorflow&amp;logoColor=white" alt="TensorFlow" height="28">
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&amp;logo=keras&amp;logoColor=white" alt="Keras" height="28">
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&amp;logo=meta&amp;logoColor=white" alt="FAISS" height="28">
</p>

### Applications & serving

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&amp;logo=fastapi&amp;logoColor=white" alt="FastAPI" height="28">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&amp;logo=django&amp;logoColor=white" alt="Django" height="28">
  <img src="https://img.shields.io/badge/Flask-232F3E?style=for-the-badge&amp;logo=flask&amp;logoColor=white" alt="Flask" height="28">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&amp;logo=react&amp;logoColor=61DAFB" alt="React" height="28">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&amp;logo=streamlit&amp;logoColor=white" alt="Streamlit" height="28">
</p>

### Engineering & MLOps

<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&amp;logo=docker&amp;logoColor=white" alt="Docker" height="28">
  <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&amp;logo=amazonaws&amp;logoColor=white" alt="AWS EC2" height="28">
  <img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&amp;logo=mlflow&amp;logoColor=white" alt="MLflow" height="28">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&amp;logo=githubactions&amp;logoColor=white" alt="GitHub Actions" height="28">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&amp;logo=git&amp;logoColor=white" alt="Git" height="28">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&amp;logo=linux&amp;logoColor=black" alt="Linux" height="28">
</p>

### Analysis & visualization

<p>
  <img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge" alt="Tableau" height="28">
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge" alt="Matplotlib" height="28">
</p>

### Certifications

| Certificate | Issuer | Year | |
|---|---|---|---|
| **SQL (Advanced)** | HackerRank | 2025 | [Verify ↗](https://www.hackerrank.com/certificates/e40a41d63714) |
| **Machine Learning A-Z** | Udemy | 2025 | [Verify ↗](https://ude.my/UC-229fbddb-ee70-42c9-87e0-dee06780397b) |
| **Deep Learning A-Z** | Udemy | 2024 | [Verify ↗](https://ude.my/UC-3bbf72ed-39f4-49fc-9897-5d8291ac87c6) |

## GitHub Observatory

<p align="center">
  <a href="https://naveenvarma999.github.io/naveenvarma999/">
    <img src="./analytics/dashboard-overview.png" alt="GitHub analytics dashboard: contribution totals, active days, longest streak, repository count, activity trends, language mix, calendar heatmap and weekday totals." width="1120">
  </a>
</p>

<p align="center">
  <a href="https://naveenvarma999.github.io/naveenvarma999/"><strong>Explore the interactive dashboard →</strong></a><br>
  <sub>Date filters · 3D rotation · Daily detail · CSV export</sub>
</p>

<!-- The interactive link becomes available after enabling GitHub Pages and running the included workflow. See START-HERE.md. -->

### Contributions in motion

<p align="center">
  <img src="./analytics/contributions-3d.gif" alt="Animated 3D contribution calendar with heights representing real daily activity and a decorative moving highlight." width="1120">
</p>

<p align="center">
  <a href="./analytics/contributions-3d.png">Still version</a> ·
  <a href="./analytics/activity.json">Contribution data</a>
</p>

<sub>Public GitHub activity; snapshot dates are shown on the charts. The included workflow refreshes the figures daily after installation. Repository and language totals describe the account snapshot. Contributions are activity indicators, not a measure of skill or code quality.</sub>

## Currently

- 🔨 **Building** InferGate, an LLM inference gateway with semantic caching and an eval gate in CI
- 🎓 **Finishing** my MSc dissertation on paediatric pneumonia detection
- 🎯 **Looking for** ML Engineer and MLOps / Platform Engineer roles in the UK

## Let's connect

I'm interested in **ML Engineer roles** and conversations about applied ML, model evaluation and reliable delivery.

**[LinkedIn](https://www.linkedin.com/in/naveenvarma000/) · [Email](mailto:naveennallapu750@gmail.com) · [LeetCode](https://leetcode.com/u/naveenvarma999/)**

<p align="center">
  <sub>Curiosity drives the experiment. Evidence earns the conclusion.</sub>
</p>
