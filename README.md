FinScout: Automated Market Intelligence Pipeline 🚀FinScout is a full-stack Robotic Process Automation (RPA) solution. It autonomously navigates financial portals, extracts real-time market data, cleanses it via an ETL pipeline, and visualizes it on an interactive dashboard.💼 Business Problem SolvedConsultants and Analysts spend hours manually copying data from dynamic websites like Yahoo Finance. APIs like Bloomberg are expensive ($24k/year).FinScout solves this by:Automating Extraction: Using Playwright to scrape dynamic JS-heavy data.Ensuring Quality: Using Pandas/Pydantic to validate data (removing 'M/B' suffixes, fixing types).Democratizing Data: Providing a Streamlit Dashboard for non-technical users and a REST API for developers.🏗 Architecturegraph LR
    User[User/Analyst] -->|Clicks Trigger| UI[Streamlit Dashboard]
    UI -->|POST /trigger| API[FastAPI Backend]
    API -->|Spawns| Bot[Playwright Bot]
    Bot -->|Scrapes| Web[Yahoo Finance]
    Bot -->|Raw Data| ETL[Pandas Transformer]
    ETL -->|Clean Data| DB[(SQLite Database)]
    DB -->|JSON| API
    API -->|Visuals| UI
🛠 Technology StackComponentToolWhy?ScraperPlaywrightFaster/more stable than Selenium. Handles modern React/Angular sites easily.BackendFastAPIAsync-native (High concurrency). Auto-generates Swagger documentation.ETLPandasVectorized operations for cleaning data. Robust logic testing.FrontendStreamlitRapid visualization for stakeholders.CI/CDGitHub ActionsEnsures ETL logic passes tests before deployment.🚀 How to Run LocallyInstall Dependenciespip install -r requirements.txt
playwright install chromium
Start the Backend (API)python main.py
Start the Frontend (Dashboard)Open a new terminal:streamlit run app/dashboard.py
🧪 Testing StrategyWe strictly separate Logic Testing from Integration Testing.tests/test_pipeline.py: Validates the ETL logic (e.g., does "2.5M" become 2500000?).tests/test_api.py: Validates that API endpoints return correct HTTP status codes.Run tests with:pytest
