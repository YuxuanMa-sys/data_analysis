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

### Basic SICAS Analysis

To run the basic SICAS analysis:

```bash
python sicas_analysis.py
```

### Enhanced Thesis Analysis

To generate the enhanced thesis report with additional visualizations:

```bash
python thesis_enhancements.py
```

### Additional Column Analysis

To analyze additional survey columns beyond the core SICAS framework:

```bash
python enhanced_analysis.py
```

### Statistical Validation

To run statistical validation tests (reliability, validity, factor analysis):

```bash
python statistical_validation.py
```

## Reports and Output Files

The project generates multiple reports:

1. **Core SICAS Analysis**
   - `sicas_analysis_report.md`: Basic SICAS model analysis
   - Visualizations in `plots/` directory

2. **Enhanced Thesis Report**
   - `thesis_report.md`: Comprehensive analysis formatted for thesis presentation
   - `thesis_report.html`: HTML version for better formatting
   - `thesis_report.pdf`: PDF version for distribution
   - Enhanced visualizations in `thesis_plots/` directory

3. **Additional Analysis**
   - `additional_analysis_report.md`: Analysis of additional survey columns
   - Supplementary visualizations in `additional_plots/` directory

4. **Statistical Validation**
   - `statistical_validation_report.md`: Statistical validation of the SICAS model
   - Validation visualizations in `validation_plots/` directory, including:
     - Dimension correlations
     - Factor loadings
     - Scree plot
     - PCA variance

## Chinese Character Handling

The script includes a translation system that converts Chinese text labels to English for visualization purposes. This approach avoids font rendering issues with Chinese characters in matplotlib. The translations maintain the meaning of the original categories while ensuring proper display in the generated plots.

The translation dictionary is located in the `get_translated_label()` function in the script and can be extended with additional translations if needed.

## Statistical Validation Overview

The statistical validation includes:

1. **Reliability Analysis**: Cronbach's alpha tests to ensure internal consistency
2. **Validity Analysis**: Correlation analysis between SICAS dimensions
3. **Factor Analysis**: Examination of factor loadings and principal component analysis

These statistical tests help confirm the validity of the SICAS model as a framework for analyzing social media marketing effectiveness.

## Data Requirements

The script is designed to work with survey data that includes questions related to:
- Demographics (gender, age, occupation, income)
- Social media usage habits
- Brand awareness and perception
- Social media interactions
- Purchase behavior and barriers
- Overall satisfaction with brand social media

If your data structure is different, you may need to adjust the column names in the analysis functions and potentially update the translation dictionary. 