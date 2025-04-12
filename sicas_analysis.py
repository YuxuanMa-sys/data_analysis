import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

# Create plots directory at the beginning
if not os.path.exists('plots'):
    os.makedirs('plots')

# Simplified approach to handle Chinese characters - use translated labels
def get_translated_label(chinese_label):
    """Create simplified English labels for Chinese categories"""
    translations = {
        # Brand awareness (sense)
        '非常了解': 'Very Familiar',
        '略有了解': 'Somewhat Familiar',
        '不太了解': 'Not Very Familiar',
        '完全不了解': 'Not Familiar At All',
        
        # Attraction (interest)
        '非常吸引': 'Very Attractive',
        '比较吸引': 'Fairly Attractive',
        '一般': 'Neutral',
        '不太吸引': 'Not Very Attractive',
        '完全不吸引': 'Not Attractive At All',
        
        # Interaction (communication)
        '经常互动(点赞、评论、分享等)': 'Frequent Interaction',
        '偶尔互动': 'Occasional Interaction',
        '很少互动': 'Rare Interaction',
        '从未互动': 'No Interaction',
        
        # Interaction types
        '点赞': 'Like',
        '评论': 'Comment',
        '分享到个人社交圈': 'Share',
        '参与话题活动': 'Topic Activities',
        '私信交流': 'Private Messages',
        '观看直播': 'Watch Livestreams',
        '其他': 'Other',
        '无': 'None',
        
        # Purchase (action)
        '是': 'Yes',
        '否': 'No',
        
        # Satisfaction (share)
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
        '其他': 'Other',
        
        # Demographics - Gender
        '男': 'Male',
        '女': 'Female',
        
        # Demographics - Age
        '18-25岁': '18-25',
        '26-35岁': '26-35',
        '36-45岁': '36-45',
        '46岁及以上': '46+',
        '18岁以下': 'Under 18',
        
        # Demographics - Occupation
        '政府机关工作人员': 'Gov. Employee',
        '企业职员': 'Corporate Employee',
        '自由职业者': 'Freelancer',
        '学生': 'Student',
        '其他': 'Other',
        
        # Demographics - Income
        '3000元以下': '<3000 RMB',
        '3000-8000元': '3000-8000 RMB',
        '8000-15000元': '8000-15000 RMB',
        '15000元以上': '>15000 RMB',
        
        # Demographics - Social Media Usage
        '少于1小时': '<1 Hour',
        '1-3小时': '1-3 Hours',
        '3-5小时': '3-5 Hours',
        '5小时以上': '>5 Hours',
        
        # Brand contact channels 
        '微信公众号': 'WeChat Official Account',
        '微博': 'Weibo',
        '小红书': 'Xiaohongshu',
        '抖音/快手': 'TikTok/Kuaishou',
        '品牌官网': 'Brand Website',
        '朋友推荐': 'Friend Recommendation',
        '线下店铺': 'Offline Store',
        '社交媒体广告': 'Social Media Ads',
        '第三方平台': 'Third-party Platform',
        'bilibili': 'Bilibili',
        '得物': 'Dewu',
        
        # Brand impression
        '高端户外品牌': 'High-end Outdoor Brand',
        '专业性强': 'Professional',
        '价格较高': 'High Price',
        '环保可持续': 'Eco-friendly',
        '产品设计时尚': 'Stylish Design',
        '广告／宣传设计时尚': 'Stylish Advertising',
        '普通品牌': 'Ordinary Brand',
        '装逼': 'Show-off Brand',

        # Brand understanding increase
        '很多': 'Significant Increase',
        '一些': 'Some Increase',
        '较少': 'Little Increase',
        '完全没有': 'No Increase',
        
        # Purchase channels
        '官方电商平台': 'Official E-commerce',
        '第三方电商平台（如天猫、京东）': 'Third-party E-commerce',
        '线下专卖店': 'Offline Store',
        '朋友代购': 'Friend Purchase',
        '社交媒体平台链接／小程序': 'Social Media Link',
        
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
    
    # Return the translation if available, otherwise return the original
    return translations.get(chinese_label, chinese_label)

# SICAS Model Components:
# S - Sense (Awareness/Attention)
# I - Interest
# C - Communication/Connection
# A - Action (Purchase)
# S - Share/Satisfaction

# Load the data
def load_data(file_path='data.csv'):
    # Handle potential encoding issues with Chinese characters
    encodings = ['utf-8', 'gbk', 'gb18030', 'utf-16', 'cp936', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            print(f"Trying encoding: {encoding}")
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully loaded with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with encoding {encoding}: {str(e)}")
            continue
    
    # If all encodings fail, try a more permissive approach
    try:
        print("Trying fallback with errors='replace'")
        df = pd.read_csv(file_path, encoding='utf-8', errors='replace')
        return df
    except Exception as e:
        print(f"Fatal error: Unable to load CSV file: {str(e)}")
        raise

def clean_data(df):
    # Clean column names - removing question numbers and special characters
    columns = df.columns.tolist()
    clean_columns = []
    
    for col in columns:
        # Remove question numbers like "1、"
        if '、' in col:
            clean_col = col.split('、', 1)[1]
        else:
            clean_col = col
        
        # Remove trailing colons
        if clean_col.endswith('：'):
            clean_col = clean_col[:-1]
        
        clean_columns.append(clean_col)
    
    df.columns = clean_columns
    return df

def analyze_sicas(df):
    # Initialize results dictionary
    results = {
        'sense': {},
        'interest': {},
        'communication': {},
        'action': {},
        'share': {}
    }
    
    # S - Sense (Brand Awareness)
    awareness_col = '您是否了解始祖鸟（Arc\'teryx）品牌？'
    if awareness_col in df.columns:
        results['sense']['awareness'] = df[awareness_col].value_counts(normalize=True)
    
    # I - Interest
    interest_col = '始祖鸟的社交媒体内容对您的吸引力如何?'
    if interest_col in df.columns:
        results['interest']['attraction'] = df[interest_col].value_counts(normalize=True)
    
    # C - Communication
    interaction_col = '您是否曾与始祖鸟的社交媒体账号互动?'
    if interaction_col in df.columns:
        results['communication']['interaction'] = df[interaction_col].value_counts(normalize=True)
    
    interaction_type_col = '您更倾向于哪种互动方式？（可多选）'
    if interaction_type_col in df.columns:
        # For multi-select questions, count occurrences of each option
        interaction_types = []
        for response in df[interaction_type_col].dropna():
            types = response.split('┋')
            interaction_types.extend(types)
        
        results['communication']['interaction_types'] = pd.Series(interaction_types).value_counts(normalize=True)
    
    # A - Action (Purchase)
    purchase_col = '您是否因社交媒体内容购买过始祖鸟产品？'
    if purchase_col in df.columns:
        results['action']['purchase'] = df[purchase_col].value_counts(normalize=True)
    
    # Additional purchase channels analysis
    channel_col = '您最常通过以下哪种途径购买？（可多选）'
    if channel_col in df.columns and '(跳过)' not in df[channel_col].unique():
        channels = []
        for response in df[channel_col].dropna():
            if response != '(跳过)':
                types = response.split('┋')
                channels.extend(types)
        
        results['action']['channels'] = pd.Series(channels).value_counts(normalize=True)
    
    # Purchase barriers
    barrier_col = '阻碍您购买的原因是什么？（可多选）'
    if barrier_col in df.columns and '(跳过)' not in df[barrier_col].unique():
        barriers = []
        for response in df[barrier_col].dropna():
            if response != '(跳过)':
                types = response.split('┋')
                barriers.extend(types)
        
        results['action']['barriers'] = pd.Series(barriers).value_counts(normalize=True)
    
    # S - Share/Satisfaction
    satisfaction_col = '您对始祖鸟社交媒体的整体满意度如何？'
    if satisfaction_col in df.columns:
        results['share']['satisfaction'] = df[satisfaction_col].value_counts(normalize=True)
    
    improvement_col = '您认为始祖鸟社交媒体内容有哪些需要改进的地方？（可多选）'
    if improvement_col in df.columns:
        improvements = []
        for response in df[improvement_col].dropna():
            types = response.split('┋')
            improvements.extend(types)
        
        results['share']['improvements'] = pd.Series(improvements).value_counts(normalize=True)
    
    return results

def visualize_sicas(results):
    # Set style
    sns.set(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # Plot for each SICAS component
    for component, data in results.items():
        for key, value in data.items():
            if not value.empty:
                plt.figure(figsize=(10, 6))
                
                # Translate Chinese labels to English for plotting
                translated_index = [get_translated_label(label) for label in value.index]
                translated_series = pd.Series(value.values, index=translated_index)
                
                ax = translated_series.plot(kind='bar', color='skyblue')
                plt.title(f'{component.capitalize()} - {key.capitalize()}', fontsize=14)
                plt.ylabel('Proportion', fontsize=12)
                plt.xticks(rotation=45, ha='right', fontsize=10)
                
                # Add value labels
                for i, v in enumerate(translated_series):
                    ax.text(i, v + 0.01, f'{v:.2f}', ha='center', fontsize=10)
                
                plt.tight_layout()
                plt.savefig(f'plots/{component}_{key}.png', dpi=300)  # Higher DPI for better quality
                plt.close()

def perform_demographic_analysis(df):
    # Analyze demographic information
    demographics = {}
    
    # Gender distribution
    gender_col = '您的性别'
    if gender_col in df.columns:
        demographics['gender'] = df[gender_col].value_counts(normalize=True)
    
    # Age distribution
    age_col = '您的年龄'
    if age_col in df.columns:
        demographics['age'] = df[age_col].value_counts(normalize=True)
    
    # Occupation distribution
    occupation_col = '您的职业'
    if occupation_col in df.columns:
        demographics['occupation'] = df[occupation_col].value_counts(normalize=True)
    
    # Income distribution
    income_col = '您的月收入（人民币）'
    if income_col in df.columns:
        demographics['income'] = df[income_col].value_counts(normalize=True)
    
    # Social media usage
    usage_col = '您每天使用社交媒体的时长大约是多少？'
    if usage_col in df.columns:
        demographics['social_media_usage'] = df[usage_col].value_counts(normalize=True)
    
    # Visualize demographics
    for key, value in demographics.items():
        if not value.empty:
            plt.figure(figsize=(10, 6))
            
            # Translate Chinese labels to English for plotting
            translated_index = [get_translated_label(label) for label in value.index]
            translated_series = pd.Series(value.values, index=translated_index)
            
            ax = translated_series.plot(kind='bar', color='lightgreen')
            plt.title(f'Demographic - {key.capitalize()}', fontsize=14)
            plt.ylabel('Proportion', fontsize=12)
            plt.xticks(rotation=45, ha='right', fontsize=10)
            
            # Add value labels
            for i, v in enumerate(translated_series):
                ax.text(i, v + 0.01, f'{v:.2f}', ha='center', fontsize=10)
            
            plt.tight_layout()
            plt.savefig(f'plots/demographic_{key}.png', dpi=300)  # Higher DPI for better quality
            plt.close()
    
    return demographics

def generate_sicas_funnel(results):
    # Create SICAS funnel visualization
    funnel_data = []
    
    # Sense - Brand awareness (using "非常了解" + "略有了解")
    if 'awareness' in results['sense']:
        aware_rate = results['sense']['awareness'].get('非常了解', 0) + results['sense']['awareness'].get('略有了解', 0)
        funnel_data.append(('Sense\n(Awareness)', aware_rate))
    
    # Interest - Content attraction (using "非常吸引" + "比较吸引")
    if 'attraction' in results['interest']:
        interest_rate = results['interest']['attraction'].get('非常吸引', 0) + results['interest']['attraction'].get('比较吸引', 0)
        funnel_data.append(('Interest', interest_rate))
    
    # Communication - Interaction (using "经常互动" + "偶尔互动" + "很少互动")
    if 'interaction' in results['communication']:
        comm_rate = results['communication']['interaction'].get('经常互动(点赞、评论、分享等)', 0) + \
                   results['communication']['interaction'].get('偶尔互动', 0) + \
                   results['communication']['interaction'].get('很少互动', 0)
        funnel_data.append(('Communication', comm_rate))
    
    # Action - Purchase rate
    if 'purchase' in results['action']:
        action_rate = results['action']['purchase'].get('是', 0)
        funnel_data.append(('Action\n(Purchase)', action_rate))
    
    # Share - Satisfaction (using "非常满意" + "比较满意")
    if 'satisfaction' in results['share']:
        share_rate = results['share']['satisfaction'].get('非常满意', 0) + results['share']['satisfaction'].get('比较满意', 0)
        funnel_data.append(('Share/\nSatisfaction', share_rate))
    
    # Plot funnel
    if funnel_data:
        stages, values = zip(*funnel_data)
        plt.figure(figsize=(10, 6))
        plt.bar(stages, values, color=['#f9d5e5', '#eeac99', '#e06377', '#c83349', '#5b9aa0'])
        plt.ylim(0, 1)
        plt.title('SICAS Model Funnel', fontsize=14)
        plt.ylabel('Proportion', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels
        for i, v in enumerate(values):
            plt.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('plots/sicas_funnel.png', dpi=300)  # Higher DPI for better quality
        plt.close()

def generate_report(results, demographics):
    with open('sicas_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write('# Arc\'teryx (始祖鸟) Social Media Marketing Analysis Report\n\n')
        f.write('## SICAS Model Analysis\n\n')
        
        # Write SICAS components
        for component, data in results.items():
            f.write(f'### {component.capitalize()}\n\n')
            for key, value in data.items():
                f.write(f'#### {key.capitalize()}\n\n')
                f.write('```\n')
                f.write(str(value))
                f.write('\n```\n\n')
                f.write(f'![{component}_{key}](plots/{component}_{key}.png)\n\n')
        
        # Write demographics
        f.write('## Demographic Analysis\n\n')
        for key, value in demographics.items():
            f.write(f'### {key.capitalize()}\n\n')
            f.write('```\n')
            f.write(str(value))
            f.write('\n```\n\n')
            f.write(f'![demographic_{key}](plots/demographic_{key}.png)\n\n')
        
        # Write SICAS funnel
        f.write('## SICAS Funnel\n\n')
        f.write('![sicas_funnel](plots/sicas_funnel.png)\n\n')
        
        # Write recommendations
        f.write('## Recommendations\n\n')
        
        # Sense recommendations
        f.write('### Improving Brand Awareness\n\n')
        f.write('- Consider expanding social media presence on platforms with high user engagement\n')
        f.write('- Develop targeted content that highlights the unique features of Arc\'teryx products\n')
        f.write('- Collaborate with outdoor influencers and communities to increase brand visibility\n\n')
        
        # Interest recommendations
        f.write('### Enhancing Content Interest\n\n')
        f.write('- Create more interactive and engaging content formats\n')
        f.write('- Showcase real customer experiences and testimonials\n')
        f.write('- Develop educational content about outdoor activities and equipment usage\n\n')
        
        # Communication recommendations
        f.write('### Improving User Interaction\n\n')
        f.write('- Implement more interactive features in social media posts\n')
        f.write('- Respond promptly to user comments and messages\n')
        f.write('- Host live events, Q&A sessions, and contests to encourage participation\n\n')
        
        # Action recommendations
        f.write('### Driving Purchase Decisions\n\n')
        f.write('- Address price concerns by highlighting product durability and value\n')
        f.write('- Provide clear information about product features and benefits\n')
        f.write('- Create exclusive social media promotions and discounts\n\n')
        
        # Share recommendations
        f.write('### Enhancing User Satisfaction and Sharing\n\n')
        f.write('- Encourage users to share their experiences with Arc\'teryx products\n')
        f.write('- Create shareable content formats like challenges and user-generated content campaigns\n')
        f.write('- Reward and recognize users who engage with and share brand content\n\n')

def main():
    print("Loading data...")
    df = load_data()
    
    print("Cleaning data...")
    df = clean_data(df)
    
    print("Analyzing SICAS components...")
    sicas_results = analyze_sicas(df)
    
    print("Performing demographic analysis...")
    demographics = perform_demographic_analysis(df)
    
    print("Visualizing SICAS components...")
    visualize_sicas(sicas_results)
    
    print("Generating SICAS funnel...")
    generate_sicas_funnel(sicas_results)
    
    print("Generating report...")
    generate_report(sicas_results, demographics)
    
    print("Analysis complete! Results saved in 'sicas_analysis_report.md' and 'plots/' directory.")

if __name__ == "__main__":
    main() 