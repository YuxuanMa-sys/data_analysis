# Arc'teryx Social Media Marketing Analysis

This project analyzes survey data about Arc'teryx (始祖鸟) brand using the SICAS model for social media marketing effectiveness.

## SICAS Model

The SICAS model is a framework for analyzing social media marketing effectiveness:

- **S** - Sense (Awareness/Attention)
- **I** - Interest
- **C** - Communication/Connection
- **A** - Action (Purchase)
- **S** - Share/Satisfaction

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure your survey data is in CSV format in a file named `data.csv` in the project root.

## Running the Analysis

To run the analysis:

```bash
python sicas_analysis.py
```

## Chinese Character Handling

The script includes a translation system that converts Chinese text labels to English for visualization purposes. This approach avoids font rendering issues with Chinese characters in matplotlib. The translations maintain the meaning of the original categories while ensuring proper display in the generated plots.

The translation dictionary is located in the `get_translated_label()` function in the script and can be extended with additional translations if needed.

## Output

The script will generate:

1. A comprehensive analysis report in `sicas_analysis_report.md`
2. Visualizations in the `plots/` directory, including:
   - Demographic analysis charts (with English labels)
   - SICAS component breakdowns (with English labels)
   - SICAS funnel visualization

## Data Requirements

The script is designed to work with survey data that includes questions related to:
- Demographics (gender, age, occupation, income)
- Social media usage habits
- Brand awareness and perception
- Social media interactions
- Purchase behavior and barriers
- Overall satisfaction with brand social media

If your data structure is different, you may need to adjust the column names in the `analyze_sicas()` and `perform_demographic_analysis()` functions, and potentially update the translation dictionary. 