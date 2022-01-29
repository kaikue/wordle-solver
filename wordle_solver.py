def generate_words_file(word_len):
    dict_file = open("words_alpha.txt", "r")
    output_file = open("words_len" + str(word_len) + ".txt", "w")
    for word in dict_file:
        if len(word.strip()) == word_len:
            output_file.write(word)
    dict_file.close()
    output_file.close()

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
    #find guess with highest average eliminations
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

def eliminate_possibilities(possibilities, guess, response):
    possibilities_reduced = possibilities.copy()
    for word in possibilities:
        word_response = generate_response(guess, word)
        if word_response != response:
            possibilities_reduced.remove(word)
    return possibilities_reduced

def play(word_len, response_func):
    possibilities = read_words_file(word_len)
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
#play_real(5)
import time
start_time = time.time()
play_fake("robot")
end_time = time.time()
print("Elapsed time: {:.2f}".format(end_time - start_time))
