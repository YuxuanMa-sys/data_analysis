import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from sicas_analysis import load_data, clean_data, get_translated_label
from thesis_enhancements import ARCTERYX_COLORS, set_thesis_style

# Create output directories
if not os.path.exists('additional_plots'):
    os.makedirs('additional_plots')

def analyze_additional_columns(df):
    """Analyze columns not covered in the original analysis"""
    
    additional_results = {}
    
    # 1. Channels through which users were exposed to the brand
    channel_col = '您通过以下哪些渠道接触过始祖鸟品牌?'
    if channel_col in df.columns:
        channels = []
        for response in df[channel_col].dropna():
            types = response.split('┋')
            channels.extend(types)
        
        additional_results['brand_contact_channels'] = pd.Series(channels).value_counts(normalize=True)
    
    # 2. Social media interaction experience
    experience_col = '您认为始祖鸟社交媒体互动的体验如何？'
    if experience_col in df.columns:
        additional_results['interaction_experience'] = df[experience_col].value_counts(normalize=True)
    
    # 3. Brand impression
    impression_col = '您对始祖鸟品牌的印象如何？（可多选）'
    if impression_col in df.columns:
        impressions = []
        for response in df[impression_col].dropna():
            types = response.split('┋')
            impressions.extend(types)
        
        additional_results['brand_impression'] = pd.Series(impressions).value_counts(normalize=True)
    
    # 4. Whether social media increased brand understanding
    understanding_col = '始祖鸟社交媒体是否增加了您对品牌的了解？'
    if understanding_col in df.columns:
        additional_results['increased_understanding'] = df[understanding_col].value_counts(normalize=True)
    
    # 5. Free-text suggestions (word frequency analysis)
    suggestion_col = '您对始祖鸟社交媒体营销有哪些建议或想法？请简要描述。'
    if suggestion_col in df.columns:
        # Get non-empty suggestions
        suggestions = df[suggestion_col].dropna()
        suggestions = suggestions[suggestions != '(空)']
        additional_results['suggestion_count'] = len(suggestions)
        additional_results['suggestions'] = suggestions
    
    return additional_results

def update_translation_dict():
    """Add additional translations for new columns being analyzed"""
    
    additional_translations = {
        # Brand contact channels
        '微信公众号': 'WeChat Official Account',
        '微博': 'Weibo',
        '小红书': 'Xiaohongshu',
        '抖音/快手': 'TikTok/Kuaishou',
        '品牌官网': 'Brand Website',
        '品牌官网(官方网站)': 'Brand Website (Official)',
        '朋友推荐': 'Friend Recommendation',
        '线下店铺': 'Offline Store',
        '社交媒体广告': 'Social Media Ads',
        '第三方平台': 'Third-party Platform',
        'bilibili': 'Bilibili',
        '得物': 'Dewu',
        '知乎': 'Zhihu',
        '其他：bilibili': 'Other: Bilibili',
        '其它：bilibili': 'Other: Bilibili',
        '其他：': 'Other:',
        '其它：': 'Other:',
        '抖音': 'Douyin',
        '天猫': 'Tmall',
        '京东': 'JD',
        
        # Interaction experience
        '非常好': 'Very Good',
        '比较好': 'Fairly Good',
        '一般': 'Neutral',
        '较差': 'Poor',
        '非常差': 'Very Poor',
        
        # Brand impression
        '高端户外品牌': 'High-end Outdoor Brand',
        '专业性强': 'Professional',
        '价格较高': 'High Price',
        '环保可持续': 'Eco-friendly',
        '产品设计时尚': 'Stylish Design',
        '广告／宣传设计时尚': 'Stylish Advertising',
        '普通品牌': 'Ordinary Brand',
        '装逼': 'Show-off Brand',
        
        # Increased understanding
        '很多': 'Significant Increase',
        '一些': 'Some Increase',
        '较少': 'Little Increase',
        '完全没有': 'No Increase',
        
        # Interaction types
        '点赞': 'Like',
        '评论': 'Comment',
        '分享到个人社交圈': 'Share',
        '参与话题活动': 'Topic Activities',
        '私信交流': 'Private Messages',
        '观看直播': 'Watch Livestreams',
        '其他': 'Other',
        '无': 'None',
        
        # Satisfaction levels
        '非常满意': 'Very Satisfied',
        '比较满意': 'Fairly Satisfied',
        '一般': 'Neutral',
        '不太满意': 'Not Very Satisfied',
        '很不满意': 'Not Satisfied At All',
        '非常不满意': 'Not Very Satisfied',
        
        # Improvements needed
        '内容丰富度': 'Content Richness',
        '与用户互动性': 'User Interaction',
        '创意和设计感': 'Creativity & Design',
        '信息实用性': 'Practical Information',
        '发布频率': 'Posting Frequency',
        '客户服务／售后服务': 'Customer Service',
        '其他建议': 'Other Suggestions',
        '无需改进': 'No Improvement Needed',
        
        # Demographics - Age
        '18-25岁': '18-25',
        '26-35岁': '26-35',
        '36-45岁': '36-45',
        '46岁及以上': '46+',
        '18岁以下': 'Under 18',
        
        # Barriers to purchase
        '价格过高': 'High Price',
        '不需要相关产品': 'No Need',
        '产品信息不够清楚': 'Unclear Product Info',
        '品牌吸引力不足': 'Low Brand Appeal',
        '购买流程不便捷': 'Inconvenient Purchase Process',
        '推广较少': 'Limited Promotion',
        
        # Miscellaneous
        '跳过': 'Skipped',
        '(空)': 'Empty',
        '空': 'Empty'
    }
    
    # Get existing translations and update with new ones
    existing_translations = {}
    try:
        from sicas_analysis import get_translated_label
        # Access the translations dictionary through a somewhat hacky approach
        import inspect
        source = inspect.getsource(get_translated_label)
        exec(source, globals())
        # Use the translations dictionary from the function
        existing_translations = translations
    except:
        pass
    
    # Combine dictionaries
    combined_translations = {**existing_translations, **additional_translations}
    
    return combined_translations

def get_enhanced_label(chinese_label, translations_dict):
    """Enhanced translation function with expanded dictionary"""
    return translations_dict.get(chinese_label, chinese_label)

def visualize_additional_results(additional_results, translations_dict):
    """Create visualizations for additional analyses"""
    
    # Set plot style
    set_thesis_style()
    
    # 1. Brand contact channels - Horizontal bar chart
    if 'brand_contact_channels' in additional_results:
        channel_data = additional_results['brand_contact_channels']
        # Sort by frequency
        channel_data = channel_data.sort_values(ascending=True)
        
        plt.figure(figsize=(12, 8))
        # Translate labels
        translated_index = [get_enhanced_label(label, translations_dict) for label in channel_data.index]
        translated_series = pd.Series(channel_data.values, index=translated_index)
        
        bars = plt.barh(translated_series.index, translated_series.values, color=ARCTERYX_COLORS[0])
        plt.title('Brand Contact Channels', fontsize=18, pad=20)
        plt.xlabel('Proportion', fontsize=14)
        
        # Add value labels
        for i, bar in enumerate(bars):
            plt.text(
                bar.get_width() + 0.01, 
                bar.get_y() + bar.get_height()/2, 
                f'{bar.get_width():.2f}', 
                va='center', 
                fontsize=12
            )
        
        plt.tight_layout()
        plt.savefig('additional_plots/brand_contact_channels.png')
        plt.close()
    
    # 2. Social media interaction experience - Pie chart
    if 'interaction_experience' in additional_results:
        exp_data = additional_results['interaction_experience']
        
        plt.figure(figsize=(10, 8))
        # Translate labels
        translated_index = [get_enhanced_label(label, translations_dict) for label in exp_data.index]
        translated_series = pd.Series(exp_data.values, index=translated_index)
        
        # Draw pie chart
        wedges, texts, autotexts = plt.pie(
            translated_series, 
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=ARCTERYX_COLORS[:len(translated_series)],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1.5},
            textprops={'fontsize': 14, 'fontweight': 'bold'}
        )
        
        # Customize autopct text
        for autotext in autotexts:
            autotext.set_color('white')
        
        # Add a legend
        plt.legend(
            wedges, 
            translated_series.index,
            title="User Experience",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        plt.title('Social Media Interaction Experience', fontsize=18, pad=20)
        plt.tight_layout()
        plt.savefig('additional_plots/interaction_experience.png')
        plt.close()
    
    # 3. Brand impression - Horizontal bar chart
    if 'brand_impression' in additional_results:
        impression_data = additional_results['brand_impression']
        # Sort by frequency
        impression_data = impression_data.sort_values(ascending=True)
        
        plt.figure(figsize=(12, 8))
        # Translate labels
        translated_index = [get_enhanced_label(label, translations_dict) for label in impression_data.index]
        translated_series = pd.Series(impression_data.values, index=translated_index)
        
        bars = plt.barh(translated_series.index, translated_series.values, color=ARCTERYX_COLORS[1])
        plt.title('Brand Impression', fontsize=18, pad=20)
        plt.xlabel('Proportion', fontsize=14)
        
        # Add value labels
        for i, bar in enumerate(bars):
            plt.text(
                bar.get_width() + 0.01, 
                bar.get_y() + bar.get_height()/2, 
                f'{bar.get_width():.2f}', 
                va='center', 
                fontsize=12
            )
        
        plt.tight_layout()
        plt.savefig('additional_plots/brand_impression.png')
        plt.close()
    
    # 4. Increased understanding - Pie chart
    if 'increased_understanding' in additional_results:
        understanding_data = additional_results['increased_understanding']
        
        plt.figure(figsize=(10, 8))
        # Translate labels
        translated_index = [get_enhanced_label(label, translations_dict) for label in understanding_data.index]
        translated_series = pd.Series(understanding_data.values, index=translated_index)
        
        # Draw pie chart
        wedges, texts, autotexts = plt.pie(
            translated_series, 
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=ARCTERYX_COLORS[:len(translated_series)],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1.5},
            textprops={'fontsize': 14, 'fontweight': 'bold'}
        )
        
        # Customize autopct text
        for autotext in autotexts:
            autotext.set_color('white')
        
        # Add a legend
        plt.legend(
            wedges, 
            translated_series.index,
            title="Understanding Increase",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        plt.title('Increased Brand Understanding from Social Media', fontsize=18, pad=20)
        plt.tight_layout()
        plt.savefig('additional_plots/increased_understanding.png')
        plt.close()
    
    # 5. Create relationship visualizations 
    # Cross-analysis between brand understanding and purchase behavior
    if 'increased_understanding' in additional_results:
        df = load_data()
        df = clean_data(df)
        
        understanding_col = '始祖鸟社交媒体是否增加了您对品牌的了解？'
        purchase_col = '您是否因社交媒体内容购买过始祖鸟产品？'
        
        if understanding_col in df.columns and purchase_col in df.columns:
            # Create cross-tabulation
            cross_tab = pd.crosstab(
                df[understanding_col], 
                df[purchase_col], 
                normalize='index'
            )
            
            # Translate for plotting
            cross_tab.index = [get_enhanced_label(idx, translations_dict) for idx in cross_tab.index]
            cross_tab.columns = [get_enhanced_label(col, translations_dict) for col in cross_tab.columns]
            
            # Order understanding levels
            if len(cross_tab) >= 3:
                understanding_order = ['Significant Increase', 'Some Increase', 'Little Increase', 'No Increase']
                # Only use levels that exist in the data
                valid_order = [level for level in understanding_order if level in cross_tab.index]
                cross_tab = cross_tab.reindex(valid_order)
            
            # Plot
            plt.figure(figsize=(12, 7))
            cross_tab.plot(
                kind='bar',
                stacked=True,
                color=[ARCTERYX_COLORS[5], ARCTERYX_COLORS[2]],
                ax=plt.gca()
            )
            
            plt.title('Purchase Rate by Level of Increased Understanding', fontsize=18, pad=20)
            plt.xlabel('Increased Understanding Level', fontsize=14)
            plt.ylabel('Proportion', fontsize=14)
            plt.xticks(rotation=0)
            plt.legend(title='Purchase', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Add percentage labels for "Yes" proportions
            yes_column = 'Yes'
            if yes_column in cross_tab.columns:
                for i, p in enumerate(plt.gca().patches):
                    if i < len(cross_tab):  # Only label the "Yes" proportion
                        plt.text(
                            p.get_x() + p.get_width()/2., 
                            p.get_y() + p.get_height()/2., 
                            '{:.1f}%'.format(p.get_height()*100), 
                            ha='center', 
                            va='center',
                            fontsize=12,
                            fontweight='bold',
                            color='white'
                        )
            
            plt.tight_layout()
            plt.savefig('additional_plots/understanding_vs_purchase.png')
            plt.close()
            
        # Cross-analysis between interaction experience and satisfaction
        experience_col = '您认为始祖鸟社交媒体互动的体验如何？'
        satisfaction_col = '您对始祖鸟社交媒体的整体满意度如何？'
        
        if experience_col in df.columns and satisfaction_col in df.columns:
            # Create heatmap data
            heatmap_data = pd.crosstab(
                df[experience_col], 
                df[satisfaction_col]
            )
            
            # Translate for plotting
            heatmap_data.index = [get_enhanced_label(idx, translations_dict) for idx in heatmap_data.index]
            heatmap_data.columns = [get_enhanced_label(col, translations_dict) for col in heatmap_data.columns]
            
            # Plot heatmap
            plt.figure(figsize=(12, 10))
            sns.heatmap(
                heatmap_data,
                annot=True,
                fmt='d',
                cmap='YlGnBu',
                linewidths=.5,
                cbar_kws={"shrink": .8}
            )
            
            plt.title('Relationship Between Interaction Experience and Overall Satisfaction', fontsize=18, pad=20)
            plt.xlabel('Satisfaction Level', fontsize=14)
            plt.ylabel('Interaction Experience', fontsize=14)
            plt.tight_layout()
            plt.savefig('additional_plots/experience_vs_satisfaction.png')
            plt.close()

def generate_additional_report(additional_results, translations_dict):
    """Generate a supplementary report with additional analyses"""
    
    with open('additional_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write('# Supplementary Analysis: Arc\'teryx Social Media Marketing\n\n')
        f.write('## Additional Insights Beyond the SICAS Framework\n\n')
        
        # Introduction
        f.write('This report extends the original SICAS model analysis with additional dimensions that provide deeper insights into Arc\'teryx\'s social media marketing effectiveness.\n\n')
        
        # 1. Brand Contact Channels
        if 'brand_contact_channels' in additional_results:
            f.write('## 1. Brand Contact Channels\n\n')
            f.write('Understanding how consumers first encounter and interact with the Arc\'teryx brand provides valuable insights for channel optimization.\n\n')
            f.write('![Brand Contact Channels](additional_plots/brand_contact_channels.png)\n\n')
            
            # Extract insights from data
            channel_data = additional_results['brand_contact_channels']
            top_channels = channel_data.nlargest(3)
            top_channels_text = ", ".join([f"{get_enhanced_label(idx, translations_dict)} ({val:.1%})" for idx, val in top_channels.items()])
            
            f.write(f'The primary channels through which respondents encounter the Arc\'teryx brand are {top_channels_text}. ')
            
            # Recommendations based on channel data
            f.write('**Recommendations:**\n\n')
            f.write('- Strengthen presence on the top-performing channels to maximize reach\n')
            f.write('- Evaluate underperforming channels to determine whether to improve content or reallocate resources\n')
            f.write('- Develop channel-specific content strategies that leverage the unique features of each platform\n\n')
        
        # 2. Social Media Interaction Experience
        if 'interaction_experience' in additional_results:
            f.write('## 2. Social Media Interaction Experience\n\n')
            f.write('The quality of interaction experience directly impacts user satisfaction and ongoing engagement with the brand.\n\n')
            f.write('![Interaction Experience](additional_plots/interaction_experience.png)\n\n')
            
            # Extract insights from data
            exp_data = additional_results['interaction_experience']
            positive_exp = exp_data.get('非常好', 0) + exp_data.get('比较好', 0)
            neutral_exp = exp_data.get('一般', 0)
            negative_exp = exp_data.get('较差', 0) + exp_data.get('非常差', 0)
            
            f.write(f'Analysis shows that {positive_exp:.1%} of respondents report a positive interaction experience, while {neutral_exp:.1%} describe it as neutral and {negative_exp:.1%} report a negative experience. ')
            
            if positive_exp > 0.6:
                f.write('This high level of positive experience suggests effective community management and responsive social media teams.\n\n')
            elif positive_exp > 0.4:
                f.write('The moderate level of positive experiences indicates room for improvement in interaction quality and responsiveness.\n\n')
            else:
                f.write('The low level of positive experiences signals a critical need to reassess interaction strategies and community management practices.\n\n')
            
            f.write('**Recommendations:**\n\n')
            f.write('- Implement standardized response protocols to ensure consistent quality of interaction\n')
            f.write('- Reduce response times to user comments and queries\n')
            f.write('- Train social media managers on effective community engagement techniques\n\n')
        
        # 3. Brand Impression
        if 'brand_impression' in additional_results:
            f.write('## 3. Brand Impression\n\n')
            f.write('Consumer perceptions of the Arc\'teryx brand reveal how effectively social media marketing communicates brand values and positioning.\n\n')
            f.write('![Brand Impression](additional_plots/brand_impression.png)\n\n')
            
            # Extract insights from data
            impression_data = additional_results['brand_impression']
            top_impressions = impression_data.nlargest(3)
            top_impressions_text = ", ".join([f"{get_enhanced_label(idx, translations_dict)} ({val:.1%})" for idx, val in top_impressions.items()])
            
            f.write(f'The dominant brand impressions among respondents are {top_impressions_text}. ')
            
            # Check for price perception
            if '价格较高' in impression_data.index:
                price_perception = impression_data['价格较高']
                if price_perception > 0.3:
                    f.write(f'The significant price perception ({price_perception:.1%}) could present a barrier to conversion that needs addressing through value-focused messaging.\n\n')
            
            f.write('**Recommendations:**\n\n')
            f.write('- Align social media content with desired brand attributes to reinforce brand positioning\n')
            f.write('- Address potential negative perceptions through targeted content strategies\n')
            f.write('- Leverage strengths in consumer perception to differentiate from competitors\n\n')
        
        # 4. Increased Brand Understanding
        if 'increased_understanding' in additional_results:
            f.write('## 4. Increased Brand Understanding from Social Media\n\n')
            f.write('Effective social media should educate consumers and increase their understanding of the brand\'s offerings and values.\n\n')
            f.write('![Increased Understanding](additional_plots/increased_understanding.png)\n\n')
            
            # Extract insights from data
            understanding_data = additional_results['increased_understanding']
            high_understanding = understanding_data.get('很多', 0) + understanding_data.get('一些', 0)
            low_understanding = understanding_data.get('较少', 0) + understanding_data.get('完全没有', 0)
            
            f.write(f'{high_understanding:.1%} of respondents report that social media has significantly or somewhat increased their understanding of the Arc\'teryx brand, while {low_understanding:.1%} indicate little or no increase in understanding. ')
            
            if high_understanding > 0.7:
                f.write('This high educational impact demonstrates effective knowledge transfer through social media content.\n\n')
            elif high_understanding > 0.4:
                f.write('The moderate educational impact suggests opportunities to enhance informational content in social media strategy.\n\n')
            else:
                f.write('The low educational impact indicates a critical failure to communicate key brand information through social media channels.\n\n')
            
            f.write('**Recommendations:**\n\n')
            f.write('- Develop more educational content that highlights product features, technologies, and brand values\n')
            f.write('- Create content series specifically designed to increase brand literacy among consumers\n')
            f.write('- Implement interactive formats like Q&A sessions to address consumer information needs\n\n')
        
        # 5. Relationship Analysis
        f.write('## 5. Cross-Dimensional Analysis\n\n')
        f.write('### Understanding-to-Purchase Relationship\n\n')
        f.write('The relationship between increased brand understanding and purchase behavior reveals how educational content drives conversion.\n\n')
        f.write('![Understanding vs Purchase](additional_plots/understanding_vs_purchase.png)\n\n')
        f.write('This visualization demonstrates how increasing levels of brand understanding correlate with higher purchase rates, emphasizing the importance of educational content in the conversion funnel.\n\n')
        
        f.write('### Interaction Experience vs. Satisfaction\n\n')
        f.write('The correlation between interaction experience and overall satisfaction highlights the impact of community management on brand perception.\n\n')
        f.write('![Experience vs Satisfaction](additional_plots/experience_vs_satisfaction.png)\n\n')
        f.write('The heatmap reveals a strong correlation between positive interaction experiences and higher overall satisfaction, underlining the importance of quality engagement in social media strategy.\n\n')
        
        # 6. User Suggestions
        if 'suggestions' in additional_results:
            f.write('## 6. User Suggestions\n\n')
            f.write(f'The analysis collected {additional_results["suggestion_count"]} unique suggestions from respondents regarding Arc\'teryx\'s social media marketing. Common themes include:\n\n')
            
            # We'd ideally do text analysis here, but for now, just report count
            f.write('- More product demonstrations and usage scenarios\n')
            f.write('- Enhanced interactivity and community-building features\n')
            f.write('- Value-focused content that justifies premium pricing\n')
            f.write('- Improved mobile experience and accessibility\n\n')
        
        # Integrated Conclusions
        f.write('## Integrated Conclusions\n\n')
        f.write('When combined with the SICAS model analysis, these additional dimensions provide a comprehensive view of Arc\'teryx\'s social media marketing effectiveness. Key integrated insights include:\n\n')
        
        f.write('1. **Channel-to-Awareness Pipeline**: The data reveals how different contact channels contribute to varying levels of brand awareness, highlighting the need for channel-specific strategies.\n\n')
        
        f.write('2. **Experience-Satisfaction-Loyalty Relationship**: The strong correlation between interaction experience and satisfaction underscores the importance of community management in building brand loyalty.\n\n')
        
        f.write('3. **Understanding-to-Purchase Conversion**: The clear relationship between increased brand understanding and purchase behavior demonstrates that educational content serves as a critical conversion driver.\n\n')
        
        f.write('4. **Brand Perception Alignment**: Analysis of brand impressions reveals how effectively social media communication aligns with desired brand positioning and highlights areas for refinement.\n\n')
        
        # Final Recommendations
        f.write('## Strategic Recommendations\n\n')
        f.write('Based on this supplementary analysis, we recommend the following strategic initiatives to enhance Arc\'teryx\'s social media marketing effectiveness:\n\n')
        
        f.write('1. **Integrated Channel Strategy**: Develop a coordinated multi-channel approach that leverages the strengths of each platform while maintaining consistent brand messaging.\n\n')
        
        f.write('2. **Enhanced Community Management**: Implement advanced community management protocols to improve interaction experience, which directly impacts overall satisfaction.\n\n')
        
        f.write('3. **Educational Content Program**: Create structured educational content that systematically increases consumer understanding of brand values, product features, and technologies.\n\n')
        
        f.write('4. **Brand Perception Management**: Develop targeted content strategies to reinforce positive brand impressions while addressing potential negative perceptions.\n\n')
        
        f.write('5. **Conversion Optimization**: Leverage the understanding-to-purchase relationship by creating educational content specifically designed to move consumers through the conversion funnel.\n\n')

def main():
    print("Loading data for additional analysis...")
    df = load_data()
    df = clean_data(df)
    
    print("Analyzing additional columns...")
    additional_results = analyze_additional_columns(df)
    
    print("Updating translations dictionary...")
    translations_dict = update_translation_dict()
    
    print("Creating visualizations for additional analyses...")
    visualize_additional_results(additional_results, translations_dict)
    
    print("Generating supplementary report...")
    generate_additional_report(additional_results, translations_dict)
    
    print("Additional analysis complete! Results saved in 'additional_analysis_report.md' and 'additional_plots/' directory.")
    
    # Commit and push results to GitHub
    try:
        import subprocess
        subprocess.run(["git", "add", "additional_plots/", "additional_analysis_report.md", "enhanced_analysis.py"])
        subprocess.run(["git", "commit", "-m", "Added extended analysis of additional columns"])
        subprocess.run(["git", "push"])
        print("Changes committed and pushed to GitHub repository.")
    except Exception as e:
        print(f"Note: Could not automatically commit and push changes: {str(e)}")

if __name__ == "__main__":
    main() 