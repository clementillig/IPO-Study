# An IPO, a dataset, and a slightly unconventional question: does notoriety matter?

Tomorrow, Anthropic is expected to go public at a reported valuation of $1.33 trillion.

Is it worth investing?

I obviously can't provide a reliable prediction of how its stock will perform. But rather than rely on speculation, I wanted to look at what happened to recent IPOs and see whether historical data could offer any useful insight.

The first thing I looked at was Jay R. Ritter's IPO statistics, which show that IPO performance is far from uniform. Between 1980 and 2024, the average US IPO first-day return was 18.9%, meaning that a stock offered at $20 would, on average, close its first trading day at approximately $23.78.

Here is where you can find the data including more relevant metrics such as the median : https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf?lang=en

But I am not satisfied with this, the dataset is way too broad, overall averages mask significant differences depending on company characteristics. I want to find a relevant proxy for Anthropic, a simple tech vs. non-tech classification won't be enough as tech companies are very different from each other. I need a database that provides financial data for each individual company that went public. and I found SkyIPO - US IPO Performance Dataset. 

I will narrow down my analysis to companies that went public from 2020 onward, to focus on more recent market trends.

To keep the analysis consistent and manageable, I will focus exclusively on returns at five predefined closing-price horizons provided by SkyIPO: the first trading day, 1 month, 3 months, 6 months, and 1 year. These checkpoints provide a practical overview of post-IPO performance without attempting to capture every price fluctuation in between. Whenever I refer to "all closing returns" throughout this analysis, I mean these five observations.


The full methodology is found in IPO_study.py, here is a quick description of the output files.

**ipo_all :** Complete IPO dataset retrieved from the API, covering the selected period (2020–2026).

**ipo_classification_review :** Full IPO universe with technology classification results (TRUE / FALSE) and the reasons behind each classification.

**ipo_tech_all :** Dataset containing only IPOs classified as technology companies, including available financial and return data.

**ipo_tech_review :** Technology IPO list with company information and a brief description of their business activity.

**ipo_tech_individual_returns :** 	Individual company returns across all available time horizons, from the first trading day to longer-term performance.

**ipo_tech_statistics :** Overall statistical analysis of technology IPO returns, including descriptive statistics, percentiles and performance distribution metrics.

**ipo_tech_yearly :** Year-by-year breakdown of technology IPO performance statistics, allowing comparison across IPO cohorts.

**ipo_tech_performance_thresholds :** Counts and percentages of technology IPOs that never reached a 50% return and remained negative across all observed time horizons.

Unsurprisingly, there isn't really a single credible proxy for Anthropic among those companies. Nevertheless, I wanted to explore another angle that might prove useful when evaluating future IPOs, even if it doesn't provide a direct proxy for Anthropic: Notoriety.

Anthropic is a high-profile company, and I suspect representativeness bias could play a significant role in the enthusiasm surrounding its IPO. It certainly wouldn't be the first time investor expectations were heavily influenced by a company's reputation and perceived potential.

I used a deliberately subjective criterion as a proxy for notoriety: whether I personally knew the company before conducting this study. This is obviously not an objective measure of brand awareness, but it provides a simple starting point for exploring whether recognizable companies exhibit different IPO performance patterns.

So among 195 confirmed tech companies, I know 8 of them, I assume them to be Notorious ones : Airbnb, Doordash, Unity, Snowflake, Reddit, Gitlab, Duolingo, Figma

The return thresholds mentioned below are illustrative benchmarks used to describe the magnitude of observed performance, not mutually exclusive classification criterion. A company may therefore appear in more than one observation.

5 of them have Consistently great performance (+30% minimum) across all time horizons :

-Airbnb
-Doordash
-Unity
-Snowflake
-Reddit

3 of them have Great performance (+30% minimum) initially and eventually drop to negative returns :

-Gitlab
-Duolingo
-Figma

Among the 187 companies I did not personally recognize, here are some of the more interesting findings. The less recognizable companies can also produce some absolutely extraordinary returns, particularly on their first trading day :

6 of them have Consistently Great performance (+50% minimum) across all time horizons :

-Bentley System
-nCino OpCo
-Shift4 Payments
-Affirm Holdings
-Swarmer
-SaverOne 2014 Ltd (First day : 726,47%, 1M : 644,15%, 3M : 666,75%, 6M : 319,69%, 1Y: 393,95%)

6 of them have Great performance (+100% minimum) initially and eventually drop to negative returns :

-zSpace
-Moving iMage Technologies : +700% on the first day
-Ostin Technology Group : +891.50% on the first day
-Jianzhi Education Technology Group : +275% on the first day
-Treasure Global : +345.50% on the first day
-AMTD Digital : +107.82% on the first day, reaching +2,365% at 1M before falling to -17.3% at 1Y

2 of them have Poor Initial performance and eventually recover with great performance (+100% minimum):

-ARM Holding PLC /UK
-Mega Fortune Co Ltd

112 of them (59,89%) have a Consistently low performance (never reach +50% at any checkpoint)

35 of them (18,72%) have a Consistently negative performance (always below 0%)

Among these 187 companies, 112 (59.89%) never reached a 50% return at any of my five closing-price checkpoints. This does not mean that they never traded above that level intraday, as my analysis is based exclusively on closing returns. Nevertheless, it illustrates how difficult it can be to achieve substantial returns from IPOs, even when the target is a 50% gain rather than a more modest return.

So, what about Anthropic ?

I don't think Anthropic is necessarily comparable to the companies in my personally recognized sample. Its market positioning, valuation, and the broader AI environment introduce factors that my dataset cannot capture.

If the AI sector is experiencing a bubble, historical IPO returns won't tell us when it will burst.

Nevertheless, my analysis raises an interesting question: could investor familiarity and brand recognition play a role in IPO performance? My small sample suggests that this possibility deserves further investigation.

Eight companies are obviously not enough to establish a statistically meaningful relationship, and personal recognition is far from an objective measure of notoriety. But the pattern was interesting enough that I didn't want to dismiss it outright.






