# M-A-Identification-Alogirthm-for-Norwegian-Accounting-Data
The algorithm takes Norwegian accounting data from Regnskapsdatabasen and identifies instances of M&amp;A. It identifies M&amp;A based on a change in parent organization and name. 

The algorithm takes the input of data by Regnskapsdatabasen by SNF and marks M&As from the data. Prior to feeding the data to the algorithm, you must merge the original datasets to combine accounting data and firm characteristics. Then, you must append the different year-files you are interested in together. You then have to convert the data set into XLS before feeding it to the algorithm.

Without changing any parameters, the M&A algorithm needs at least 5 years of data to work. We used data for 2004 to 2020 initially, as earlier years contained errors and were missing the ownership variable, which is crucial for the identification of a majority owner.

The output is a data set that satisfies the time frame condition of at least five observations per company and marked M&As by the ma2 variable. The ma2 variable is defined as 1 in the pre-acquisition year, and zero otherwise. It thus marks the treated observations and the proposed matching year for treatment analysis.
