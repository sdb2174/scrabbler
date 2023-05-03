Scrabble RL AI
================

The goal of this project is to improve upon the existing evaluation of scrabble states and moves.

# Introduction and Related Work

We will assume the reader is familiar with the rules of scrabble which can be found [here](LINK).

When making a move, professional players consider 4 main things:
- The state of the board (current tiles and their orientation on the board)
- The points they will get for playing a word
- The letters left in their hand
- The remaining multiplier tiles that are left on the board for playing a word

While factors such as the probability of the tiles in the other players hand are also a factor, they are stochastic and cannot be estimated in a way that would improve on the information of what has been played and our current hand.

We focus on 2 of these key factors: The letter left in the players hand given a play (known as leaves) and the remaining multiplier tiles on the board.

Currently, the SOTA ScrabbleAI is [Quackle](http://people.csail.mit.edu/jasonkb/quackle/) which trained on Millions of Monte Carlo simulations. This AI, though powerful, has 2 major weekness which stem from its dependence on lookup tables to determine penalties for leaves. 

1. The penalties are specific to the the distrubtion of letters that were in the games they were trained on.This approach cannot adapt to changes in the number of different letters in the bag because of this. 
2. Even if using the standard set of letters, this method becomes less and less useful as the game goes on because it doesn't consider the letters that have already been played along with the letters in the players hand. This is likely why the model cannot solve end games perfectly. Currently, brute force methods, such as [Ortograph](https://elbbarcs.com/en/EndGame/description.htm), are used to solve these situations which can be computationally expensive.

To improve on this, we look to adjust for these issues with a modified Q-learning approach.

# Method
We describe our value function as below:
The standard Q values function is as described below:
$$
Q(s_t,a) = R(s,a) + \lambda Q(s^,,a)
$$
We modify this and we decompose the equation into:
$$
Q(s_t,a) = R(s,a) + f(l(s_t,a),s_t,b) + g(m(s_t,a))
$$
Where $f()$ is the function that determines the pentality for leaving the remaining tiles in the players hand, $l$, and $g()$ determines the penalty for leaving the set of remaining multiplier tiles, $m$. This is our approximation of the true Q value function which, due to the massive state and action space, is beyond the scope of this project.

Our focus will be on the first penalty, $f()$. We describe $f()$ as follows:
$$
f(l,s,b) = d(l) + \lambda_1 h(s_p,b)
$$
where $s_p$ is the combination the letters that are already on the board + the letters in the players hand and $b$ is the original distribution of letters in the bag. $d()$ simple uses the quakle look-up table value. This is so the $f()$ has reasonable starting ground.

We run simulations using [INSERT NAME OF SIMULATOR HERE](INSERT LINK TO ORIGINAL REPO HERE). 

# References:
https://medium.com/@14domino/scrabble-is-nowhere-close-to-a-solved-game-6628ec9f5ab0






