# Python Wordle Solver

**a basic self contained wordle solver **

Takes inputs of letters used in wordle and returns list of remaining words, ordered by 'score'.

The 'score' of a word is detemrined by the frequency of the letters in said word appearing in the other remaining words, ignoring double letters until the sample is sufficently small

takes the inputs:
```
  red_set -> a list of [string], all the 'red' letters
  yellow_set -> a dictionary of {string:list[int]}. the yellow letter and corresping position it appeared yellow at (positions are 0 index).
  green_set -> a dictionary of {string:list[int]}. the green letter and corresping position it appeared green at (positions are 0 index).
 ```
  
   _for example:_
  ```
    red_set = ['i', 'd', 'e', 'u', 'g', 'l'],
    yellow_set = {'o': [2,3]},
    green_set = {'r': [0]}
  ```
  
 Returns:
 ```
 Number of words still possible
 4 highest scoring words remaining
 ```
  
   _for example:_
  ```
 There is 14 possible words still remaining
 the highest scoring words are [('ronco', 55), ('rorty', 55), ('rocta', 49), ('rotan', 49)]
  ```
