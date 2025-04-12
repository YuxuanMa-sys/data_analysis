import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from sicas_analysis import load_data, clean_data, analyze_sicas, get_translated_label, perform_demographic_analysis

# Create enhanced plots directory
if not os.path.exists('thesis_plots'):
    os.makedirs('thesis_plots')

# Set custom color palette for consistency
ARCTERYX_COLORS = ["#2E6E91", "#5CA2C3", "#9CCFE8", "#F0C53F", "#E58723", "#E63946", "#8D99AE", "#57A773"]
sns.set_palette(ARCTERYX_COLORS)

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

def set_thesis_style():
    """Set up a professional style for thesis-quality plots"""
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Custom styling for thesis-quality plots
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['axes.titlesize'] = 16
    mpl.rcParams['axes.labelsize'] = 14
    mpl.rcParams['xtick.labelsize'] = 12
    mpl.rcParams['ytick.labelsize'] = 12
    mpl.rcParams['legend.fontsize'] = 12
    mpl.rcParams['figure.titlesize'] = 20
    mpl.rcParams['figure.figsize'] = (10, 6)
    mpl.rcParams['figure.dpi'] = 300
    
    # Ensure high-quality output
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['savefig.format'] = 'png'
    mpl.rcParams['savefig.bbox'] = 'tight'
    mpl.rcParams['savefig.pad_inches'] = 0.1

def create_pie_charts(results, demographics):
    """Create pie charts for key proportions"""
    
    # Generate pie charts for demographic data
    for key, data in demographics.items():
        if not data.empty:
            plt.figure(figsize=(10, 8))
            
            # Translate labels
            translated_index = [get_translated_label(label) for label in data.index]
            translated_series = pd.Series(data.values, index=translated_index)
            
            # Only include top categories if too many slices
            if len(translated_series) > 7:
                # Keep top 6, group others
                top_categories = translated_series.nlargest(6)
                others_sum = translated_series.iloc[6:].sum()
                if others_sum > 0:
                    top_categories['Others'] = others_sum
                translated_series = top_categories
            
            # Draw pie chart with enhanced styling
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
                title="Categories",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            # Add title and styling
            plt.title(f'Distribution of {key.capitalize()}', fontsize=18, pad=20)
            plt.tight_layout()
            plt.savefig(f'thesis_plots/pie_{key}.png')
            plt.close()
    
    # Create pie charts for key SICAS components
    key_components = {
        'sense': 'awareness',
        'action': 'purchase',
        'share': 'satisfaction'
    }
    
    for component, key in key_components.items():
        if key in results[component] and not results[component][key].empty:
            plt.figure(figsize=(10, 8))
            
            # Translate labels
            data = results[component][key]
            translated_index = [get_translated_label(label) for label in data.index]
            translated_series = pd.Series(data.values, index=translated_index)
            
            # Draw pie chart with enhanced styling
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
                title=f"{component.capitalize()} - {key.capitalize()}",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            # Add title and styling
            plt.title(f'{component.capitalize()} - {key.capitalize()} Distribution', fontsize=18, pad=20)
            plt.tight_layout()
            plt.savefig(f'thesis_plots/pie_{component}_{key}.png')
            plt.close()

def create_radar_chart(results):
    """Create a radar chart for SICAS model comparison"""
    
    # Extract key metrics for the radar chart
    metrics = {
        'Brand Awareness': results['sense']['awareness'].get('非常了解', 0) + results['sense']['awareness'].get('略有了解', 0),
        'Content Attraction': results['interest']['attraction'].get('非常吸引', 0) + results['interest']['attraction'].get('比较吸引', 0),
        'Social Interaction': results['communication']['interaction'].get('经常互动(点赞、评论、分享等)', 0) + results['communication']['interaction'].get('偶尔互动', 0),
        'Purchase Conversion': results['action']['purchase'].get('是', 0),
        'User Satisfaction': results['share']['satisfaction'].get('非常满意', 0) + results['share']['satisfaction'].get('比较满意', 0)
    }
    
    # Prepare data for radar chart
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    # Number of variables
    N = len(categories)
    
    # Create angle values (in radians)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    
    # Make the plot close
    values += values[:1]
    angles += angles[:1]
    categories += categories[:1]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories[:-1], fontsize=14)
    
    # Draw the chart
    ax.plot(angles, values, linewidth=2, linestyle='solid', color=ARCTERYX_COLORS[0])
    ax.fill(angles, values, alpha=0.25, color=ARCTERYX_COLORS[0])
    
    # Set y-axis limits
    ax.set_ylim(0, 1)
    
    # Add grid lines and styling
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add value labels at each point
    for angle, value, category in zip(angles, values, categories):
        if category == categories[0]:  # Skip the duplicated point
            continue
        ax.text(angle, value + 0.05, f'{value:.2f}', 
                horizontalalignment='center', 
                verticalalignment='center',
                fontsize=12, fontweight='bold')
    
    # Add title
    plt.title('SICAS Model Performance Overview', size=20, pad=20)
    
    # Save the chart
    plt.tight_layout()
    plt.savefig('thesis_plots/radar_sicas_overview.png')
    plt.close()

def create_heatmap(df):
    """Create correlation heatmap between key variables"""
    
    # Encode categorical variables for correlation analysis
    encoded_df = pd.DataFrame()
    
    # Map key categorical variables to numerical values
    # Brand awareness
    awareness_col = '您是否了解始祖鸟（Arc\'teryx）品牌？'
    if awareness_col in df.columns:
        awareness_map = {
            '非常了解': 4, 
            '略有了解': 3, 
            '不太了解': 2, 
            '完全不了解': 1
        }
        encoded_df['Brand_Awareness'] = df[awareness_col].map(awareness_map)
    
    # Content attraction
    interest_col = '始祖鸟的社交媒体内容对您的吸引力如何?'
    if interest_col in df.columns:
        interest_map = {
            '非常吸引': 5,
            '比较吸引': 4,
            '一般': 3,
            '不太吸引': 2,
            '完全不吸引': 1
        }
        encoded_df['Content_Attraction'] = df[interest_col].map(interest_map)
    
    # Interaction
    interaction_col = '您是否曾与始祖鸟的社交媒体账号互动?'
    if interaction_col in df.columns:
        interaction_map = {
            '经常互动(点赞、评论、分享等)': 4,
            '偶尔互动': 3,
            '很少互动': 2,
            '从未互动': 1
        }
        encoded_df['Interaction_Level'] = df[interaction_col].map(interaction_map)
    
    # Purchase
    purchase_col = '您是否因社交媒体内容购买过始祖鸟产品？'
    if purchase_col in df.columns:
        purchase_map = {'是': 1, '否': 0}
        encoded_df['Purchase'] = df[purchase_col].map(purchase_map)
    
    # Satisfaction
    satisfaction_col = '您对始祖鸟社交媒体的整体满意度如何？'
    if satisfaction_col in df.columns:
        satisfaction_map = {
            '非常满意': 5,
            '比较满意': 4,
            '一般': 3,
            '不太满意': 2,
            '很不满意': 1
        }
        encoded_df['Satisfaction'] = df[satisfaction_col].map(satisfaction_map)
    
    # Create correlation matrix
    corr_matrix = encoded_df.corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    # Draw heatmap
    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmax=1,
        vmin=-1,
        center=0,
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": .5},
        annot=True,
        fmt=".2f"
    )
    
    plt.title('Correlation Between SICAS Components', fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig('thesis_plots/heatmap_sicas_correlation.png')
    plt.close()

def create_grouped_bar_charts(results, demographics):
    """Create grouped bar charts to show relationships between demographics and SICAS metrics"""
    
    # Load full dataset for cross-analysis
    df = load_data()
    df = clean_data(df)
    
    # Example: Gender vs Brand Awareness
    gender_col = '您的性别'
    awareness_col = '您是否了解始祖鸟（Arc\'teryx）品牌？'
    
    if gender_col in df.columns and awareness_col in df.columns:
        # Create cross-tabulation
        cross_tab = pd.crosstab(
            df[gender_col], 
            df[awareness_col], 
            normalize='index'
        )
        
        # Translate for plotting
        cross_tab.index = [get_translated_label(idx) for idx in cross_tab.index]
        cross_tab.columns = [get_translated_label(col) for col in cross_tab.columns]
        
        # Plot
        plt.figure(figsize=(12, 7))
        cross_tab.plot(
            kind='bar',
            stacked=False,
            color=ARCTERYX_COLORS[:len(cross_tab.columns)],
            ax=plt.gca()
        )
        
        plt.title('Brand Awareness by Gender', fontsize=18, pad=20)
        plt.xlabel('Gender', fontsize=14)
        plt.ylabel('Proportion', fontsize=14)
        plt.xticks(rotation=0)
        plt.legend(title='Awareness Level', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('thesis_plots/grouped_gender_awareness.png')
        plt.close()
    
    # Example: Age vs Purchase Rate
    age_col = '您的年龄'
    purchase_col = '您是否因社交媒体内容购买过始祖鸟产品？'
    
    if age_col in df.columns and purchase_col in df.columns:
        # Create cross-tabulation
        cross_tab = pd.crosstab(
            df[age_col], 
            df[purchase_col], 
            normalize='index'
        )
        
        # Translate for plotting
        cross_tab.index = [get_translated_label(idx) for idx in cross_tab.index]
        cross_tab.columns = [get_translated_label(col) for col in cross_tab.columns]
        
        # Order age groups logically
        age_order = ['18-25', '26-35', '36-45', '46+']
        cross_tab = cross_tab.reindex(age_order)
        
        # Plot
        plt.figure(figsize=(12, 7))
        cross_tab.plot(
            kind='bar',
            stacked=True,
            color=[ARCTERYX_COLORS[5], ARCTERYX_COLORS[2]],
            ax=plt.gca()
        )
        
        plt.title('Purchase Rate by Age Group', fontsize=18, pad=20)
        plt.xlabel('Age Group', fontsize=14)
        plt.ylabel('Proportion', fontsize=14)
        plt.xticks(rotation=0)
        plt.legend(title='Purchase', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add percentage labels
        for i, p in enumerate(plt.gca().patches):
            if i < len(age_order):  # Only label the "Yes" proportion
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
        plt.savefig('thesis_plots/stacked_age_purchase.png')
        plt.close()

def generate_sicas_conclusions(results, demographics):
    """Generate research conclusions based on SICAS analysis"""
    
    conclusions = []
    
    # Brand Awareness (Sense) Conclusions
    awareness_data = results['sense']['awareness']
    high_awareness = awareness_data.get('非常了解', 0) + awareness_data.get('略有了解', 0)
    
    if high_awareness > 0.6:
        conclusions.append("**Brand Awareness:** Arc'teryx enjoys high brand recognition, with over {:.1f}% of respondents indicating they are familiar with the brand. This strong awareness foundation provides an excellent starting point for marketing initiatives.".format(high_awareness*100))
    elif high_awareness > 0.3:
        conclusions.append("**Brand Awareness:** Arc'teryx has moderate brand recognition, with {:.1f}% of respondents familiar with the brand. This suggests opportunities for increasing brand visibility in the market.".format(high_awareness*100))
    else:
        conclusions.append("**Brand Awareness:** Arc'teryx has relatively low brand recognition ({:.1f}%), indicating a significant need for awareness-building campaigns.".format(high_awareness*100))
    
    # Interest Conclusions
    interest_data = results['interest']['attraction']
    high_interest = interest_data.get('非常吸引', 0) + interest_data.get('比较吸引', 0)
    
    if high_interest > 0.6:
        conclusions.append("**Content Attraction:** The brand's social media content effectively captures audience interest, with {:.1f}% finding it attractive. This demonstrates strong content strategy alignment with audience preferences.".format(high_interest*100))
    elif high_interest > 0.3:
        conclusions.append("**Content Attraction:** {:.1f}% of respondents find Arc'teryx's social media content attractive, suggesting room for enhancing content appeal to better engage the audience.".format(high_interest*100))
    else:
        conclusions.append("**Content Attraction:** Only {:.1f}% of respondents find the social media content attractive, highlighting a critical need to revise content strategy to better align with audience preferences.".format(high_interest*100))
    
    # Communication Conclusions
    interaction_data = results['communication']['interaction']
    active_interaction = interaction_data.get('经常互动(点赞、评论、分享等)', 0) + interaction_data.get('偶尔互动', 0) + interaction_data.get('很少互动', 0)
    
    if active_interaction > 0.5:
        conclusions.append("**User Interaction:** With {:.1f}% of respondents engaging with Arc'teryx social media in some capacity, the brand has established an interactive relationship with its audience, demonstrating effective two-way communication.".format(active_interaction*100))
    else:
        conclusions.append("**User Interaction:** The majority of respondents ({:.1f}%) report never interacting with Arc'teryx social media, indicating a significant gap in audience engagement that needs addressing.".format((1-active_interaction)*100))
    
    # Purchase Behavior (Action) Conclusions
    purchase_data = results['action']['purchase']
    purchase_rate = purchase_data.get('是', 0)
    
    if purchase_rate > 0.3:
        conclusions.append("**Purchase Conversion:** The {:.1f}% conversion rate from social media to purchases represents a strong return on investment for Arc'teryx's social media marketing efforts, exceeding industry benchmarks.".format(purchase_rate*100))
    elif purchase_rate > 0.1:
        conclusions.append("**Purchase Conversion:** The {:.1f}% social media-driven purchase rate aligns with industry standards but presents opportunities for optimization through improved call-to-action strategies and streamlined purchasing pathways.".format(purchase_rate*100))
    else:
        conclusions.append("**Purchase Conversion:** With only {:.1f}% of respondents making purchases based on social media content, there exists a significant disconnect between engagement and conversion that requires strategic intervention.".format(purchase_rate*100))
    
    # Satisfaction Conclusions
    satisfaction_data = results['share']['satisfaction']
    high_satisfaction = satisfaction_data.get('非常满意', 0) + satisfaction_data.get('比较满意', 0)
    
    if high_satisfaction > 0.7:
        conclusions.append("**User Satisfaction:** The remarkably high satisfaction rate ({:.1f}%) demonstrates exceptional social media content quality and audience alignment, creating strong potential for advocacy and word-of-mouth marketing.".format(high_satisfaction*100))
    elif high_satisfaction > 0.4:
        conclusions.append("**User Satisfaction:** {:.1f}% of users report satisfaction with Arc'teryx's social media, indicating generally positive reception but with room for enhancement to reach excellence.".format(high_satisfaction*100))
    else:
        conclusions.append("**User Satisfaction:** The satisfaction rate of {:.1f}% suggests significant issues with social media content strategy that require comprehensive reassessment to better meet audience expectations.".format(high_satisfaction*100))
    
    # Demographic Insights
    if 'gender' in demographics:
        gender_data = demographics['gender']
        majority_gender = gender_data.idxmax()
        majority_gender_pct = gender_data.max()
        
        conclusions.append("**Demographic Insight:** The customer base shows a {:.1f}% representation of {} respondents, suggesting targeted content strategies could be developed to either strengthen appeal to this dominant demographic or to expand reach among underrepresented groups.".format(
            majority_gender_pct*100, 
            get_translated_label(majority_gender).lower()
        ))
    
    if 'age' in demographics:
        age_data = demographics['age']
        # Find top two age groups
        top_ages = age_data.nlargest(2)
        
        conclusions.append("**Age Distribution:** The majority of respondents fall within the {} ({:.1f}%) and {} ({:.1f}%) age brackets, indicating these segments should be prioritized in content strategy while considering approaches to engage other age demographics.".format(
            get_translated_label(top_ages.index[0]),
            top_ages.iloc[0]*100,
            get_translated_label(top_ages.index[1]),
            top_ages.iloc[1]*100
        ))
    
    # Improvement Recommendations
    if 'improvements' in results['share']:
        improvement_data = results['share']['improvements']
        top_improvements = improvement_data.nlargest(3)
        
        improvement_list = ", ".join(["{} ({:.1f}%)".format(
            get_translated_label(idx), val*100
        ) for idx, val in top_improvements.items()])
        
        conclusions.append("**Priority Improvements:** Based on user feedback, the most critical areas for improvement are: {}. These insights should guide immediate refinements to Arc'teryx's social media strategy.".format(improvement_list))
    
    # Overall SICAS Funnel Analysis
    # Calculate drop-off at each stage
    awareness = high_awareness
    interest = high_interest
    communication = active_interaction
    action = purchase_rate
    satisfaction = high_satisfaction
    
    # Find largest drop-off
    transitions = [
        ("awareness-interest", awareness - interest),
        ("interest-communication", interest - communication),
        ("communication-action", communication - action),
        ("action-satisfaction", action - satisfaction if action > satisfaction else 0)
    ]
    
    largest_drop = max(transitions, key=lambda x: x[1])
    
    if largest_drop[1] > 0.2:
        if largest_drop[0] == "awareness-interest":
            conclusions.append("**Funnel Analysis:** The most significant drop-off occurs between awareness and interest ({:.1f}% decrease), indicating that while many consumers know the brand, the content fails to capture their interest. Content strategy should be revised to better align with the interests of brand-aware consumers.".format(largest_drop[1]*100))
        elif largest_drop[0] == "interest-communication":
            conclusions.append("**Funnel Analysis:** Despite generating interest, there's a substantial {:.1f}% decrease in active communication, suggesting barriers to engagement that should be addressed through more interactive content formats and stronger calls-to-action.".format(largest_drop[1]*100))
        elif largest_drop[0] == "communication-action":
            conclusions.append("**Funnel Analysis:** The {:.1f}% drop between interaction and purchase represents a critical conversion gap. This indicates potential issues with product pricing, availability, or purchase pathway that should be strategically addressed.".format(largest_drop[1]*100))
        elif largest_drop[0] == "action-satisfaction":
            conclusions.append("**Funnel Analysis:** The {:.1f}% decline from purchase to satisfaction suggests post-purchase disappointment that could damage brand reputation. Aligning marketing messaging more closely with product reality and improving customer experience should be prioritized.".format(largest_drop[1]*100))
    
    # Final comprehensive conclusion
    overall_performance = np.mean([awareness, interest, communication, action, satisfaction])
    
    if overall_performance > 0.6:
        conclusions.append("**Overall SICAS Performance:** Arc'teryx demonstrates strong social media marketing effectiveness with above-average performance across the SICAS model, particularly in {}. The brand should maintain its successful strategies while addressing the identified gap in the {} transition to further optimize marketing ROI.".format(
            "brand awareness and user satisfaction" if (awareness + satisfaction)/2 > overall_performance else "content interest and engagement",
            largest_drop[0].replace("-", " to ")
        ))
    elif overall_performance > 0.3:
        conclusions.append("**Overall SICAS Performance:** Arc'teryx shows moderate effectiveness in social media marketing with varied performance across the SICAS framework. The brand should prioritize improving the {} stage and addressing the significant drop-off between {} to enhance overall marketing effectiveness.".format(
            min([("awareness", awareness), ("interest", interest), ("communication", communication), ("action", action), ("satisfaction", satisfaction)], key=lambda x: x[1])[0],
            largest_drop[0].replace("-", " and ")
        ))
    else:
        conclusions.append("**Overall SICAS Performance:** Arc'teryx faces significant challenges in social media marketing effectiveness with below-average performance across the SICAS model. A comprehensive strategy overhaul is recommended, starting with {} and systematically addressing each stage of the customer journey.".format(
            min([("awareness", awareness), ("interest", interest), ("communication", communication), ("action", action), ("satisfaction", satisfaction)], key=lambda x: x[1])[0]
        ))
    
    return conclusions

def generate_enhanced_report(results, demographics, conclusions):
    """Generate an enhanced report for thesis use"""
    
    with open('thesis_report.md', 'w', encoding='utf-8') as f:
        f.write('# Arc\'teryx Social Media Marketing Effectiveness Analysis\n\n')
        f.write('## Using the SICAS Model Framework\n\n')
        
        # Executive Summary
        f.write('## Executive Summary\n\n')
        f.write('This analysis examines Arc\'teryx\'s social media marketing effectiveness through the SICAS (Sense-Interest-Communication-Action-Share) framework, based on survey data from consumers. The findings reveal insights into brand awareness, content engagement, interaction patterns, purchase conversion, and overall satisfaction with the brand\'s social media presence.\n\n')
        
        # Key Findings - Conclusions
        f.write('## Key Findings\n\n')
        for conclusion in conclusions:
            f.write(f'- {conclusion}\n\n')
        
        # Visualization Gallery
        f.write('## Visualization Gallery\n\n')
        
        # SICAS Overview - Radar Chart
        f.write('### SICAS Model Overview\n\n')
        f.write('![SICAS Radar Overview](thesis_plots/radar_sicas_overview.png)\n\n')
        f.write('*Figure 1: Radar chart visualizing performance across all SICAS dimensions, showing the relative strengths and weaknesses in Arc\'teryx\'s social media marketing funnel.*\n\n')
        
        # Correlation Heatmap
        f.write('### Component Correlations\n\n')
        f.write('![SICAS Correlation Heatmap](thesis_plots/heatmap_sicas_correlation.png)\n\n')
        f.write('*Figure 2: Correlation heatmap showing relationships between different SICAS components, revealing how each stage influences subsequent stages in the marketing funnel.*\n\n')
        
        # Demographic Insights
        f.write('### Demographic Analysis\n\n')
        
        # Gender distribution
        f.write('#### Gender Distribution\n\n')
        f.write('![Gender Distribution](thesis_plots/pie_gender.png)\n\n')
        f.write('*Figure 3: Gender distribution of survey respondents.*\n\n')
        
        # Age distribution
        f.write('#### Age Distribution\n\n')
        f.write('![Age Distribution](thesis_plots/pie_age.png)\n\n')
        f.write('*Figure 4: Age distribution of survey respondents.*\n\n')
        
        # Cross-Analysis
        f.write('### Cross-Demographic Analysis\n\n')
        
        # Gender vs Awareness
        f.write('#### Gender vs. Brand Awareness\n\n')
        f.write('![Gender vs Brand Awareness](thesis_plots/grouped_gender_awareness.png)\n\n')
        f.write('*Figure 5: Brand awareness levels across different gender groups, showing variation in brand recognition between demographics.*\n\n')
        
        # Age vs Purchase
        f.write('#### Age vs. Purchase Behavior\n\n')
        f.write('![Age vs Purchase](thesis_plots/stacked_age_purchase.png)\n\n')
        f.write('*Figure 6: Purchase conversion rates across age groups, highlighting which demographics are most likely to convert from social media engagement to product purchase.*\n\n')
        
        # Individual SICAS Components
        f.write('## SICAS Component Analysis\n\n')
        
        # Sense - Brand Awareness
        f.write('### Sense (Brand Awareness)\n\n')
        f.write('![Brand Awareness](thesis_plots/pie_sense_awareness.png)\n\n')
        f.write('*Figure 7: Distribution of brand awareness levels among respondents.*\n\n')
        
        # Interest - Content Attraction
        f.write('### Interest (Content Attraction)\n\n')
        f.write('![Content Attraction](plots/interest_attraction.png)\n\n')
        f.write('*Figure 8: Respondents\' ratings of how attractive they find Arc\'teryx\'s social media content.*\n\n')
        
        # Action - Purchase
        f.write('### Action (Purchase Conversion)\n\n')
        f.write('![Purchase Conversion](thesis_plots/pie_action_purchase.png)\n\n')
        f.write('*Figure 9: Proportion of respondents who have made purchases based on Arc\'teryx\'s social media content.*\n\n')
        
        # Satisfaction
        f.write('### Share (User Satisfaction)\n\n')
        f.write('![User Satisfaction](thesis_plots/pie_share_satisfaction.png)\n\n')
        f.write('*Figure 10: Overall satisfaction levels with Arc\'teryx\'s social media presence.*\n\n')
        
        # Methodological Notes
        f.write('## Methodological Notes\n\n')
        f.write('This analysis employs the SICAS model to evaluate social media marketing effectiveness through five key dimensions: Sense (awareness), Interest (attraction), Communication (interaction), Action (purchase), and Share (satisfaction). Data was collected through a comprehensive consumer survey with responses from various demographic groups.\n\n')
        f.write('The analysis utilizes multiple visualization techniques to reveal patterns and insights, including pie charts, radar charts, heatmaps, and grouped bar charts. Statistical correlations between SICAS components were calculated to identify relationships between different stages of the consumer journey.\n\n')
        
        # Recommendations
        f.write('## Strategic Recommendations\n\n')
        f.write('Based on the comprehensive analysis of Arc\'teryx\'s social media marketing effectiveness, the following strategic recommendations are proposed:\n\n')
        
        # Add recommendations based on findings
        if 'awareness' in results['sense']:
            awareness_data = results['sense']['awareness']
            high_awareness = awareness_data.get('非常了解', 0) + awareness_data.get('略有了解', 0)
            
            if high_awareness < 0.6:
                f.write('1. **Enhance Brand Visibility**: Implement targeted advertising campaigns and collaborative partnerships with outdoor influencers to increase brand recognition, particularly among the identified demographic segments with lower awareness.\n\n')
            else:
                f.write('1. **Leverage Strong Brand Recognition**: Capitalize on high brand awareness by focusing on differentiation messaging that reinforces Arc\'teryx\'s unique value proposition compared to competitors.\n\n')
        
        if 'attraction' in results['interest']:
            interest_data = results['interest']['attraction']
            high_interest = interest_data.get('非常吸引', 0) + interest_data.get('比较吸引', 0)
            
            if high_interest < 0.6:
                f.write('2. **Content Strategy Revision**: Develop more engaging content formats based on audience preferences, emphasizing authentic storytelling, user-generated content, and educational material about outdoor activities.\n\n')
            else:
                f.write('2. **Refine Content Excellence**: Continue to enhance the already effective content strategy by introducing more innovative formats while maintaining the successful elements that are attracting audience interest.\n\n')
        
        if 'interaction' in results['communication']:
            interaction_data = results['communication']['interaction']
            active_interaction = interaction_data.get('经常互动(点赞、评论、分享等)', 0) + interaction_data.get('偶尔互动', 0)
            
            if active_interaction < 0.5:
                f.write('3. **Boost Audience Engagement**: Create more interactive content formats such as polls, contests, Q&A sessions, and interactive stories to encourage active participation rather than passive consumption.\n\n')
            else:
                f.write('3. **Nurture Community Interaction**: Build upon the existing engagement by developing a structured community management strategy that rewards participation and creates opportunities for deeper brand relationships.\n\n')
        
        if 'purchase' in results['action']:
            purchase_data = results['action']['purchase']
            purchase_rate = purchase_data.get('是', 0)
            
            if purchase_rate < 0.2:
                f.write('4. **Optimize Conversion Pathways**: Address the significant gap between engagement and purchase by simplifying the buying journey, implementing strategic calls-to-action, and developing social commerce capabilities.\n\n')
            else:
                f.write('4. **Enhance Purchase Experience**: Streamline the already successful conversion process and implement loyalty-building initiatives to encourage repeat purchases and maximize lifetime customer value.\n\n')
        
        if 'barriers' in results['action']:
            barriers_data = results['action']['barriers']
            price_barrier = barriers_data.get('价格过高', 0)
            
            if price_barrier > 0.3:
                f.write('5. **Address Price Perception**: Develop targeted content that emphasizes product value, durability, and long-term benefits to justify the premium pricing and overcome the significant price barrier identified in the research.\n\n')
        
        f.write('6. **Demographic-Specific Strategies**: Develop tailored content approaches for different demographic segments based on the cross-analysis findings, with particular attention to age groups showing the highest potential for conversion improvement.\n\n')
        
        # Conclusion
        f.write('## Conclusion\n\n')
        f.write('The SICAS model analysis provides a structured framework for evaluating and enhancing Arc\'teryx\'s social media marketing effectiveness. By addressing the identified gaps in the consumer journey and building on existing strengths, the brand can optimize its social media strategy to better achieve marketing objectives and drive business results.\n\n')
        f.write('This research demonstrates the value of a systematic approach to social media marketing analysis and provides actionable insights that can inform strategic decision-making. Future research could expand on these findings with longitudinal studies to track changes in effectiveness over time and competitive benchmarking to contextualize performance within the outdoor apparel industry.\n\n')

def main():
    """Main function to run enhanced analysis"""
    
    # Set the style for thesis-quality plots
    set_thesis_style()
    
    # Load and analyze data using the existing functions
    print("Loading data...")
    df = load_data()
    
    print("Cleaning data...")
    df = clean_data(df)
    
    print("Analyzing SICAS components...")
    sicas_results = analyze_sicas(df)
    
    print("Performing demographic analysis...")
    demographics = perform_demographic_analysis(df)
    
    # Create enhanced visualizations
    print("Creating pie charts...")
    create_pie_charts(sicas_results, demographics)
    
    print("Creating radar chart...")
    create_radar_chart(sicas_results)
    
    print("Creating correlation heatmap...")
    create_heatmap(df)
    
    print("Creating grouped bar charts...")
    create_grouped_bar_charts(sicas_results, demographics)
    
    # Generate research conclusions
    print("Generating research conclusions...")
    conclusions = generate_sicas_conclusions(sicas_results, demographics)
    
    # Generate enhanced report
    print("Generating enhanced thesis report...")
    generate_enhanced_report(sicas_results, demographics, conclusions)
    
    print("Enhanced analysis complete! Results saved in 'thesis_report.md' and 'thesis_plots/' directory.")

if __name__ == "__main__":
    main() 