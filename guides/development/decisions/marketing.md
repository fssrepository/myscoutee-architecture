# Marketing decisions and product evidence

**Status:** decision framework, not an adopted campaign plan. Marketing is in scope for this repository because it affects positioning, acquisition channels, product feedback and operating cost.

## Current evidence and owner

The product has versioned pitch materials, articles and social posts, and a product statement: a completed, mutually welcomed real-world meeting. Retrospective marketing records describe past content work and the limitations of token/list-price estimates. Those records do not measure campaign reach, conversion, retention or revenue. The source ledger identifies the owners without duplicating copy or media.

## Decision questions

| Decision | Evidence to collect | Avoid claiming |
| --- | --- | --- |
| Audience and positioning | Interviews, use-case demand, landing-page comprehension | That an attractive pitch proves product-market fit |
| Channel choice | Reach, qualified visits, consented sign-ups and cost per qualified action | That impressions alone equal useful acquisition |
| Creative format | Controlled variants, audience fit, production/review time | That a new asset improves conversion without a comparison |
| Product feedback | Onboarding completion, real-world meeting outcomes and reasons for drop-off | That usage volume alone proves the product goal |
| Budget allocation | Incremental spend, attribution uncertainty and opportunity cost | That a token-equivalent estimate is an actual invoice |

A campaign proposal should state audience, promise, channel, hypothesis, budget cap, measurement window, privacy/consent treatment, stop rule and owner. Match the promise to product behavior and current qualification. Product-facing claims should cite an actual release or verified capability; a lab demonstration is not a production feature.

## Example decision record shape

```text
Decision: [one channel or message choice]
Status: proposed | trial | adopted | rejected
Audience and user problem: [...]
Current baseline and source: [...]
Hypothesis and success measure: [...]
Spend and production effort: [...]
Privacy, brand and product-claim review: [...]
Result, uncertainty and next decision: [...]
```

This is a reusable record format, not a request to start a campaign or publish content.

## Reading the advertising numbers

| Term | Practical meaning |
| --- | --- |
| Impression / reach | A display / the platform's estimate of distinct accounts exposed. Neither is a website visit. |
| Click / landing-page view (LPV) | An ad interaction / a platform-reported arrival after the destination loads. Compare both with the site's successful page requests; reporting windows and definitions can differ. |
| Lead / qualified lead | A person who expresses interest / one who also meets the campaign's stated fit and consent criteria. A submitted form is not yet a MyScoutee meeting. |
| Conversion | The action chosen for measurement, such as a consented sign-up or operator enquiry. Specify the event before comparing campaigns. |

| Metric | Full name | Short reading |
| --- | --- | --- |
| CPM | Cost per mille (1,000 impressions) | Ad spend ÷ impressions × 1,000; visibility or reach cost, not visit cost. |
| CPC | Cost per click | Ad spend ÷ counted clicks; specify which click type. |
| CPL | Cost per lead | Ad spend ÷ recorded leads; a qualified lead may cost more. |
| CPV | Cost per view | Ad spend ÷ eligible video views; a view threshold depends on the format. |
| CTR | Click-through rate | Counted clicks ÷ impressions; response to the ad, not site engagement. |
| CVR | Conversion rate | Defined conversions ÷ eligible ad interactions; name the action and denominator. |
| CPA | Cost per action | Ad spend ÷ defined conversions; a lead is only one possible action. |
| CAC | Customer acquisition cost | Total sales and marketing cost ÷ new customers; broader than ad spend. |
| ROAS | Return on ad spend | Attributed conversion value ÷ ad spend; depends on values and attribution. |

These are reporting ratios; some names also denote bidding methods. They do not by themselves describe an invoice or prove incremental impact. Compare campaigns only after fixing the event definition, attribution window, currency and period. [Google Ads glossary](https://support.google.com/google-ads/answer/12851704), [Google's CPM definition](https://support.google.com/google-ads/answer/6310), [Google's CPV definition](https://support.google.com/google-ads/answer/2382888), [Meta Audience Network glossary](https://www.facebook.com/audiencenetwork/resources/glossary).

For MyScoutee, a useful sequence is **exposure → loaded visit → meaningful page interaction → consented sign-up or qualified operator enquiry → completed, mutually welcomed meeting**. Record the cost and drop-off at each step. Ad-platform attribution, browser analytics and server logs answer different questions; use one time zone, campaign ID and measurement window when reconciling them.

## Choosing a channel

These are **campaign hypotheses**, not measured MyScoutee performance rankings. Facebook and Instagram share Meta advertising tools but should be reported by placement and creative. Targeting availability and delivery depend on campaign objective, region, account eligibility and platform policy; the auction can deliver differently even inside an eligible audience.

| Decision | Facebook | Instagram | LinkedIn | YouTube |
| --- | --- | --- | --- | --- |
| Best first hypothesis | Local pilot and community invitation | Visual discovery of the meeting concept | Operator and venue/partner enquiries | Product explanation and familiarity |
| Creative fit | Clear local event or meeting invitation | Short visual story or Reels demonstration | Concrete pilot offer and partner benefit | Short or longer demonstration video |
| Targeting lens | Geography; eligible broad or interest settings | Geography; eligible broad or interest settings | Company, industry, job title and eligible matched audiences | Eligible demographics, interests, in-market/custom segments and placements |
| Check beyond the platform metric | Loaded visit and qualified action, not feed engagement alone | In-app-browser visibility and meaningful action, not a tap alone | Qualified enquiry, not a form fill alone | Later site action, not a video view alone |

Platform references: [Meta auction and delivery](https://about.fb.com/wp-content/uploads/2023/01/Toward_fairness_in_personalized_ads.pdf) and [lead-generation formats](https://about.fb.com/ltam/wp-content/uploads/sites/14/2023/11/LeadGenerationGuide.pdf); [LinkedIn targeting](https://business.linkedin.com/advertise/ads/targeting) and [lead forms](https://business.linkedin.com/advertise/ads/sponsored-content/lead-gen-ads); [Google audience segments](https://support.google.com/google-ads/answer/2497941) and [YouTube video objectives](https://support.google.com/youtube/answer/2375497).

Do not upload member profiles, private affinity data or contact lists for ad targeting without a separate privacy and consent review. Keep channel tests small and comparable; no universal cost-per-lead or platform winner is established by the current evidence.

## Historical Meta measurement: what the separate tool showed

An **owner-supplied private Meta traffic review dated 21 October 2026** compared Meta screenshots, nginx requests and a temporary landing-page diagnostic recorder. The recorder counted visibility and input in Instagram's in-app browser; its data went to an nginx debug log, outside the Java/Mongo product audit. This was a bounded investigation. Only aggregate findings appear here.

On 20-21 October, the review estimated **204 visitors by distinct IP address** (**103 with a Meta click ID**) and counted **464 successful landing-page requests** (**127 with a click ID**). These units cannot be equated: IP counts misestimate people, requests do not prove viewing, and missing click IDs do not prove another source. Among **97 measured Instagram browser opens**, **86 had no recorded input**, **56 were visible for at most one second**, and median visible time was **0.842 seconds**. This raised a traffic-quality question, not proof of bots or fraud. In adjacent three-hour windows around Spain's removal from targeting, Instagram page requests fell from **49 to zero**; the exact timing and cause remain unverified. Meta screenshots covered different periods and had inconsistent counts, so they cannot be reconciled by subtraction.

Check the **quality of arrival** before optimizing cheap clicks or platform-reported landing-page views. Temporary diagnostics need a bounded purpose and retention; routine decisions need privacy-reviewed aggregate events. The ad data do **not** measure gender dynamics. MyScoutee's purpose includes addressing unequal attention and filtering in online dating; the founder describes a path to mutually welcomed real-world meetings. [Pew's U.S. survey](https://www.pewresearch.org/internet/2020/02/06/the-virtues-and-downsides-of-online-dating/) reports different message-volume experiences for men and women. That context does not show this campaign discriminated or the product solved the problem.
