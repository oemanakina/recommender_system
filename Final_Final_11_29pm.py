import csv

# KEY for skill names
legend = {"V": "Vocabulary", "A": "Word Agreement", "S": "Spelling", "Gen": "Gender", "Per": "Persons", "G": "Grammar", "T": "Tenses", "Past": "Past Tenses", "Fut": "Future Tenses", "M": "Modes", "Sub": "Subjunctive Mode", "Hyp": "Hypothetical Mode", "Pro": "Professional Communication", "Pron": "Pronouns", "Prep": "Prepositions"}
# contains total mistakes made by students && skill_weights.values() is the vector
student_mistakes = {"V": 0, "A": 0, "S": 0, "Gen": 0, "Per": 0, "G": 0, "T": 0, "Past": 0, "Fut": 0, "M": 0, "Sub": 0, "Hyp": 0, "Pro": 0, "Pron": 0, "Prep": 0}
skill_weights = {"V": 0, "A": 0, "S": 0, "Gen": 0, "Per": 0, "G": 0, "T": 0, "Past": 0, "Fut": 0, "M": 0, "Sub": 0, "Hyp": 0, "Pro": 0, "Pron": 0, "Prep": 0}
# weights for calculating student vector
mistake_per_skill = [4, 1, 4, 2, 2, 11, 7, 3, 2, 3, 1, 1, 4, 2, 1]
#weight_by_test = [0.2, 0.05, 0.2, 0.1, 0.1, 0.55, 0.35, 0.15, 0.1, 0.15, 0.05, 0.05, 0.2, 0.1, 0.05]
# is the "ideal" exercise set based on mistakes made by student
ideal_set = []

exercises = []

#naive_bayes classifier
#global variables
#prior probabilities for getting below B, B or C
priors = [0.08, 0.67, 0.25]

#probabilities of a range of scores for each level
# 0-30, 31-40, 41-50, 51-60, 61-70, 71-80, 81-90, 91-100
#each tuple represents 1 range for 3 outcomes (below B, B, C)
densities = [(0,0,0),(0.2,0,0),(0.4,0,0),(0.4,0.1,0),(0,0.4,0),(0,0.4,0.3),(0,0.1,0.5),(0,0,0.2)]

outputs_bayes = ["You do not qualify for level B just yet. See details for recommendations: ",
           "You will most likely get the B Level.\n",
           "Congratulations! Looks like you can get the C Level!\n",
           "You can easily get 100% on Level C. Why do you even learn French?? No recommendations for you."]
extra_output_B_C = ["However your score is below mean for this level. See recommendations to improve your score:",
                "Your level is above mean for this level! Good job, but see recommendations to keep your score."]
means = [71.3, 86.4] #means for scores B and C

def get_data(filepath):

    txt_file = open(filepath, "r")

    results = list(csv.reader(txt_file, delimiter = ","))
    for i in range(20):     #there are 20 questions, so we will count it manually
        if (results[i][0] == '2'): continue         #skip questions with full marks

        skill_list = results[i][1].split(",")       #get all skills

        if (results[i][0] == '1'):                  #if 1 then first skill mastered, skip and get the rest
            skill_list.remove(skill_list[0])

        for skill in skill_list:                    #add 1 to all skills
            student_mistakes[skill] += 1

    i = 0
    for key,value in student_mistakes.items():
        skill_weights[key] = (value/mistake_per_skill[i])
        if (skill_weights[key] >= 0.4): ideal_set.append(1)
        else: ideal_set.append(0)
        i+=1
    
    txt_file.close()

    with open("exercises.csv", newline='') as csvfile:
          reader = csv.reader(csvfile, delimiter=',', quotechar='|')
          j = 0
          for row in reader:
            exercises.append([])
            for item in row:
                exercises[j].append(int(item))
            j+=1

    return results

def matching_skills(ideal, exercise):
    total_matches = 0
    for i in range(len(ideal)):
        if ideal[i] == 1 and ideal[i]-exercise[i] == 0:
            total_matches += 1
    return total_matches


def best_match(ideal):
    matched = {}
    index = 0
    for exercise in exercises:
        matched[index] = matching_skills(ideal, exercise)
        index+=1
    
    exercise_list = {}
    the_one = [key for key, value in matched.items() if value == max(matched.values())]
    exercise_list[the_one[0]] = exercises[the_one[0]]
    matched.pop(the_one[0])
    the_one = [key for key, value in matched.items() if value == max(matched.values())]
    exercise_list[the_one[0]] = exercises[the_one[0]]
    matched.pop(the_one[0])
    the_one = [key for key, value in matched.items() if value == max(matched.values())]
    exercise_list[the_one[0]] = exercises[the_one[0]]

    return exercise_list

def recommendation_string(dict_exercises):
    text = "You should focus on: \n"
    skill_dict = {k: v for k, v in sorted(skill_weights.items(), key = lambda item: item[1])}
    skills_to_practice = [key for key, value in skill_dict.items() if value >= 0.4]
    #if len(skills_to_practice) == 0: return "You got 100% in this test keep up the good work"
    for i in skills_to_practice:
        text += "{} \n".format(legend[i])
    text += "Based on that we recommend the following practice sets: \n"
    for key,value in dict_exercises.items():
        i = 0
        text += "Exercise set {}: focuses on ".format(key+1)
        for skill in legend.values():
            if value[i] == 1:
                text += "{}, ".format(skill)
            i+=1
        text = text[:len(text)-2]
        text += "\n"

    text = text[:len(text)-2]
    return text
        
def naive_bayes_classifier(results):
    final_score = round(float(results[len(results) - 1][0]))
    # final_score = 80 - YOU CAN PLAY WITH DIFFERENT VALUES WITHOUT CHANGING THE INPUT FILE, JUST TO SEE DIFFERENT OUTPUTS
    p_score_given_level = []
    # print(type(final_score), final_score)
    j=0
    #counter for tuples' indices
    if final_score <= 30:
        p_below_B = densities[0][j]
        p_level_B = densities[0][j+1]
        p_level_C = densities[0][j+2]
    elif 31 <= final_score <= 40:
        p_below_B = densities[1][j]
        p_level_B = densities[1][j+1]
        p_level_C = densities[1][j+2]
    elif 41 <= final_score <= 50:
        p_below_B = densities[2][j]
        p_level_B = densities[2][j + 1]
        p_level_C = densities[2][j + 2]
    elif 51 <= final_score <= 60:
        p_below_B = densities[3][j]
        p_level_B = densities[3][j + 1]
        p_level_C = densities[3][j + 2]
    elif 61 <= final_score <= 70:
        # print("I am here")
        p_below_B = densities[4][j]
        p_level_B = densities[4][j + 1]
        p_level_C = densities[4][j + 2]
    elif 71 <= final_score <= 80:
        p_below_B = densities[5][j]
        p_level_B = densities[5][j + 1]
        p_level_C = densities[5][j + 2]
    elif 81 <= final_score <= 90:
        p_below_B = densities[6][j]
        p_level_B = densities[6][j + 1]
        p_level_C = densities[6][j + 2]
    elif 91 <= final_score <= 100:
        # print("I am here")
        p_below_B = densities[7][j]
        p_level_B = densities[7][j + 1]
        p_level_C = densities[7][j + 2]


    p_score_given_level.append(p_below_B*priors[0])
    p_score_given_level.append(p_level_B*priors[1])
    p_score_given_level.append(p_level_C*priors[2])
    max_p = max(p_score_given_level)
    # print("done computing", p_score_given_level)
    # print ("max is", max_p)
    if max_p==0:
        output = outputs_bayes[0]
    else:
        for i in range(3):
            if p_score_given_level[i] == max_p:
                output = outputs_bayes[i]

        if (output == outputs_bayes[1]):
            if final_score < means[0]:
                output += extra_output_B_C[0]
            else:
                output += extra_output_B_C[1]
        elif (output == outputs_bayes[2]):
            if final_score < means[1]:
                output += extra_output_B_C[0]
            else:
                output += extra_output_B_C[1]

    return output



if __name__ == '__main__':
    filepath = 'sample_score_new.csv'
    results = get_data(filepath)
    print(naive_bayes_classifier(results))
    print(recommendation_string(best_match(ideal_set)))