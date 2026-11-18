# IPO-Study

A study from Jay R. Ritter, professor of finance at the University of Florida shows the distribution of returns is often highly asymmetrical: a few initial public offerings deliver exceptional performance, while a significant proportion underperform the market.

However there is a particularly interesting phenomenon in IPOs: underpricing.
Historically, between 1980 and 2024, the average return between the offering price and the first-day closing price in the United States has been 18.9%. This means that, on average, a company that goes public at $20 ends its first day of trading at approximately $23.78.

Here is where you can find the data including more relevant metrics such as the median : https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf?lang=en

But I am not satisfied with this, the dataset is way too broad, overall averages mask significant differences depending on company characteristics. I want to find a relevant proxy for Anthropic, a mere tech against non tech classification won't be enough as tech companies are very differents from each other. I need a database that provides financial data for each individual company that went public. and I found SkyIPO – US IPO Performance Dataset. 

I will narrow down my analysis to companies that went public as early as 2020 early as I want to highlight recent market trends.

The full methodology is found in IPO_study.py, here is a quick description of the output files.

**ipo_all :** Complete IPO dataset retrieved from the API, covering the selected period (2020–2026).

**ipo_classification_review :** Full IPO universe with technology classification results (TRUE / FALSE) and the reasons behind each classification.

**ipo_tech_all :** Dataset containing only IPOs classified as technology companies, including available financial and return data.

**ipo_tech_review :** Technology IPO list with company information and a brief description of their business activity.

**ipo_tech_individual_returns :** 	Individual company returns across all available time horizons, from the first trading day to longer-term performance.

**ipo_tech_statistics :** Overall statistical analysis of technology IPO returns, including descriptive statistics, percentiles and performance distribution metrics.

**ipo_tech_yearly :** Year-by-year breakdown of technology IPO performance statistics, allowing comparison across IPO cohorts.

**ipo_tech_performance_thresholds :** Counts and percentages of technology IPOs that never reached a 50% return and remained negative across all observed time horizons.



