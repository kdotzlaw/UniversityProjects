# Analyzing Covid-19 Data to Predict Long Covid-19 Cases

## Analysis

Our group used the Apriori algorithm to mine association rules from demographic data and identify rules that have a minimum confidence of 0.3. We then preformed demographic-symptom clustering using symptom frequencies and chi-square tests to determine differences between groups. Using the Boruta algorithm and descriptive analysis, we identified the most important features for prediction. We created and trained three models, a decision tree model, a random forest model created by Sudre, and a custom random forest model, to predict whether a person has a long covid-19 case. This project resulted in 3 publications in IEEE alongside our professor.

## Results

- Demographic analysis showed that individuals who are assigned female at birth, female identifying individuals, white individuals, and individuals who have had at least one vaccination are developing Long Covid-19
- Identified high confidence association rules that indicate that individuals assigned female at birth develop Long Covid-19
- Symptom clustering determined that cough, headache and fatigue were the most prevalent symptoms for individuals developing Long Covid-19
- Symptom clustering determined that cough, headache and fatigue were the most prevalent symptoms for individuals developing Long Covid-19
- Our decision tree had an AUC of 0.706
- Our custom random forest model had an AUC of 0.721
- Sudre's random forest model had an AUC of 0.76
