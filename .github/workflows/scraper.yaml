name: Daily Community Scraper

on:
  schedule:
    - cron: '0 9 * * *'  # 매일 오전 9시에 실행
  workflow_dispatch:

jobs:
  scrape-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repo
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4

    - name: Run scraper script
      run: |
        python scraper.py

    - name: Copy output to docs/index.md
      run: |
        mkdir -p docs
        cp output.md docs/index.md

    - name: Commit and push updates
      run: |
        git config --global user.name 'github-actions'
        git config --global user.email 'actions@github.com'
        git add docs/index.md
        git commit -m "📰 Update daily popular posts"
        git push

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
