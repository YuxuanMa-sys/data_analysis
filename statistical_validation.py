import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from factor_analyzer import FactorAnalyzer
from sklearn.decomposition import PCA
import os
from sicas_analysis import load_data, clean_data, get_translated_label

# Create output directory
if not os.path.exists('validation_plots'):
    os.makedirs('validation_plots')

def map_questions_to_dimensions(df):
    """Map survey questions to their respective SICAS dimensions"""
    
    dimensions = {
        'sense': {
            'questions': ['您是否了解始祖鸟（Arc\'teryx）品牌？'],
            'codes': ['S1']
        },
        'interest': {
            'questions': ['始祖鸟的社交媒体内容对您的吸引力如何?'],
            'codes': ['I1']
        },
        'communication': {
            'questions': ['您是否曾与始祖鸟的社交媒体账号互动?', 
                         '您认为始祖鸟社交媒体互动的体验如何？'],
            'codes': ['C1', 'C2']
        },
        'action': {
            'questions': ['您是否因社交媒体内容购买过始祖鸟产品？'],
            'codes': ['A1']
        },
        'share': {
            'questions': ['您对始祖鸟社交媒体的整体满意度如何？'],
            'codes': ['S2']
        }
    }
    
    # Create encoded dataframe for statistical analysis
    encoded_df = pd.DataFrame()
    
    # For each dimension, encode the corresponding questions
    for dimension, info in dimensions.items():
        for i, question in enumerate(info['questions']):
            if question in df.columns:
                code = info['codes'][i]
                
                # Encode responses using appropriate mapping based on question type
                if '了解' in question:  # Brand awareness
                    mapping = {
                        '非常了解': 4, 
                        '略有了解': 3, 
                        '不太了解': 2, 
                        '完全不了解': 1
                    }
                elif '吸引力' in question:  # Content attraction
                    mapping = {
                        '非常吸引': 5,
                        '比较吸引': 4,
                        '一般': 3,
                        '不太吸引': 2,
                        '完全不吸引': 1
                    }
                elif '互动' in question and '体验' not in question:  # Interaction frequency
                    mapping = {
                        '经常互动(点赞、评论、分享等)': 4,
                        '偶尔互动': 3,
                        '很少互动': 2,
                        '从未互动': 1
                    }
                elif '体验' in question:  # Interaction experience
                    mapping = {
                        '非常好': 5,
                        '比较好': 4,
                        '一般': 3,
                        '较差': 2,
                        '非常差': 1
                    }
                elif '购买' in question:  # Purchase
                    mapping = {'是': 1, '否': 0}
                elif '满意度' in question:  # Satisfaction
                    mapping = {
                        '非常满意': 5,
                        '比较满意': 4,
                        '一般': 3,
                        '不太满意': 2,
                        '非常不满意': 1,
                        '很不满意': 1
                    }
                else:
                    continue
                
                # Apply mapping
                encoded_df[code] = df[question].map(mapping)
    
    return encoded_df, dimensions

def calculate_cronbachs_alpha(items):
    """Calculate Cronbach's alpha for a set of items"""
    # Remove rows with missing values
    items = items.dropna()
    
    # Need at least 2 items and 2 responses for calculation
    if items.shape[1] < 2 or items.shape[0] < 2:
        return np.nan
    
    # Calculate item variances and total variance
    item_variances = items.var(axis=0, ddof=1)
    total_variance = items.sum(axis=1).var(ddof=1)
    
    # Calculate Cronbach's alpha
    n = items.shape[1]
    alpha = (n / (n - 1)) * (1 - item_variances.sum() / total_variance)
    
    return alpha

def reliability_analysis(encoded_df, dimensions):
    """Perform reliability analysis using Cronbach's alpha"""
    
    reliability_results = {}
    
    # For each dimension with multiple items, calculate Cronbach's alpha
    for dimension, info in dimensions.items():
        codes = info['codes']
        
        # Need at least 2 items for reliability analysis
        if len(codes) >= 2:
            items = encoded_df[codes]
            alpha = calculate_cronbachs_alpha(items)
            reliability_results[dimension] = alpha
        elif len(codes) == 1:
            # For single-item dimensions, note that reliability can't be calculated
            reliability_results[dimension] = "Single item"
    
    # Calculate overall reliability if we have enough dimensions
    if sum(1 for v in reliability_results.values() if isinstance(v, float)) >= 2:
        # Use dimensions that have numerical alpha values
        valid_dimensions = [dim for dim, alpha in reliability_results.items() 
                           if isinstance(alpha, float)]
        
        # If we have multiple valid dimensions, calculate overall reliability
        if len(valid_dimensions) >= 2:
            all_codes = []
            for dim in valid_dimensions:
                all_codes.extend(dimensions[dim]['codes'])
            
            items = encoded_df[all_codes]
            overall_alpha = calculate_cronbachs_alpha(items)
            reliability_results['overall'] = overall_alpha
    
    return reliability_results

def validity_analysis(encoded_df, dimensions):
    """Perform correlation analysis to assess validity"""
    
    # Create a correlation matrix of all encoded items
    correlation_matrix = encoded_df.corr()
    
    # Create a dictionary to store validity results
    validity_results = {
        'correlation_matrix': correlation_matrix,
        'dimension_correlations': {}
    }
    
    # Calculate dimension scores as mean of items in each dimension
    for dimension, info in dimensions.items():
        codes = info['codes']
        if len(codes) > 0:
            # Create dimension score (if multiple items, take mean)
            encoded_df[f'{dimension}_score'] = encoded_df[codes].mean(axis=1)
    
    # Calculate correlations between dimension scores
    dimension_scores = [f'{dim}_score' for dim in dimensions.keys() 
                       if f'{dim}_score' in encoded_df.columns]
    
    if len(dimension_scores) >= 2:
        dim_corr = encoded_df[dimension_scores].corr()
        validity_results['dimension_correlations'] = dim_corr
    
    # Visualize correlation matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(validity_results['dimension_correlations'], 
                annot=True, 
                cmap='coolwarm', 
                fmt='.2f',
                linewidths=.5)
    plt.title('Correlations Between SICAS Dimensions', fontsize=16)
    plt.tight_layout()
    plt.savefig('validation_plots/dimension_correlations.png')
    plt.close()
    
    return validity_results

def factor_analysis(encoded_df, dimensions):
    """Perform factor analysis to validate the SICAS model structure"""
    
    # Combine all codes from all dimensions
    all_codes = []
    for info in dimensions.values():
        all_codes.extend(info['codes'])
    
    # Need at least 3 items for factor analysis
    if len(all_codes) < 3:
        return {"error": "Not enough items for factor analysis"}
    
    # Select items for factor analysis
    items = encoded_df[all_codes].dropna()
    
    # Check if we have enough data
    if items.shape[0] < 10:  # Need a reasonable sample size
        return {"error": "Not enough data points for factor analysis"}
    
    # Perform factor analysis
    fa_results = {}
    
    # Check for factorability
    # Kaiser-Meyer-Olkin (KMO) test
    from factor_analyzer.factor_analyzer import calculate_kmo
    kmo_all, kmo_model = calculate_kmo(items)
    fa_results['kmo'] = kmo_model
    
    # Bartlett's test of sphericity
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
    chi_square_value, p_value = calculate_bartlett_sphericity(items)
    fa_results['bartlett'] = {'chi_square': chi_square_value, 'p_value': p_value}
    
    # If data is factorable, proceed with factor analysis
    if kmo_model > 0.5 and p_value < 0.05:
        # Create factor analyzer object
        fa = FactorAnalyzer(n_factors=min(5, len(all_codes)), rotation='varimax')
        fa.fit(items)
        
        # Get factor loadings
        loadings = pd.DataFrame(
            fa.loadings_, 
            index=all_codes, 
            columns=[f'Factor {i+1}' for i in range(fa.n_factors)]
        )
        fa_results['loadings'] = loadings
        
        # Get communalities
        communalities = pd.Series(fa.get_communalities(), index=all_codes)
        fa_results['communalities'] = communalities
        
        # Get eigenvalues and variance explained
        eigenvalues, variance_explained = fa.get_eigenvalues()
        fa_results['eigenvalues'] = eigenvalues
        fa_results['variance_explained'] = variance_explained
        
        # Calculate factor scores
        factor_scores = pd.DataFrame(
            fa.transform(items),
            columns=[f'Factor {i+1}' for i in range(fa.n_factors)]
        )
        fa_results['factor_scores'] = factor_scores
        
        # Create scree plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, 'bo-')
        plt.title('Scree Plot', fontsize=16)
        plt.xlabel('Factor Number', fontsize=14)
        plt.ylabel('Eigenvalue', fontsize=14)
        plt.axhline(y=1.0, color='r', linestyle='--')  # Kaiser criterion
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('validation_plots/scree_plot.png')
        plt.close()
        
        # Create factor loadings heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(loadings, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Factor Loadings', fontsize=16)
        plt.tight_layout()
        plt.savefig('validation_plots/factor_loadings.png')
        plt.close()
    
    # If sufficient factors available, also try Principal Component Analysis (PCA)
    if len(all_codes) >= 2:
        # Perform PCA
        pca = PCA()
        pca.fit(items)
        
        # Store PCA results
        fa_results['pca_variance_ratio'] = pca.explained_variance_ratio_
        fa_results['pca_cumulative_variance'] = np.cumsum(pca.explained_variance_ratio_)
        
        # Create PCA variance plot
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), 
                pca.explained_variance_ratio_, alpha=0.7, color='g')
        plt.step(range(1, len(pca.explained_variance_ratio_) + 1), 
                np.cumsum(pca.explained_variance_ratio_), where='mid', color='r')
        plt.ylabel('Explained Variance Ratio')
        plt.xlabel('Principal Components')
        plt.title('PCA Explained Variance', fontsize=16)
        plt.axhline(y=0.8, color='k', linestyle='--')
        plt.tight_layout()
        plt.savefig('validation_plots/pca_variance.png')
        plt.close()
    
    return fa_results

def generate_validation_report(reliability_results, validity_results, factor_results):
    """Generate a report on the statistical validation results"""
    
    with open('statistical_validation_report.md', 'w', encoding='utf-8') as f:
        f.write('# SICAS Model Statistical Validation\n\n')
        
        # Introduction
        f.write('## Introduction\n\n')
        f.write('This report presents the statistical validation of the SICAS model used in the analysis of Arc\'teryx\'s social media marketing effectiveness. The validation includes reliability tests (Cronbach\'s alpha), validity assessments, and factor analysis to verify that the survey instrument properly measures the five SICAS dimensions (Sense, Interest, Communication, Action, Share).\n\n')
        
        # Reliability Analysis
        f.write('## 1. Reliability Analysis (Cronbach\'s Alpha)\n\n')
        f.write('Reliability analysis ensures that the measurement items within each dimension show internal consistency. Cronbach\'s alpha values above 0.7 are generally considered acceptable, while values above 0.8 indicate good reliability.\n\n')
        
        # Create reliability table
        f.write('| Dimension | Cronbach\'s Alpha | Interpretation |\n')
        f.write('|-----------|-----------------|----------------|\n')
        
        for dimension, alpha in reliability_results.items():
            if dimension != 'overall':
                interpretation = ""
                if alpha == "Single item":
                    interpretation = "Cannot calculate (single item)"
                elif isinstance(alpha, float):
                    if alpha >= 0.9:
                        interpretation = "Excellent"
                    elif alpha >= 0.8:
                        interpretation = "Good"
                    elif alpha >= 0.7:
                        interpretation = "Acceptable"
                    elif alpha >= 0.6:
                        interpretation = "Questionable"
                    elif alpha >= 0.5:
                        interpretation = "Poor"
                    else:
                        interpretation = "Unacceptable"
                
                # Format dimension name for display
                dim_display = dimension.capitalize()
                if dimension == 'sense':
                    dim_display = "Sense (Awareness)"
                elif dimension == 'interest':
                    dim_display = "Interest (Attraction)"
                elif dimension == 'communication':
                    dim_display = "Communication (Interaction)"
                elif dimension == 'action':
                    dim_display = "Action (Purchase)"
                elif dimension == 'share':
                    dim_display = "Share (Satisfaction)"
                
                # Format alpha value for display
                alpha_display = alpha if isinstance(alpha, str) else f"{alpha:.3f}"
                
                f.write(f'| {dim_display} | {alpha_display} | {interpretation} |\n')
        
        # Add overall reliability if available
        if 'overall' in reliability_results:
            overall_alpha = reliability_results['overall']
            interpretation = ""
            if isinstance(overall_alpha, float):
                if overall_alpha >= 0.9:
                    interpretation = "Excellent"
                elif overall_alpha >= 0.8:
                    interpretation = "Good"
                elif overall_alpha >= 0.7:
                    interpretation = "Acceptable"
                elif overall_alpha >= 0.6:
                    interpretation = "Questionable"
                elif overall_alpha >= 0.5:
                    interpretation = "Poor"
                else:
                    interpretation = "Unacceptable"
            
            overall_alpha_display = overall_alpha if isinstance(overall_alpha, str) else f"{overall_alpha:.3f}"
            f.write(f'| **Overall SICAS Model** | {overall_alpha_display} | {interpretation} |\n\n')
        
        # Add reliability interpretation
        if 'overall' in reliability_results and isinstance(reliability_results['overall'], float):
            overall_alpha = reliability_results['overall']
            if overall_alpha >= 0.7:
                f.write('The overall Cronbach\'s alpha value indicates that the SICAS model demonstrates adequate internal consistency reliability. This means that the items within each dimension consistently measure the same construct.\n\n')
            else:
                f.write('The overall Cronbach\'s alpha value suggests some inconsistency in the measurement items. This could be due to the limited number of items per dimension or variability in respondent interpretations. Future research should consider expanding the number of items per dimension to improve reliability.\n\n')
        
        # Note about single-item dimensions
        f.write('> **Note**: Several dimensions in this analysis contain only a single measurement item, which prevents the calculation of Cronbach\'s alpha for those dimensions individually. For single-item dimensions, alternative validation methods such as test-retest reliability would be more appropriate but are beyond the scope of this analysis.\n\n')
        
        # Validity Analysis
        f.write('## 2. Validity Analysis\n\n')
        f.write('Validity analysis examines whether the survey instrument accurately measures what it intends to measure. For the SICAS model, we analyze the correlations between dimensions to assess construct validity.\n\n')
        
        # Include dimension correlation plot
        f.write('### 2.1 Dimension Correlations\n\n')
        f.write('The following heatmap shows the correlations between SICAS dimensions:\n\n')
        f.write('![Dimension Correlations](validation_plots/dimension_correlations.png)\n\n')
        
        # Interpret correlation results
        if 'dimension_correlations' in validity_results and not validity_results['dimension_correlations'].empty:
            dim_corr = validity_results['dimension_correlations']
            
            # Find the strongest correlation (excluding self-correlations)
            np.fill_diagonal(dim_corr.values, 0)  # Temporarily set diagonal to 0
            strongest_corr = dim_corr.stack().idxmax()
            strongest_corr_value = dim_corr.stack().max()
            np.fill_diagonal(dim_corr.values, 1)  # Reset diagonal to 1
            
            # Get dimension names for display
            dim1_display = strongest_corr[0].split('_')[0].capitalize()
            dim2_display = strongest_corr[1].split('_')[0].capitalize()
            
            # Provide interpretation of correlations
            f.write(f'The correlation analysis reveals that the strongest relationship exists between the **{dim1_display}** and **{dim2_display}** dimensions (r = {strongest_corr_value:.2f}). ')
            
            # Identify theoretical expectations
            if ('sense_score' in dim_corr.columns and 'interest_score' in dim_corr.columns and 
                dim_corr.loc['sense_score', 'interest_score'] > 0.3):
                f.write('As theoretically expected, brand awareness (Sense) correlates positively with content attraction (Interest), suggesting that consumers who are more aware of the brand tend to find its content more attractive. ')
            
            if ('interest_score' in dim_corr.columns and 'action_score' in dim_corr.columns and 
                dim_corr.loc['interest_score', 'action_score'] > 0.3):
                f.write('The correlation between content attraction (Interest) and purchase behavior (Action) confirms that engaging content contributes to conversion. ')
            
            if ('communication_score' in dim_corr.columns and 'share_score' in dim_corr.columns and 
                dim_corr.loc['communication_score', 'share_score'] > 0.3):
                f.write('The relationship between interaction (Communication) and satisfaction (Share) highlights how engagement impacts overall satisfaction with the brand\'s social media presence. ')
            
            f.write('\n\n')
            
            # Overall validity assessment
            avg_corr = (dim_corr.sum().sum() - dim_corr.shape[0]) / (dim_corr.size - dim_corr.shape[0])
            if avg_corr > 0.4:
                f.write('The moderate to strong correlations between dimensions provide evidence of construct validity, indicating that the five dimensions of the SICAS model are interrelated as expected by the theoretical framework. However, the correlations are not so high as to suggest redundancy among dimensions.\n\n')
            elif avg_corr > 0.2:
                f.write('The modest correlations between dimensions suggest that the SICAS components are measuring related but distinct aspects of social media marketing effectiveness, providing evidence of discriminant validity while maintaining theoretical coherence.\n\n')
            else:
                f.write('The relatively weak correlations between dimensions suggest that the SICAS components may be measuring distinct aspects of social media marketing effectiveness with limited overlap. While this demonstrates discriminant validity, it raises questions about the theoretical coherence of the model as a unified framework.\n\n')
        
        # Factor Analysis
        f.write('## 3. Factor Analysis\n\n')
        f.write('Factor analysis examines whether the measurement items cluster as expected into the five SICAS dimensions. This helps validate the structural integrity of the model.\n\n')
        
        # Check if factor analysis was performed successfully
        if 'error' in factor_results:
            f.write(f'**Note**: {factor_results["error"]}. Factor analysis could not be performed due to insufficient data.\n\n')
        else:
            # Report KMO and Bartlett's test results
            if 'kmo' in factor_results:
                f.write('### 3.1 Sampling Adequacy\n\n')
                kmo = factor_results['kmo']
                f.write(f'**Kaiser-Meyer-Olkin (KMO) Measure**: {kmo:.3f}\n\n')
                
                if kmo >= 0.8:
                    f.write('The KMO value indicates **excellent** sampling adequacy for factor analysis.\n\n')
                elif kmo >= 0.7:
                    f.write('The KMO value indicates **good** sampling adequacy for factor analysis.\n\n')
                elif kmo >= 0.6:
                    f.write('The KMO value indicates **acceptable** sampling adequacy for factor analysis.\n\n')
                elif kmo >= 0.5:
                    f.write('The KMO value indicates **mediocre** but acceptable sampling adequacy for factor analysis.\n\n')
                else:
                    f.write('The KMO value indicates **poor** sampling adequacy, suggesting caution in interpreting factor analysis results.\n\n')
            
            if 'bartlett' in factor_results:
                chi_square = factor_results['bartlett']['chi_square']
                p_value = factor_results['bartlett']['p_value']
                
                f.write(f'**Bartlett\'s Test of Sphericity**: Chi-square = {chi_square:.2f}, p-value = {p_value:.4f}\n\n')
                
                if p_value < 0.05:
                    f.write('Bartlett\'s test is statistically significant (p < 0.05), indicating that factor analysis is appropriate for this data.\n\n')
                else:
                    f.write('Bartlett\'s test is not statistically significant (p > 0.05), suggesting caution in interpreting factor analysis results.\n\n')
            
            # Scree plot
            f.write('### 3.2 Factor Extraction\n\n')
            f.write('The scree plot helps determine the optimal number of factors to extract:\n\n')
            f.write('![Scree Plot](validation_plots/scree_plot.png)\n\n')
            
            # Factor loadings
            if 'loadings' in factor_results:
                f.write('### 3.3 Factor Loadings\n\n')
                f.write('The factor loadings show how strongly each measurement item relates to each factor:\n\n')
                f.write('![Factor Loadings](validation_plots/factor_loadings.png)\n\n')
                
                # Interpret factor loadings
                loadings = factor_results['loadings']
                f.write('**Interpretation**:\n\n')
                
                # Check if loadings align with SICAS dimensions
                aligned_with_theory = True
                for col in loadings.columns:
                    # For each factor, identify items with high loadings
                    high_loading_items = loadings[loadings[col] > 0.4][col].index.tolist()
                    if not high_loading_items:
                        continue
                    
                    # Check if these items come from the same SICAS dimension
                    item_dimensions = []
                    for item in high_loading_items:
                        if item.startswith('S'):
                            item_dimensions.append('Sense' if item == 'S1' else 'Share')
                        elif item.startswith('I'):
                            item_dimensions.append('Interest')
                        elif item.startswith('C'):
                            item_dimensions.append('Communication')
                        elif item.startswith('A'):
                            item_dimensions.append('Action')
                    
                    if len(set(item_dimensions)) > 1:
                        aligned_with_theory = False
                
                if aligned_with_theory:
                    f.write('The factor loadings generally align with the theoretical SICAS dimensions, with items from the same dimension loading most strongly on the same factor. This provides evidence of construct validity for the SICAS model.\n\n')
                else:
                    f.write('The factor loading pattern shows some deviation from the theoretical SICAS structure. Some items from different dimensions load on the same factor, which suggests that respondents may perceive these dimensions as related or that the measurement items may need refinement to better distinguish between dimensions.\n\n')
            
            # PCA results
            if 'pca_variance_ratio' in factor_results:
                f.write('### 3.4 Principal Component Analysis\n\n')
                f.write('PCA provides an alternative view of the dimensional structure:\n\n')
                f.write('![PCA Variance](validation_plots/pca_variance.png)\n\n')
                
                # Interpret PCA results
                variance_explained = factor_results['pca_variance_ratio']
                cumulative_variance = factor_results['pca_cumulative_variance']
                components_for_80 = np.argmax(cumulative_variance >= 0.8) + 1 if any(cumulative_variance >= 0.8) else len(cumulative_variance)
                
                f.write(f'The first component explains {variance_explained[0]:.1%} of the total variance, while the first {components_for_80} components together explain {cumulative_variance[components_for_80-1]:.1%} of the variance.\n\n')
                
                if components_for_80 <= 5:
                    f.write(f'The fact that {components_for_80} components explain over 80% of the variance is consistent with the five-dimensional SICAS model structure.\n\n')
                else:
                    f.write(f'The PCA results suggest that more than the five theoretical SICAS dimensions may be present in the data, indicating potential complexity in how respondents perceive the social media marketing elements.\n\n')
        
        # Conclusion
        f.write('## Conclusion\n\n')
        
        # Assess overall statistical validity
        reliability_adequate = False
        if 'overall' in reliability_results and isinstance(reliability_results['overall'], float):
            reliability_adequate = reliability_results['overall'] >= 0.7
        
        validity_adequate = False
        if 'dimension_correlations' in validity_results and not validity_results['dimension_correlations'].empty:
            avg_corr = (dim_corr.sum().sum() - dim_corr.shape[0]) / (dim_corr.size - dim_corr.shape[0])
            validity_adequate = avg_corr > 0.2
        
        factor_adequate = False
        if 'error' not in factor_results and 'kmo' in factor_results:
            factor_adequate = factor_results['kmo'] >= 0.5
        
        # Generate conclusion based on results
        if reliability_adequate and validity_adequate and factor_adequate:
            f.write('The statistical validation provides strong support for the SICAS model as an effective framework for analyzing social media marketing effectiveness. The model demonstrates adequate reliability, construct validity, and structural integrity. The five dimensions (Sense, Interest, Communication, Action, Share) form a coherent framework that effectively captures key aspects of consumer engagement with brand social media.\n\n')
        elif (reliability_adequate and validity_adequate) or (reliability_adequate and factor_adequate) or (validity_adequate and factor_adequate):
            f.write('The statistical validation provides moderate support for the SICAS model. While some aspects of the validation are strong, others suggest areas for refinement. The current implementation of the model is adequate for analysis purposes, but future research should consider enhancing the measurement instrument with additional items per dimension to strengthen the model\'s statistical properties.\n\n')
        else:
            f.write('The statistical validation results suggest that the current implementation of the SICAS model has limitations. While the theoretical framework is sound, the measurement instrument may benefit from significant refinement. Future research should consider developing more robust multi-item scales for each dimension and validating them with larger sample sizes. Despite these limitations, the model still provides useful insights into social media marketing effectiveness when interpreted cautiously.\n\n')
        
        f.write('### Recommendations for Future Research\n\n')
        f.write('1. **Expanded Measurement Scales**: Develop multiple items for each SICAS dimension to enable more robust reliability assessment.\n\n')
        f.write('2. **Larger Sample Size**: Collect data from a larger sample to improve the statistical power of factor analysis.\n\n')
        f.write('3. **Confirmatory Factor Analysis**: Conduct confirmatory factor analysis to formally test the hypothesized five-factor structure of the SICAS model.\n\n')
        f.write('4. **Test-Retest Reliability**: Assess the stability of measurements over time, particularly for single-item dimensions.\n\n')
        f.write('5. **Cross-Validation**: Validate the model across different industries and cultural contexts to establish generalizability.\n\n')

def main():
    print("Loading data for statistical validation...")
    df = load_data()
    df = clean_data(df)
    
    print("Mapping questions to SICAS dimensions...")
    encoded_df, dimensions = map_questions_to_dimensions(df)
    
    print("Performing reliability analysis (Cronbach's alpha)...")
    reliability_results = reliability_analysis(encoded_df, dimensions)
    
    print("Performing validity analysis...")
    validity_results = validity_analysis(encoded_df, dimensions)
    
    print("Performing factor analysis...")
    factor_results = factor_analysis(encoded_df, dimensions)
    
    print("Generating statistical validation report...")
    generate_validation_report(reliability_results, validity_results, factor_results)
    
    print("Statistical validation complete! Results saved in 'statistical_validation_report.md' and 'validation_plots/' directory.")
    
    # Commit and push results to GitHub
    try:
        import subprocess
        subprocess.run(["git", "add", "validation_plots/", "statistical_validation_report.md", "statistical_validation.py"])
        subprocess.run(["git", "commit", "-m", "Added statistical validation of the SICAS model"])
        subprocess.run(["git", "push"])
        print("Changes committed and pushed to GitHub repository.")
    except Exception as e:
        print(f"Note: Could not automatically commit and push changes: {str(e)}")

if __name__ == "__main__":
    main() 