- You haven’t seen me use Jupyter notebooks on the channel yet. Well, that’s changing now!
- I’ll go through a couple of examples today showing you when Jupyter notebooks are a great solution. But I’ll also show you what can go wrong and when it makes sense to write plain old Python scripts like a caveman.
- Now, let’s take a closer look at Jupyter notebooks and what you can do with them.

### What are Jupyter notebooks?

- _Show a JupyterLab screen_
- Jupyter gets its name from its ability to run a lot of different languages. It can run \***\*Ju\*\***lia code, **\*\***Pyt**\*\***hon code, and **R** (should that be \***\*eR\*\***?) code, giving us JuPyt(e)R, or just Jupyter.
  ************\*\*\*\*************Highlight JuPyteR on the screen, maybe overlay the planet Jupiter on the screen************\*\*\*\*************
- What’s great about Jupyter is that it allows you to explore your code, and make decisions based on the output. It also allows you to document the decisions that you made. This is why they’re very popular for data scientists, who often need to spend time exploring their data before knowing what to build.
- You can run Jupyter in a web-based interface, but there’s also a VSCode extension that I’ll use in this video. So let’s take a look at a more complete example.

### Jupyter notebooks in VSCode

- ****\*\*****Load nb1_ufo_overview.ipynb**
  First section deals with structure of notebooks, not directly pros or cons\* - Let’s start off by looking at a dataset of UFO sightings, which we got from the Data Science site [Kaggle.com](http://Kaggle.com) (link in the description)
  \*\*\***Show**\*** https://static.wikia.nocookie.net/babylon5/images/4/4c/Shadow-battlecrab.jpg/revision/latest?cb=20080502211130 - A Jupyter notebook is built out of cells, and these cells come in three main varieties: - Markdown (input) cells - Code (input) cells - And output cells - For example, you can see that we have already created a title and subtitle in Markdown, and now it is rendered. By double clicking, we can see the underlying markdown code
  **\***Double click on the title, and show the underlying Markdown. Hit <Shift-Enter> to re-render**\*** - In an input cell, we can press `<shift + enter>` to execute the cell. The number on the left tells us the order the cells have been executed. - JUDGEMENT CALL: There are a bunch of keyboard shortcuts I use to make editing in Jupyter easier, but they may be distracting. Even if you don’t go through them, they will be helpful to you when doing live coding, so I’ll list them here
          | Mode | Key | What it does |
          | --- | --- | --- |
          | Input | Esc | Enters command mode |
          | Command | a | Adds a cell above current cell |
          | Command | b | Adds a cell below current cell |
          | Command | dd (ie d twice) | Deletes current cell |
          | Command  | m | Makes current cell a Markdown cell |
          | Command | y | Makes current cell a code cell |
          | Command | enter | Return to input mode |
          | Input | shift + enter | Execute current cell |
      - PRO: WE CAN EASILY CHECK THE OUTPUT
      Here we have some code that reads in the CSV and does some formatting on it. What you need to do here will vary with the data you find, and how much processing it already has, so we are not going to dwell on it too much. One of the nice things we do get is pretty formatting of data frames. The last line, `ufo_df.head()` , displays a data frame and allows us quick inspection.
      **********************Execute the second code cell**********************
          - This can be really useful to see what type of data you have, and whether you have applied all the needed processing steps.
      - PRO: WE CAN WRITE COMMENTARY ON OUR FINDINGS TO SHARE WITH OTHERS
      PRO: WHILE PROGRAMMING, WE CAN FIND OTHER DIRECTIONS TO EXPLORE
          - Jupyter makes viewing plots of data really simple and easy to share. Let’s see if UFO sightings are increasing or not:
          ****************Execute the third code cell under ********************Are UFO Sightings increasing or decreasing?*********************
              - We can see overall that the sightings are increasing, and can leave a note to that effect.
              - We can also see there are short “wiggles” in the data, so maybe there are seasonal effects. Aliens like the summer maybe? This gives us an idea of something else we might want to investigate, but that we might not have thought of when we started out.
              - We can also notice that UFO sightings increased rapidly around the year 2000. So lots of questions being raised that we could dig into.
              - This is one of the primary advantages of Jupyter notebooks — as you are doing your exploration you can uncover interesting questions that would have been hard to anticipate and design around from the start.
          - *Scroll down to **Where are the UFO sighting hotspots?***
          - For this exercise, we are going to leave the questions raised in this graph, and instead try to figure out where the best place to see a UFO is. Notice that our original data had the longitude and latitude in it, so we can directly plot it and try to get an idea.
          ************Execute input cell 4 and get a map.************
              - Here we see a lot of sightings from North America, India, and Oceania. But with so many points it is hardest to say which the ****best**** spot is.
              - We can get a list of countries
              Run cell 5
              or even display graphically
              Run cell 6
              - Don’t use Pie Charts! Really only the first line of this code is necessary to see the pattern, the rest of the code is here to tidy up the formatting of the chart.
          - We can see the *******country******* with the most sightings is the US, but the US is also large. If we wanted to maximize our chances of seeing a UFO, we want to know the number of sightings per area. So let’s write some code to do that.
              - Now, we are going to simplify a little bit, by looking at the density per square degree of latitude and longitude. It isn’t perfect, because  the distances get warped as we move toward the poles. It also doesn’t account for the wraparound near of latitude near the poles, or of longitude near the dateline, but those areas don’t have many sightings anyway.
              - Write simplified function `num_rows_in_window`
              - Now we can apply this function to all sites in the dataframe
              - Note that this function takes ~ 5 mins to run, so cut away until it is done
              - Now that the function is done, we can execute our last line and get a summary of where the most sightings occur
- Show Arjan talking to camera
  Now this is all great. But, notebooks also introduce some serious problems. Let’s take a look at another example.
- ****\*\*****Load nb2_dice.ipynb****\*\*****
  (Overview)
  This example is going to start in a pretty similar way. We are interested in programming a game that involves rolling dice, like Dungeons and Dragons. We want to know if we can create a die roller, so we can create one like the one we see here
  ********************\*\*********************Show the first three cells, which has N_SIDES=6 and `roll_n_dice` defined already\*
  - Like in our UFO example, we can quickly visualize results. If you are an avid boardgamer, you probably know the most likely outcome of rolling two d6s is 7 — but by how much? We can easily visualize this in a notebook
    _Execute cell 4_
  - CON: ITERATIVE DEVELOPMENT ENCOURAGES IMMEDIATE FEEDBACK
    - In this example, lets say that we were interested in comparing rolling 20 d6s vs 6 d20s. Other than it being a pain to roll 20 dice, is there really that much of a difference in outcome? Getting the results for rolling 20 d6s is easy
      _Execute cell 5_
      In a script, we would have to start over and run again as we add more code, so we might take this as an opportunity to change our function. In the notebook, it is tempting to just override the variable N_SIDES to 20, as we get immediate feedback.
      ******\*\*******Execute cell 6******\*\*******
    - It is better to place these results on the same graph to compare them
      _Execute cell 7_
    - We have really quickly (and easily) been able to tell there really is a difference beyond just how annoying rolling 20 dice would be. Rolling 20 d6s leads to higher results, and less spread (your statistics professor would probably tell you something about the central limit theorem … whatever that is). But are able to tell people they cannot swap d20s for d6s and expect the “same game”.
    - So what is the problem. Notice what happens if we go back and rerun cell 5
      _Execute cell 5 again, making it cell 8_
    - When this cell runs, we still have `N_SIDES=20`, but reading the notebook suggests that `N_SIDES=6`
    - In more complicated examples, it might not even be obvious that you that an error has been made.
  - CON: EVEN ITERATIVE DEVELOPMENT USING FUNCTIONS IS HARD TO REASON ABOUT
    - The takeaway is that we should not have modified a global variable, but instead included the number of sides as an argument to `roll_n_dice` . Because most dice are 6-sided, we can provide that as the default
    - Provide the code
    ```jsx
    def roll_n_dice(n_dice: int, n_sides: int=6) -> int:
        """Rolls n_dice dice, each die has n_sides, and returns the total"""
        rolls = [random.randint(1, n_sides) for _ in range(n_dice)]
        return sum(rolls)
    ```
    - Now our code for generating distributions is not dependent on global state
    ```python
    outcomes_roll_20_six_sided_dice = [
        roll_n_dice(n_dice=20, n_sides=6) for _ in range(10000)
    ]
    outcomes_roll_6_twenty_sided_dice = [
        roll_n_dice(n_dice=6, n_sides=20) for _ in range(10000)
    ]

    sns.histplot(outcomes_roll_6_twenty_sided_dice, binwidth=1, label="6 twenty-sided die")
    sns.histplot(outcomes_roll_20_six_sided_dice, binwidth=1, label="20 six-sided die")
    plt.legend();
    ```
    - But if we re-run cell 10, notice what happens **\*\*\***Cell 10 included below, not retyped — just confusing as the numbers are changing all the time!**\*\*\***
    ```python
    N_SIDES=20   # change to 20 sided dice

    outcomes_roll_6_d20 = [
        roll_n_dice(n_dice=6) for _ in range(10000)
    ]
    sns.histplot(outcomes_roll_6_d20, binwidth=1)
    ```
    - If we run this code, it **\***looks**\*** like it is rolling 20 sided dice, but really `roll_n_dice` has changed since we ran this cell. This is actually rolling 6 d6s. In an ordinary Python script we don’t go back and rerun code, but a Jupyter notebook allows us to run things out of order — and when doing iterative programming we often do.
    We have to be careful when doing iterative development that we track the scope of everything we are doing.
    - Jupyter notebooks do have the `Kernel > Restart and run all` menu option that will clear all state from your notebook, and run it top-to-bottom. This is a check that the results you are seeing are not coming from doing “iterative development”  
      _Do a restart and run all_
  - CON: CAN BREAK NOTEBOOK BY REMOVING IMPORTS OR RENAMING VARIABLES
    - _Delete the `import random` import_
    - The notebook will also retain global variables and imports. So if we remove the `import  random` statement, note that the code is still working (for now)
      _Rerun one of the histogram cells_
    - Because the notebook has already imported the module, it won’t realize that it is missing until you restart — or potentially give it to someone else to use.
    - _Do a restart and run all to show the code is actually broken_
    - Have you encountered these types of issues with notebooks as well? If you have any tips, post a comment!

### Scripts + Notebooks

- We can get around some of these issue by taking functions we have developed in a notebook, and moving them into importable scripts.
- ******\*******show dice.py******\*******
- Here we have a Python script that does all the rolling for us. By “starting over” in a script, it can be easier to find different patterns.
  - e.g. instead of providing a default argument for the sides of a die, we can use partial function application to create a function for this common case.
- go back to the notebook, and delete the cells that define N_SIDES, and both versions of `def roll_n_dice`. Also import dice at the top. Basically replace all the previous code with the last cell.
- Now we can import our functions from the dice module, and still use Jupyter for plotting.
- Separating our code like this has other advantages. Jupyter is a little trickier to use with some of the standard Python tools, like
  - Autoformatters (black)
  - Linters (flake8/pylint)
  - Version control diffs
- It is also difficult to import functions from a Jupyter notebook, so it is challenging to write unit tests for code in a Jupyter notebook.
- By separating the logic of the code, we can use testing and tools to keep our code clean, while still leveraging the visualization, exploration, and commentary that Jupyter notebooks bring.

### Final thoughts

- Jupyter notebooks are a great way to write code interactively and directly visualize what’s happening.
- Being able to run cells in arbitrary order is great for exploration and iterative design, but it also make your code difficult to reason about.
- In that case, start moving parts of your code to regular Python modules, and import them.
- That way, you can have your cake and eat it too. Or throw it in someone’s face. Or you can do other things with that cake. I don’t even wanna know!
- Once part of your code is in regular modules, you can write unit tests for it and use standard Python tooling such as linters and type checkers.
- I’m a big fan of using type annotations. Watch this video next for 5 reasons why I think you should also use them.
- Thanks for watching, take care!
