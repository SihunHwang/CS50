# degree

Program that determines how many “degrees of separation” apart two actors are.
The part that I wrote is the 'shortest path' function in degrees.py file.

HOW TO EXECUTE: use terminal. command line arguments which can either be <small> or <large>, each representing the size of the dataset.
In the command line type: <python degrees.py {small or large}>
Then input two Hollywood stars when told to do so. One at a time.
They must be in the people.csv file of chosen dataset.

EXPLANATION:
According to the Six Degrees of Kevin Bacon game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.

In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (it’s true that a movie could take us to multiple different actors, but that’s okay for this problem). Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.
