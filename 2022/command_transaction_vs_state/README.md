# Intro (talking head)

Last week, I talked about the Command pattern and show you how you can use it to store transactions. If you haven't watched that, I've put a link in the description. This week, I'm going to show you how you can take this idea to the next level by changing what data you store. This is not always what you want to do, but in some cases, it's an extremely powerful approach.

That choice is a software design decision. My goal with this channel is to help you with improving the way you make those decisions. Help you recognize patterns that will then hopefully lead you to a better design in the end. I've written a guide that provides you with a starting point. And it's free, go to arjancodes.com/designguide to get your code. It contains the 7 steps that I follow myself when I design a piece of software, and I hope it helps you too to make better design decisions. Arjancodes.com/designguide, the link is also in the description.

Before we dive into this upgraded version of the command pattern, let's do a brief recap of last week's example.

# Explain the example briefly (screencast)

# Transactions vs state (talking head)

When you think about what data is stored in the example, we have on the one hand a bank and accounts and the other thing that is stored is transactions in order to undo/redo things. The problem with this approach is that it's hard to get a list of transactions. If you want to see your bank statement and see what transactions have been processed in the past, the current approach doesn't support this. A simple way to solve this is to also maintain a list of transactions that have been executed. But that's also not ideal. For one, it's another thing to keep track of, and you need to update it whenever you undo/redo transactions. A second issue is that it introduces redundancy. If you know the list of transactions, you can compute the balance. But there's also a balance field in each Account. Which one is the correct one? What's the ground truth? The list of transactions, or the account balance value?

In the current example, the account balance is clear the ground truth, because we don't store past transactions apart from in the undo list, which may very well be deleted once you logout of your banking app. The other way to do it is that the transactions are the ground truth. This completely changes things. In particular, it has a huge effect on the undo/redo mechanism, which in fact becomes completely trivial. There are a few things to watch out for though. Let's modify the example and see what happens when we turn transactions into the ground truth.

# Modify the example to be transaction-based (screencast)

- Create a ledger of transactions and keep track of the current pointer
- Undo and redo become trivially simple
- If you add a transaction, delete anything after the current pointer
- Rename account.balance to balance_cache.
- Add a clear_cache method to both account and bank
- Add a compute_balances to the bank controller.

# Final thoughts

Transaction-based systems are more common than you think. Not just banking works in this way, lots on non-destructive editing tools also work in this fashion. For example, Final Cut Pro doesn't change the original video files you use to produce a video. It applies transformations on those video files similar to the transactions in our example. Final Cut then creates a cache to make viewing and editing the video faster. Logic Pro, an audio editing tool, does the same thing, except for audio the caching needs are a bit less extreme than for Final Cut. Even most 3D modeling tools use this for lighting, hair animation, and so on. You apply and edit all the effects you like, and then you render it to create the final result. Rendering here is equivalent to computing the balance caches in the accounts. There are even often different rendering systems in place: a lower-quality one, but faster, for editing, a fullblown rendering for movie exports, and things in-between, like baking textures, which generates textures that include the edits that you applied to it, and then you use that again to continue your non-destructive editing.

The takeaway is this. If you're designing a piece of software, don't forget about the possibility of storing the transactions instead of the state. Let me know in the comments if you've used this kind of approach before and what your experience is with it.

I hope you enjoyed this video, thanks for watching and see you next time!
