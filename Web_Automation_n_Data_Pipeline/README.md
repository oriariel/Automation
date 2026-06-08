# SentinelScrape: Production-Grade Web Automation & Data Pipeline

A highly modular, professional web scraping and automation engine built in Python using Selenium. This project demonstrates enterprise software development patterns, specifically leveraging the **Page Object Model (POM)** to decouple UI layout logic from data retrieval and storage operations.

To tackle modern web scraping hurdles, the pipeline implements an anti-detection layer capable of gracefully navigating dynamic DOM interfaces, normalizing unstructured payloads, and writing them safely into an optimized database layer.

---

## 🚀 Core Features

- **Anti-Bot Mitigation:** Integrates specialized browser binaries via `undetected_chromedriver` to safely bypass modern defensive infrastructure (e.g., Cloudflare, Akamai Interstitials).
- **Page Object Model (POM):** Architected with clean separation of concerns. Page objects handle script actions and locators independently, ensuring high code maintainability.
- **Deterministic Synchronization:** Completely avoids unsafe, hardcoded `time.sleep()` blocks. Employs Selenium explicit conditional wait strategies (`presence`, `visibility`, `clickable`) to handle asynchronous DOM updates dynamically.
- **Optimized Persistence:** Implements batch transactions (`executemany`) utilizing an isolated SQLite database layer to write retrieved data quickly without locking processing threads.
- **Robust Resource Teardown:** Features custom low-level overrides (monkey-patched destructors) to gracefully bypass common webdriver pipeline teardown issues (`WinError 6`), ensuring system processes release resources cleanly.

---

## 📂 System Architecture

The project is structured with strict adherence to professional development principles, completely eliminating bloated "single-script" anti-patterns:

```text
├── config/
│   └── config.py           # Centralized environment configs (URLs, Timeouts, Versions)
├── pages/
│   ├── base_page.py        # Core automation wrapper & explicit wait primitives
│   └── search_page.py      # Target UI mappings, CSS/XPath locators, and parsing loops
├── utils/
│   └── db_manager.py       # SQL Schema generation & batch data archiving layer
├── data/
│   └── pipeline_data.db    # Auto-generated SQLite relational database file
├── main.py                 # Core engine orchestrator and operational entry point
├── test_env.py             # Pre-flight diagnostic isolation script
└── requirements.txt        # Frozen dependency tracking file
