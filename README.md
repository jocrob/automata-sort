# automata-sort
Pixel Sorting is a popular method used for creating glitch art, first introduced by, digital media artist, Kim Asendorf as a Processing language script. The original algorithm chooses horizontal or vertical lines of pixels in an image and sorts them based on various color criteria. This project uses the basic premise of sorting pixels by value, and applies it to cellular automata to create a more dynamic range of effects in the output images. 

<h3> Usage </h3>

Requires Pillow 
> pip install Pillow

From command line:
<blockquote>python automatasort.py %PathToFile% %PathToImage% %Automaton% %NumberIterations%</blockquote>

As of now there are three automata to choose from Rule 90, Rule 184, and Conway's Game of Life. The arguments are...
> rule90, rule184, life

<h3> Examples </h3>

<p>Original Image</p>
<img src = "https://github.com/jocrob/automata-sort/blob/master/examples/flowers.jpg"> 

<p>Rule 90 - 15 iterations</p>
<img src = "https://github.com/jocrob/automata-sort/blob/master/examples/rule90%20-%2015%20iterations.png">

<p>Rule 184 - 30 iterations</p>
<img src = "https://github.com/jocrob/automata-sort/blob/master/examples/rule%20184%20-%2030%20iterations.png">

<p>Game of Life - 30 iterations</p>
<img src = "https://github.com/jocrob/automata-sort/blob/master/examples/GOL%20-%2030%20iterations.png">

<hr>

<p>Based on <a href = "https://github.com/satyarth/pixelsort"> satyarth's Pixel Sort </a></p>
