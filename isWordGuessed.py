from bisect import bisect_left 
def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE...
    lettersGuessed_sorted = sorted(lettersGuessed)
    length_lettersGuessed_sorted = len(lettersGuessed_sorted)
    check_guessWord_flag = True
    print(lettersGuessed_sorted)
    for i in range(len(secretWord)):
        k = bisect_left(lettersGuessed_sorted, secretWord[i])
        if k == length_lettersGuessed_sorted or lettersGuessed_sorted[k] != secretWord[i] :
           check_guessWord_flag = False
           print (check_guessWord_flag)
           break
    return check_guessWord_flag

secretWord = 'apple'
lettersGuessed = ['e', 'i', 'k', 'p', 'l', 's']
print(isWordGuessed(secretWord, lettersGuessed))