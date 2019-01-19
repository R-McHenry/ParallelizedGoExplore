# SynchronousGoExplore
A first bare bones paralleled implementation of Go Explore as described by the Uber Engineering blog post

Currently no deep learning is incorperated with the project. The avalible exploration policies are random, and markov chain.

The notebook syncGoExplore.ipynb demonstrates the use of Go Explore to create a speedrun of level in a gym environment using multiple threads.

Dependencies:

	ray (linux and osx only)
	gym retro
	imageio (also needs freeimage)
	rom file for the game environment

Original reddit discussion with some more information:
https://www.reddit.com/r/MachineLearning/comments/agf43s/d_go_explore_vs_sonic_the_hedgehog/

Original blog post by Uber:
https://eng.uber.com/go-explore/

To do:

Add smarter exploration policies (fast simple models and deep learning)

Asynchronous Go Explore, i.e. allow workers to be constantly playing and updating only when ready/neccesary

Add iterative deepening

Add procedures for experiments to search for good hyperparameters