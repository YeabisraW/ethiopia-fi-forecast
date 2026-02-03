# 📔 Data Enrichment Log: Ethiopia FI Forecast

| Source | Collection Date | original_text / Event | Pillar | Confidence | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [NBE 2021-25 Strategy](https://nbe.gov.et) | 2026-02-03 | Refreshed NFIS-II Targets | Policy | High | Established the 70% inclusion baseline target. |
| [World Bank Findex](https://worldbank.org) | 2026-02-03 | 2021 Survey Microdata | Access | High | Used to anchor LSTM baseline training. |
| [Ethio Telecom / Telebirr](https://ethiotel.et) | 2026-02-03 | 40M+ Registered Users | Usage | Medium | Highlights the 'Registration vs. Usage' gap. |

**Rationale for Additions:**
* **Correct Pillar Handling:** Events are mapped to *Access* (physical/digital), *Usage* (activity), or *Policy* (regulations).
* **Source Tracking:** Each data point is linked to its primary source to ensure research reproducibility.