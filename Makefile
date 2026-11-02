.PHONY: serve verify

serve:
	python3 -m http.server 8000 --directory dist

verify:
	node --check dist/app.js
	python3 scripts/verify_publication_claims.py
	python3 scripts/verify_research.py
	python3 scripts/verify_portfolios.py
	python3 scripts/verify_monthly_launches.py
	python3 scripts/verify_paper_summaries.py
