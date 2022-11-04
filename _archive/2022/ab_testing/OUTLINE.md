# How To Support A/B Testing In Your Python Code

If you build a software application, whether that’s a website, desktop app or a mobile app, you need to take a lot of decisions about how your user, your customer is going to use your app. If you just take those decisions based on what you think will work, you’re basically flying blind because you don’t know what the user actually prefers and you risk that your users are going to leave because your app doesn’t deliver. Because of that, it’s common practice to do A/B tests. There are two ingredients you need in your code to support this. I’ll cover both of them today and I’ll also show you how to incorporate them in your code while keeping your software design clean.

I’m also going to show you a few platforms that can be helpful. This video is not sponsored by any of the platforms that I’m going to show you. They have not been involved in the production of this video whatsoever, I’ll be using these platforms purely as illustration.

Before running A/B tests it’s a good idea to go through your code and try to improve the design so that it’s easier to switch between different setups. But how do you actually detect design issues in your code? I have a free Code Diagnosis workshop that teaches you a Three Factor Framework that contains the main areas you should focus on. It’s based on my own experience reviews tons of code and trying to make that process more efficient and more effective. Go to [arjan.codes/diagnosis](http://arjan.codes/diagnosis) to enroll. The link is also in the description of this video.

## Explain the example (screencast)

In order to show how to setup A/B tests, I’m going to use a simple text editor example today. It’s called Worsepad. It’s like Notepad, but worse. (explain and run the code - `simple_feature_flag.py`)

## What are A/B tests?

What is an A/B test? A/B testing (also called bucket testing or split testing) is a way to compare two versions of a single variable. You typically test a subject’s response to variant A versus variant B, in order to determine which of the two variants is more effective.

A/B testing is a common practice in user experience research. Companies like Google, Meta, Twitter, are running experiments with their users all the time. Enabling and disabling certain features, layouts, text changes, etc. and then measuring the response of the user. These can range from switching to a whole different user interface for a subset of users to really minor things like changing the wording of a marketing text or the text or the icon on a button. Often, you may not even notice that you’ve been part of an experiment, you’ve just seen something different than the regular users, and then your actions are being recorded and analyzed.

## A/B tests and privacy

Is that legal? You’ll commonly see pretty broad phrases in privacy statements on websites about what data can be collected about you while you’re browsing that website. Browsers nowadays have code that can block this kind of tracking. With desktop applications though, this is a lot harder since these are standalone. In that case, you’re protected by the privacy laws of your country. Which may not really protect you at all. And not all companies are upfront about what they’re doing with your data and it’s not always easy to find out on your own.

If you’re in the EU, there’s the GDPR which is one of the strictest privacy controls out there. Customers should be able to opt out of systems that track their actions and collect data about them, they should be able to see what data is stored about them as well as request erasing this data.

In short, if you’re doing A/B tests, make sure to ask permission. If you don’t, you might get into legal trouble. But mostly, it’s just the right thing to do.

In order for your code to support A/B tests, you need two things. One, you need a mechanism to provide either the A or B variety. And two, you need to define KPIs, key performance indicators, and a mechanism to record them so you can compare.

## Feature flags (screencast)

A common mechanism to provide the A and B varieties is by using feature flags. With feature flags, you can enable or disable certain pieces of code. Let’s take a look at how to incorporate a feature flag in our example program.

- Show a basic feature flag (`simple_feature_flag.py`)
- Show reading feature flag from a config file (`from_config` folder)

## Feature flags and continuous integration

I really like using feature flags, and they’re not just useful for running A/B tests. If you’re using continuous integration as a development process, then you can use a feature flag to hide a feature that you’re still working on. So the code is actually already published, but the feature is not active yet. You can then activate the feature by simply switching on the feature flag. In essence, you decouple the release from the deployment.

In the example I just showed you, the feature flag setting was part of the code, or part of a config file. If you want to have more control over opening up features to your users, you need to store feature flag settings outside of your code so you can change their values without having to deploy a new version of your code. You can do that in your own database. If you want to go all in though, you can also use a “feature flag as a service” platform. Some example platforms are LaunchDarkly, GrowthBook, or Flagship. They generally offer some sort of web-based interface that allows you to define feature flags, enable or disable them, you can only enable them for certain types of users (for example, users enrolled in a beta program), you can do phased rollouts and slowly enable the feature over time for more users. On some platforms you can also do measurements of how the feature is being used. Let’s take a look at Growthbook as an example.

## Growthbook (screencast)

- Create a feature flag in Growthbook
- Adapt the code to retrieve the feature flag setting (see `with_tracking` example)

## Mixpanel (screencast)

Growthbook supports running experiments with features. But I thought it might be nice to show you an alternative platform which is quite popular called Mixpanel.

- Briefly show the Mixpanel web interface
- Adapt the code to send usage information to Mixpanel (see `with_tracking` example)
- Show the result in the Mixpanel analytics dashboard

## Final thoughts

I hope you enjoyed this overview of how to add feature flags and A/B testing to your application. If you did, give this video a like and consider subscribing to my channel. You might also be interested in this video (Pulumi video) that shows you how to deploy your application to the cloud using a approach called infrastructure-as-code. Thanks for watching, take care, and see you soon.
