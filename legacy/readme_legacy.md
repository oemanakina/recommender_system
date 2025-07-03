# Legacy Project Description: French Language Score Predictor & Recommender

This document describes the original project as it was developed for the Intro to AI course (COMP3106, Fall 2022). The code for this version is contained entirely within the `Final_Final_11_29pm.py` script.

## Objective

The goal of the original project was to simulate a recommender system for French language learners. It was designed to perform two primary functions based on a student's test results:

1.  **Predict Proficiency Level:** Estimate the student's final proficiency level (e.g., "Level B," "Level C") based on their overall score.
2.  **Recommend Exercises:** Identify the student's specific areas of weakness (e.g., grammar, vocabulary, tenses) and recommend a personalized set of practice exercises to help them improve.

## How It Works

The entire logic is contained in a single script and relies on a set of pre-defined data structures and rules.

### 1. Data Input

-   The system reads a student's test results from a CSV file (e.g., `sample_score_new.csv`).
-   Each row in the CSV represents one of 20 test questions, containing the score for that question and a tag for the linguistic skills it tests (e.g., "V,A" for Vocabulary and Word Agreement).
-   The last two rows contain the total points and the final percentage score.

### 2. Error Analysis and Skill Weighting (`get_data` function)

-   The script iterates through the score file and counts the number of mistakes a student made for each specific skill.
-   It calculates a "skill weight" for each category by comparing the student's mistakes against a pre-defined list of the total possible mistakes for that skill (`mistake_per_skill`).
-   If a skill's weight is 0.4 or higher, it's considered a "weakness," and this is used to build an "ideal set" vector representing the skills the student needs to practice.

### 3. Exercise Recommendation (`best_match` and `recommendation_string` functions)

-   The script reads a separate `exercises.csv` file, where each row represents an exercise set as a vector of skills it covers.
-   The `best_match` function compares the student's "ideal set" vector to all available exercise vectors to find the ones that cover the most areas of weakness.
-   It selects the top three best-matching exercise sets.
-   The `recommendation_string` function then formats this information into a human-readable report, listing the weak skills and describing the recommended exercise sets.

### 4. Proficiency Level Prediction (`naive_bayes_classifier` function)

-   This function implements a simple Naive Bayes classifier to predict the student's final level.
-   It uses a pre-defined set of prior probabilities for achieving each level (`priors`).
-   It also uses a set of hard-coded "densities," which represent the probability of getting a certain score range, given a specific proficiency level.
-   Based on the student's final score, the script calculates the posterior probability for each proficiency level and outputs a prediction.
-   It also provides additional feedback comparing the student's score to the average for that level.

## Summary

The original project was a rule-based system that cleverly used hand-coded weights, probabilities, and vector comparisons to simulate an intelligent recommender. It was self-contained and effectively demonstrated the core logic of identifying user needs and matching them to relevant resources. The new version of this project builds upon this foundation by re-implementing the logic within a scalable, production-ready software architecture. 