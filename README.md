# An IPO, a dataset, and a slightly unconventional question: does notoriety matter?

Tomorrow, Anthropic is expected to go public at a reported valuation of $1.33 trillion.

Is it worth investing?

I obviously can't provide a reliable prediction of how its stock will perform. But rather than rely on speculation, I wanted to look at what happened to recent IPOs and see whether historical data could offer any useful insight.

The first thing I looked at was Jay R. Ritter's IPO statistics, which show that IPO performance is far from uniform. Between 1980 and 2024, the average US IPO first-day return was 18.9%, meaning that a stock offered at $20 would, on average, close its first trading day at approximately $23.78.


Here is where you can find the data including more relevant metrics such as the median : https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf?lang=en

But I am not satisfied with this, the dataset is way too broad, overall averages mask significant differences depending on company characteristics. I want to find a relevant proxy for Anthropic, a mere tech against non tech classification won't be enough as tech companies are very differents from each other. I need a database that provides financial data for each individual company that went public. and I found SkyIPO – US IPO Performance Dataset. 

I will narrow down my analysis to companies that went public as early as 2020 early as I want to highlight recent market trends. We will also only analyze the returns at closure at the following time horizons as those are those provided by SkyIPO : 
-First-day return
-Return 1M
-Return 3M
-Return 6M
-Return 1Y

In the following when I will mention "All closure returns" I will mean only those 5 ones. Rather than calculate a percentage of daily returns that were above or below a range. I think it's simpler for decision making purposes to assume that those 5 are enough to consider that the variations of the companies will stay within a reasonable range rather than considering each individual outlier. As if we go that way to always get more precision, we would eventually need to use a rigorously peer reviewed mathematical model for stock picking, which is not a necessity in practice even among institutional investors, otherwise Finance would be a solved case. So let's save ourselves some trouble and make the powerful assumption that those 6 returns accurately describe the variations of our stock prices.

The full methodology is found in IPO_study.py, here is a quick description of the output files.

**ipo_all :** Complete IPO dataset retrieved from the API, covering the selected period (2020–2026).

**ipo_classification_review :** Full IPO universe with technology classification results (TRUE / FALSE) and the reasons behind each classification.

**ipo_tech_all :** Dataset containing only IPOs classified as technology companies, including available financial and return data.

**ipo_tech_review :** Technology IPO list with company information and a brief description of their business activity.

**ipo_tech_individual_returns :** 	Individual company returns across all available time horizons, from the first trading day to longer-term performance.

**ipo_tech_statistics :** Overall statistical analysis of technology IPO returns, including descriptive statistics, percentiles and performance distribution metrics.

**ipo_tech_yearly :** Year-by-year breakdown of technology IPO performance statistics, allowing comparison across IPO cohorts.

**ipo_tech_performance_thresholds :** Counts and percentages of technology IPOs that never reached a 50% return and remained negative across all observed time horizons.

Unsurprisingly, there isn't really a single credible proxy for Anthropic among those companies. Nevertheless, we can fallback to another criteria that will actually provide a strong basis to decide to invest in IPOs in the future not on the same scale but of the same nature : based on Notoriety.

Most people who will invest in Anthropic will do so solely for Representativeness bias as it is a high profile company, and it is not the only one.

I will classify companies with a purely subjective method : Did I hear about them or not ?

So among 195 confirmed tech companies, I know 8 of them, I assume them to be Notorious ones : Airbnb, Doordash, Unity, Snowflake, Reddit, Gitlab, Duolingo, Figma

5 of them have Consistantly great performance (+30% minimum) across all time horizons :

-Airbnb
-Doordash
-Unity
-Snowflake
-Reddit

3 of them have Great performance (+30% minimum) initially and eventually drop to negative returns :

-Gitlab
-Duolingo
-Figma

Among the remaining 187 Non Notorious companies : 

6 of them have Consistantly Great performance (+50% minimum) across all time horizons :

-Bentley System
-nCino OpCo
-Shift4 Payments
-Affirm Holdings
-Swarmer
-SaverOne 2014 Ltd (1st day : 726,47%, 1M : 644,15%, 3M : 666,75%, 6M : 319,69%, 1Y: 393,95%)

6 of them have Great performance (+100% minimum) initially and eventually drop to negative returns :

-zSpace
-Moving iMage Technologies (1st day : 700%)
-Jianzhi Education Technology Group (1st day : 275%)
-Treasure Global (1st day : 345,50%)
-AMTD Digital (1st day : 107,82%, 1M : 2365%, 3M : 500%, 6M : 28.21%, 1Y : -17,3%)
-Ostin Technology Group (1st day : 891,50%)

2 of them have Bad Initial performance and eventually recover with great performance (+100% minimum) :

-ARM Holding PLC /UK
-Mega Fortune Co Ltd

112 of them (59,89%) have a Consistantly low performance (never reach +50%)

35 of them (18,72%) have a Consistantly negative performance (always below 0%)

**So, what about Anthropic ?**

I don't think Anthropic is necessarily comparable to the companies in my personally recognized sample. Its market positioning, valuation, and the broader AI environment introduce factors that my dataset cannot capture.

If the AI sector is experiencing a bubble, historical IPO returns won't tell us when it will burst.

Nevertheless, my analysis raises an interesting question: could investor familiarity and brand recognition play a role in IPO performance? My small sample suggests that this possibility deserves further investigation.

Eight companies are obviously not enough to establish a statistically meaningful relationship, and personal recognition is far from an objective measure of notoriety. But the pattern was interesting enough that I didn't want to dismiss it outright.




