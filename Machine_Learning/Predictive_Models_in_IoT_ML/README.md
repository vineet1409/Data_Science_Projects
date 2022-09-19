# Predictive Models in IoT - Energy Prediction Use Case

### Description and Dataset Overview
This IoT project presents and discusses data-driven predictive models for the energy use of appliances. 
Data used include measurements of temperature and humidity sensors from a wireless network, whether from a 
nearby airport station and recorded energy use of lighting fixtures. 
The project discusses data filtering to remove non-predictive parameters and feature ranking. 
The data set is at 10 min for about 4.5 months. The house temperature and humidity conditions were monitored 
with a ZigBee wireless sensor network. Each wireless node transmitted the temperature and humidity conditions around 3.3 min. 
Then, the wireless data was averaged for 10 minutes periods. The energy data was logged every 10 minutes with m-bus energy meters. 
Weather from the nearest airport weather station (Chievres Airport, Belgium) was downloaded from a public data set from Reliable 
Prognosis (rp5.ru) and merged together with the experimental data sets using the date and time column. 
Two random variables have been included in the data set for testing the regression models and to filter 
out non-predictive attributes (parameters). 


### Key Takeaways
● Understanding the problem statement
● Importing Dataset directly from AWS
● Understanding the attributes and their datatypes
● Using the summary function in R and interpreting its result
● Time stamping the column with time attributes
● Visualizing and understanding density plot, Plotting box plot and whiskers plot for visualizing outliers
● Visualizing ggplot and Barplot
● EDA & Feature Engineering
● Applying Boosting model Gradient Boosting Model for training
● Applying SVM using different Kernels
● Selecting best evaluation metrics
● Using Grid Search CV to extract the best features
● Making final predictions and Saving them in form of CSV
● Visualizing in QuickSight






