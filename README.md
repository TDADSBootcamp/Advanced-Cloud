Supporting materials for Data Science Bootcamp - Big Data Ecosystem

# Contents

Each of the following have their own README.md instructions.

- [python/race_condition](python/race_condition) demonstrates incorrect final values of a shared counter when incremented by multiple threads concurrently.
- [python/awesome_game](python/awesome_game) supports an exercise to manually walk through a map/reduce process to produce a leaderboard from player scores.
- [python/word_count](python/word_count) is a mapper and reducer in Python to implement a word count over text input.
- [python/knn](python/knn) implements a k-nearest neighbours classifier using two map/reduce operations.

# Running without Hadoop

We can test our mappers and reducers by piping outputs to input and using the `sort` command line tool to simulate the shuffle step.

Example: `cat myfile.txt | python mapper.py | sort | python reducer.py`

# Running Hadoop

You can optionally run a real Hadoop cluster on your VM to process these jobs.

You can install and run Hadoop on your VM using [these instructions](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html).

There is also a [Dockerfile](Dockerfile) provided in this project that builds a Docker image with a Hadoop distribution installed. 
Build the image from this directory: `docker build -t hadoop .`

Run the word count example from this directory:

```
docker run \
  -v $(pwd)/python:/work \
  hadoop \
  -input /work/word_count/war_of_the_worlds.txt \
  -output /work/uncommitted/hadoop-output/$(date --iso-8601=seconds) \
  -mapper 'python3 /work/word_count/mapper.py' \
  -reducer 'python3 /work/word_count/reducer.py'
```

This will run a container based on the `hadoop` image you built, mounting the `python` directory to `/work`.

:warning: the output that Hadoop will write from this container will not be owned by your user account. You will need to `sudo rm -rf python/uncommitted` to delete them.