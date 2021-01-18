# MealPepper

# Abstract
The objective of this project was to create a meal planner that a user could use to create meal plans that meet his or her dietary needs as cheaply as possible. A user would provide the algorithm constraints like “vegan”, 2200 calories, 150+ grams of protein, and all daily vitamins. Our algorithm would then compute the cheapest diet (using 100k+ foods from a local Whole Foods) for the user that meets all of the given requirements. 

# Introduction / Background / Related work
In doing research on how to do this, we discovered there has been several studies on a similar problem and has been nicknamed the “The Diet Problem” or “The Stigler Diet”. The diet was originally motivated to provide healthy nutrition for soldiers as cheaply as possible.

The algorithm that has been used in the past is Linear Programming (LP). Linear Programming (as we will describe later with more detail) solves a system of linear equations maximizing (or minimizing) for a singular function -- in this case, price. In order to get integer results, it used Integer programming, which is a more computationally expensive algorithm.

However, when this problem was done historically, it was done on optimizing using several dozen to several hundred food items. LP is an NP-Hard problem meaning it is not suited for the 100k+ food items in Whole Foods’ database. To combat this challenge, we either needed a more efficient algorithm, or we needed to filter the number of foods we run the algorithm on. We considered multiple options for each. To improve the algorithm, we looked for an algorithm that could quickly find local maximas instead of global maximas, like simulated annealing. This seemed to be too complex, so we decided to try a heuristic to filter food items first. We thought it would yield better results with less programming complexity. We will explain how we did this later in our implementation details.

# High-level Algorithm

Create DB using a data from scraping Whole Foods’ product catalog
Given constraints, use a heuristic value on each food to predict its likelihood in being in that meal plan, pick the top 1000 products
Use Linear Programming algorithm to compute the meal plan

An explanation of Linear / Integer Programming

### Figure 1

![alt text](https://i.stack.imgur.com/HACvN.png)


Figure 1 is a visual representation of linear-programming. It is a 2D representation of a problem because there are only two variables it is optimizing for. In our algorithm, we are using 1000 variables, but because displaying a 1000D graph is not feasible, this one will do (just keep this in mind).

There are 3 important aspects of this algorithm.
The constraints (shown in Figure 1 as black lines and red equations)
The Max function (shown with red lines and a black equation)
And variables/possible solutions, which are represented by different points on graphs

When the constraints are mapped on the graph, they leave a region of possible solutions that is represented by the shaded region. The points of intersection of that region are known as critical points. The algorithm states that the optimal solution exists in one of these critical points (the max value for all of the critical points is the solution of the algorithm). Being more specific, the last point that you hit when moving the Maximizing line up (in this example by increasing Z) is the Optimal Solution. 

So in Figure 1, the optimal solution is at point (2.25, 3.75) = 41.25. Notice that these are decimal values. For our project we wanted to make it a little easier on the user and make these values integers. To get the maximal integer value is not as simple as rounding, it requires a slight variation of the algorithm known as Integer Programming.

To solve this problem, the critical points and region become formed by the points composed of integers, shown in Figure 1 as green dots, and the optimal solution becomes the max of the outer bound integer points. In this example, it would be (3, 3) = 39.




# Filtering Heuristic
To compute an optimal solution for a problem like ours, where we want to compute the optimal solution for 10s of thousands of foods (with capability to do even more), a polynomial function cannot be used. However, we made the assumption that we could guess based on the user’s inputted dietary restrictions and a food item’s nutritional profile, we could predict a rough estimate as to how likely a food item would be in the user’s meal plan.

Using this heuristic, we could filter out the 1000 food items (a number we found the algorithm could handle in a quick manner) and still have a good chance of creating either an optimal solution or close to it.

For the heuristic value, we decided to use a number that represented how much of the constraints a food item satisfied per dollar.
```# ((SUM of Min Constraint Percentage met) - (SUM of Max Constraint Percentage met)) / pricePerServing
def calculate_heuristic(self, food):
   perc_points = 0
   for c in self.constraints:
        name = c["name"]  # the nutrient constrained by constraint
        nutrient = food.nutritionMap.__getitem__(name)

        # value per serving for given food and nutrient
        food_val = nutrient.perServing if not nutrient == None else 0
        if "min_val" in c:
           perc_points += (food_val / c["min_val"])
        if "max_val" in c:
           perc_points -= (food_val / c["max_val"])

   return perc_points / food.pricePerServing
```




For every constraint (composed of a nutrient, min_val, and max_val), see what percent a given foods satisfies that constraint (add for min values and subtract for max values). Then divide the percentage points by the price of that food to make sure the cost to meet the goal is accounted for.

In my trials, this always resulted in an optimal solution that was within 2% of the optimal solution ran from using the entire food database without filtering.

Empirical results
We had three significant evolutions of the algorithm.
Fully Optimal Solution using Integer programming, that used every food in database as input
Sub-Optimal Solution that filtered the foodset to 1000 random foods before executing the Integer Programming algorithm.
A Near-Optimal Solution that filtered the foodset to the 1000 food items we deemed most likely to be in the meal plan.

To compare the results of our algorithm, we ran all three algorithms with the same input and compared the results.

The Input (16 constraints):
```
{
   "filters": ["paleo-friendly"],
   "constraints": [
       { "name": "calories", "min_val": 2000, "max_val": 2100},
       { "name": "protein", "min_val": 140 },
       { "name": "carbohydrates", "max_val": 100 },
       { "name": "vitaminD", "min_val": 20},
       { "name": "vitaminA", "min_val": 1000 },
       { "name": "vitaminE", "min_val": 15 },
       { "name": "vitaminK", "min_val": 120 },
       { "name": "vitaminC", "min_val": 90},
       { "name": "thiamin", "min_val": 1.2 },
       { "name": "selenium", "min_val": 55 },
       { "name": "riboflavin", "min_val": 1.3 },
       { "name": "niacin", "min_val": 16 },
       { "name": "vitaminB6", "min_val": 2 },
       { "name": "vitaminB12", "min_val": 6 },
       { "name": "iron", "min_val": 18 },
       { "name": "magnesium", "min_val": 420 }]}
```
       
Here are the results on 5 trials each.


Avg Computation Time
Optimal Solution Price
Algorithm 1
14.04s
$5.29/day
Algorithm 2
0.3s
$9.12/day
Algorithm 3
0.4s
$5.36/day


From these trials you can see why we evolved to the third algorithm. 14 seconds is too long for a user to wait for a solution, and $9.12 is nearly double the true optimal price making it not a useful algorithm for providing users with a cheap, healthy meal plan. At $5.36/day computed in less than half a second, the third algorithm is both usable and useful to users. 

Side Note: $5.36/day may seem expensive but that is due to all health constraints. It is possible to get 2000 calories a day for only $0.75 by eating All-Purpose flour (: 

# Conclusions / future directions 
We had a few original plans that we either deemed unnecessary or did not get to, the three I want to focus on are:
More complex heuristics
Weekly Meal Plans using CSP
Optimize for food ratings
Create UI for users

*More Complex Heuristics*  
It turned out to not be necessary, but if we had more time we would likely implement this feature anyways. The idea would be to run the Long-Form Optimal Solution on 1000s of different generated inputs, and then use machine learning to create a better heuristic for predicting how likely a food item is to be in a meal plan given constraints.

*Weekly Meal Plans using CSP*  
Week long meal plans is something if we had more time we would do. The idea would be to multiply the constraints by 7 and calculate enough food for the week. In order to divide the meal-plan into days, we were going to use CSP algorithms like Arc-Consistancy. The constraints would be things like “each day has 2 servings of veggies”, “if there is a grain, there also needs to be a meat”, etc. We did not get to this step so the idea is not fully flushed out, but if we had more time, it is something we would work on.

*Optimize for Food Ratings*   
Something that we would have liked to do would be to optimize not only for price, but also for food ratings. This way people could have not just cheap and healthy food, but also tasty. To make this happen, we would just create a new value function that takes into account a rating and not just price. How heavily the rating would be rated vs price would be up to the user.

*Creating a UI and shipping to users*  
We made a simple UI to allow this algorithm to be added to a website so users can interact with it. We did not fully connect the UI nor make it as User Friendly as we would like. This did not seem like a priority for the purposes of this class. If we had more time (and may still do it anyways), we would have created a UI and put it on the internet for people to use.






### Citations
Department of Math/CS - Home, www.mathcs.emory.edu/~cheung/Courses/323/Syllabus/ConstrainedOpt/int-prog1.html.
Devin. “Stigler Diet – Everything You Need to Know About the Stigler Diet.” TLC Diet, tlcdiet.org/stigler-diet/.
NEOS, neos-guide.org/content/diet-problem.
