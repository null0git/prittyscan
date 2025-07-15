# prittyscan

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

**prittyscan** is an advanced Python wrapper for the popular network scanning tool [Nmap](https://nmap.org/). It executes Nmap scans and parses its XML output to present the results in a clean, colorful, and well-organized terminal interface using the [Rich](https://github.com/Textualize/rich) library.

This tool supports TCP and UDP scanning with service version detection, execution of Nmap NSE scripts, live display of scan results in tables with nested script outputs, and exports results to both JSON and CSV formats for further analysis or integration.

---

## Features

- Perform TCP (`-sV`) and UDP (`-sU`) port scans with detailed service/version detection  
- Run multiple Nmap NSE scripts and display their outputs directly under corresponding ports  
- Nicely formatted and color-coded terminal tables and panels using Rich  
- Export scan data to JSON and CSV for easy consumption in other tools or reports  
- Pass arbitrary additional arguments directly to Nmap to leverage all its advanced scanning options  
- Easy-to-use command-line interface with descriptive output and logging  

---

## Prerequisites

- **Nmap** installed and accessible via your system's PATH (test by running `nmap --version`)  
- **Python 3.7+** installed  
- Python package **rich** installed (`pip install rich`)  

---

## Installation

1. Ensure Nmap is installed on your system.

   - On Debian/Ubuntu:  
     ```bash
     sudo apt install nmap
     ```
   - On macOS (with Homebrew):  
     ```bash
     brew install nmap
     ```
   - On Windows: Download installer from [nmap.org](https://nmap.org/download.html)

2. Install Python dependencies:

   ```bash
   pip install rich
   ```

| Option          | Description                                                         | Example                                |
| --------------- | ------------------------------------------------------------------- | -------------------------------------- |
| `<target>`      | Target hostname or IP to scan (required)                            | `scanme.nmap.org`                      |
| `-p, --ports`   | Comma-separated ports or port ranges (e.g., 22,80,443,1000-2000)    | `-p 22,80,443`                         |
| `-u, --udp`     | Enable UDP scan                                                     | `-u`                                   |
| `-s, --scripts` | Comma-separated Nmap NSE scripts to run                             | `-s default,safe`                      |
| `--export-csv`  | Export scan results to CSV file                                     | `--export-csv results.csv`             |
| `--export-json` | Export scan results to JSON file                                    | `--export-json results.json`           |
| `--extra-args`  | Pass additional raw arguments directly to Nmap (all following args) | `--extra-args --reason --osscan-guess` |
