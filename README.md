# IPO-Study

A study from Jay R. Ritter, professor of finance at the University of Florida shows the distribution of returns is often highly asymmetrical: a few initial public offerings deliver exceptional performance, while a significant proportion underperform the market.

However there is a particularly interesting phenomenon in IPOs: underpricing.
Historically, between 1980 and 2024, the average return between the offering price and the first-day closing price in the United States has been 18.9%. This means that, on average, a company that goes public at $20 ends its first day of trading at approximately $23.78.

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

My conclusion is that 59,89% of Non Notorious tech companies going public don't reach 50% returns at a one year time horizon since 2020. While the 50% returns might seem to be an excessive target, it is perfectly reasonable in the sense that it's a maximum.... that wasn't reached, and you won't sell at max when you're in the midst of action because you have no way of knowing when you're at max meaning, the exact moment you should sell. The return you can reasonably expect from a stock that never reach 50% is much less. Remind yourself that 18.72% of the stocks never make a positive closure across a one year horizon, the actual risk of selling at a loss is much higher. 

People invest in non notorious companies IPO anyway because the rare occurence to which it works out it can reach tremendous values like 500% returns (21 000% for AMTD Digital, considering intraday returns rather than only closures).

Meanwhile, the Notorious companies have 8 out of 8 times at minimum a return at closure of 30% if you sell on first quotation day. Emphasis on 8 times, while it's not statistically significant, my humble opinion is that if you simply dismiss the notion that this number could mean something, you might be too reliant on your book smarts to not miss out on several opportunities. To me this is a signal of both safety and great returns.

So what about Anthropic ? I don't think it fits with the other Notorious companies, there was no talk of a Doordash or Airbnb buble. But if there is indeed an AI buble, we won't know until the day it burst, and that day may very well be tomorrow.



