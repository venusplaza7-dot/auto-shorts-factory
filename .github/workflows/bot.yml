name: auto-shorts-factory
on:
  schedule:
    - cron: '0 */2 * * *'
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install
        run: |
          sudo apt-get update && sudo apt-get install -y ffmpeg
          pip install -r requirements.txt
      - name: Generate Short
        env:
          YT_API_KEY: ${{ secrets.YT_API_KEY }}
          GOOGLE_CLIENT_ID: ${{ secrets.GOOGLE_CLIENT_ID }}
          GOOGLE_CLIENT_SECRET: ${{ secrets.GOOGLE_CLIENT_SECRET }}
          GOOGLE_REFRESH_TOKEN: ${{ secrets.GOOGLE_REFRESH_TOKEN }}
        run: python generate.py
