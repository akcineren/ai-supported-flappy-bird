
# flappy-bird

Reinforcement learning with NEAT framework used to generate a neural network that plays flappy bird.



## What does this project contains?

- Reinforcement learning model generating a neural network that plays flappy bird without any mistakes.
- An implementation of the famous game "Flappy Bird" in pygame library.





  
## How it works?

- Code takes the NEAT config file as input and generates continuous generations with given parameters

- Each generated bird gets reward for flying longer and passing the pipes without collisions.

- Birds with the most rewards are used for creating new generations until at least one bird scores 50 in the game. If a bird passes the 50th pipe it is considered and observed as a perfect model.

- When the ideal bird is found, game restarts with only one perfect model as bird and from now on FPS is fixed at 30.



  
## Run it yourself!

Clone the project
```bash
  git clone https://github.com/akcineren/flappy-bird.git
```

Go to project directory
```bash
  cd flappy-bird
```

Install required packages
```bash
  pip install neat-python
  pip install pygame
```

Run the code!
```bash
  cd scripts
  python main.py
```

## Things I suggest you to try.
- You can adjust the config file to observe effects of parameters on learning process.
- Population size can be reduced to achieve more generations and complex neural networks or can be increased to achieve less generations and more basic neural networks.
- Pipe spawning speed and the velocity of the pipes on the x-axis can be increased for more challenging gameplay so model can learn something harder than the classic flappy bird.
- Overall this project is a great tool for understanding the NEAT framework.

## Video of the project

  [![Watch the video](https://img.youtube.com/vi/tnb9b2qEga4/hqdefault.jpg)](https://youtu.be/tnb9b2qEga4)




  
