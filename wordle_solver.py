import numpy as np
import json

def generate_words_file(word_len):
    dict_file = open("words_alpha.txt", "r")
    output_file = open("words_len" + str(word_len) + ".txt", "w")
    for word in dict_file:
        if len(word.strip()) == word_len:
            output_file.write(word)
    dict_file.close()
    output_file.close()

def gen_init_guess_recursive(word, possibilities, results, response):
    if len(response) == len(word):
        print(response, end=": ")
        possibilities = eliminate_possibilities(possibilities, word, response)
        best_guess = find_best_guess(possibilities)
        results[response] = best_guess
        print(best_guess)
        return
    for letter in ["g", "y", "b"]:
        gen_init_guess_recursive(word, possibilities, results, response + letter)

def generate_initial_guesses(starting_word):
    possibilities = np.array(read_words_file(len(starting_word)))
    initial_guesses = {}
    gen_init_guess_recursive(starting_word, possibilities, initial_guesses, "")
    json_str = json.dumps(initial_guesses, indent=4)
    guesses_file = open("initial_guesses_" + starting_word + ".json", "w")
    guesses_file.write(json_str)
    guesses_file.close()

def test_all(word_len):
    words = read_words_file(str(word_len) + "_answers")
    max_tries = 0
    hardest_word = ""
    total_tries = 0
    for word in words:
        tries = play_fake(word)
        if tries > max_tries:
            max_tries = tries
            hardest_word = word
        total_tries += tries
    average_tries = total_tries / len(words)
    print()
    print("Played", len(words), "words")
    print("Average guesses:", average_tries)
    print("Max tries:", max_tries, "(" + hardest_word + ")")

def read_words_file(word_len):
    words = []
    file = open("words_len" + str(word_len) + ".txt", "r")
    for word in file:
        words.append(word.strip())
    return words

def generate_response(guess, answer):
    response = ""
    used = [False] * len(guess)
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            response += "g"
        else:
            found_yellow = False
            for j in range(len(guess)):
                if j != i and answer[j] == guess[i] and not used[j] and answer[j] != guess[j]:
                    used[j] = True
                    response += "y"
                    found_yellow = True
                    break
            if not found_yellow:
                response += "b"
    return response

vec_response = np.vectorize(generate_response)

def eliminate_possibilities(possibilities, guess, response):
    return possibilities[np.where(vec_response(guess, possibilities) == response)]

def count_eliminate_possibilities(possibilities, guess, response):
    return eliminate_possibilities(possibilities, guess, response).size

vec_count_eliminate = np.vectorize(count_eliminate_possibilities, excluded=["possibilities"])

def find_best_guess(possibilities):
    #find guess with highest average eliminations
    best_remain = None
    best_guess = None
    for guess in possibilities:
        total_remain = np.sum(vec_count_eliminate(possibilities=possibilities, guess=guess, response=vec_response(guess, possibilities)))
        """total_remain = 0
        for answer in possibilities:
            response = generate_response(guess, answer)
            result_possibilities = eliminate_possibilities(possibilities, guess, response)
            total_remain += result_possibilities.size"""
        if best_guess is None or total_remain < best_remain:
            best_remain = total_remain
            best_guess = guess
    return best_guess

def play(word_len, response_func):
    possibilities = np.array(read_words_file(word_len))
    def guess_word(guess, word_len, response_func):
        nonlocal possibilities
        print("Guess: " + guess)
        response = response_func(guess)
        if (response == "g" * word_len) or (response == ""):
            return None
        possibilities = eliminate_possibilities(possibilities, guess, response)
        print("Possibilities:", possibilities.size)
        return response
    
    guess = "arose"
    tries = 0
    
    """initial_guesses_file = open("initial_guesses_" + guess + ".json")
    initial_guesses = json.load(initial_guesses_file)
    tries = 1
    result = guess_word(guess, word_len, response_func)
    if result is None:
        print("Won in 1 try... wow!")
        return tries
    guess = initial_guesses[result]"""
    
    while True:
        tries += 1
        result = guess_word(guess, word_len, response_func)
        if result is None:
            print("Won in " + str(tries) + " tries!")
            return tries
        guess = find_best_guess(possibilities)

def play_real(word_len):
    def get_response(guess):
        return input("Response: ").lower()
    return play(word_len, get_response)

def play_fake(answer):
    def get_response(guess):
        response = generate_response(guess, answer)
        print("Response: " + response)
        return response
    return play(len(answer), get_response)

#generate_words_file(5)
#generate_initial_guesses("arose")
#test_all(5)
play_real(5)
#play_fake("boxer")

"""
import time
start_time = time.time()
play_fake("hobby")
end_time = time.time()
print("Elapsed time: {:.2f}".format(end_time - start_time))
#"""
