import numpy as np

def generate_words_file(word_len):
    dict_file = open("words_alpha.txt", "r")
    output_file = open("words_len" + str(word_len) + ".txt", "w")
    for word in dict_file:
        if len(word.strip()) == word_len:
            output_file.write(word)
    dict_file.close()
    output_file.close()

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

vec_response = np.vectorize(generate_response)

def find_best_guess(possibilities):
    #find guess with highest average eliminations
    best_remain = None
    best_guess = None
    for guess in possibilities:
        total_remain = 0
        for answer in possibilities:
            response = generate_response(guess, answer)
            result_possibilities = eliminate_possibilities(possibilities, guess, response)
            total_remain += result_possibilities.size
        if best_guess is None or total_remain < best_remain:
            best_remain = total_remain
            best_guess = guess
    return best_guess

def eliminate_possibilities(possibilities, guess, response):
    return possibilities[np.where(vec_response(guess, possibilities) == response)]

def play(word_len, response_func):
    possibilities = np.array(read_words_file(word_len))
    tries = 0
    
    def guess_word(guess, word_len, response_func):
        nonlocal possibilities
        print("Possibilities:", possibilities.size)
        print("Guess: " + guess)
        response = response_func(guess)
        if response == "g" * word_len:
            return True
        possibilities = eliminate_possibilities(possibilities, guess, response)
        return False
    
    guess = "arose"
    while True:
        tries += 1
        result = guess_word(guess, word_len, response_func)
        if result:
            print("Won in " + str(tries) + " tries!")
            return
        guess = find_best_guess(possibilities)

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
#play_real(5)
import time
start_time = time.time()
play_fake("robot")
end_time = time.time()
print("Elapsed time: {:.2f}".format(end_time - start_time))
