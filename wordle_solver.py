def generate_words_file(word_len):
    dict_file = open("words_alpha.txt", "r")
    output_file = open("words_len" + str(word_len) + ".txt", "w")
    for word in dict_file:
        if len(word.strip()) == word_len:
            output_file.write(word)
    dict_file.close()
    output_file.close()

#find the guess that eliminates the most possibilities (best average-case performance)
#if not the first guess: eliminate possible words based on input
#for each potential guess:
#   for each possible answer: what if it was that answer? how many possibilities would that eliminate?
#   across all possible answers: what is the average # of possibilities eliminated?
#across all possible guesses: what is the highest average elimination?

def read_words_file(word_len):
    words = set()
    file = open("words_len" + str(word_len) + ".txt", "r")
    for word in file:
        words.add(word.strip())
    return words

def generate_response(guess, answer):
    response = ""
    used = [False] * len(guess)
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            used[i] = True
            response += "g"
        else:
            found_yellow = False
            for j in range(len(guess)):
                if j != i and answer[j] == guess[i] and not used[j]:
                    used[j] = True
                    response += "y"
                    found_yellow = True
                    break
            if not found_yellow:
                response += "b"
    return response

def find_best_guess(possibilities):
    best_avg_elims = -1
    best_guess = None
    for guess in possibilities:
        total_elims = 0
        for answer in possibilities:
            response = generate_response(guess, answer)
            result_possibilities = eliminate_possibilities(possibilities, guess, response)
            eliminations = len(possibilities) - len(result_possibilities)
            total_elims += eliminations
        avg_elims = total_elims / len(possibilities)
        #print("guess:", guess, "avg elims:", avg_elims)
        if avg_elims > best_avg_elims:
            best_avg_elims = avg_elims
            best_guess = guess
    return best_guess

"""
def valid(word, guess, response):
    return generate_response(guess, word) == response
    
    # remove all greens
    # yellows: must be anywhere but in that position
    # blacks: must not appear at all except as designated by other yellows/greens
    for i in range(len(response)):
        if response[i] == "g":
            if word[i] != guess[i]:
                return False
        elif response[i] == "b":
            if word[i] == guess[i]:
                return False
    return True
"""

def eliminate_possibilities(possibilities, guess, response):
    possibilities_reduced = possibilities.copy()
    for word in possibilities:
        word_response = generate_response(guess, word)
        if word_response != response:
            possibilities_reduced.remove(word)
    return possibilities_reduced

def play(word_len, response_func):
    possibilities = read_words_file(word_len)
    #guess_responses = []
    tries = 0
    
    tries = 1
    guess = "arose"
    print("Guess: " + guess)
    response = response_func(guess)
    if response == "g" * word_len:
        print("Won in " + str(tries) + " tries!")
        return
    possibilities = eliminate_possibilities(possibilities, guess, response)
    
    while True:
        tries += 1
        print("Possibilities:", len(possibilities))
        guess = find_best_guess(possibilities)
        print("Guess: " + guess)
        response = response_func(guess)
        if response == "g" * word_len:
            print("Won in " + str(tries) + " tries!")
            return
        #guess_responses.insert(0, (guess, response))
        possibilities = eliminate_possibilities(possibilities, guess, response)

def play_real(word_len):
    def get_response(guess):
        return input("Response: ").lower()
    play(word_len, get_response)

def play_fake(answer):
    def get_response(guess):
        response = generate_response(guess, answer)
        print("Response: " + response)
        return response
    play(len(answer), get_response)

#generate_words_file(5)
play_real(5)
#play_fake("robot")