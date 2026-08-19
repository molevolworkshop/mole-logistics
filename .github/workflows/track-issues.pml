name: Sync Tracking Issues

on:
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    permissions:
      issues: write # Required for the workflow to create issues

    steps:
      - name: Checkout mole-logistics
        uses: actions/checkout@v4

      - name: Checkout website repository
        uses: actions/checkout@v4
        with:
          repository: molevolworkshop/molevolworkshop.github.io # Replace with your actual website repo if different
          token: ${{ secrets.GITHUB_TOKEN }}
          path: website-repo

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Run Issue Sync Script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/sync-faculty-issues.py