# LegalDocAnalyzer
LegalDocAnalyzer/
├── app.py                  # Flask backend
├── config.py               # Paths/API keys
├── requirements.txt        # Dependencies
├── data/
│   ├── LeSICiN/           # Indian Supreme Court cases
│   └── FIR/               # FIR dataset for structure analysis
├── models/
│   ├── inlegalbert/       # Fine-tuned InLegalBERT model
│   └── summarization/     # Trained summarizer
├── templates/              # Frontend HTML
│   └── index.html
└── utils/
    ├── preprocess.py       # Data cleaning
    └── translate.py        # Translation (Hindi/Tamil)
