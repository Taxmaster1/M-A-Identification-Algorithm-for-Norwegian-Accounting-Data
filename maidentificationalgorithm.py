#Creator: Adaas
#Importing required packages for perfrorming the data import and dataframe structure
import pandas as pd

#the algorithm takes the input as data from SNF Regnskapsdatabasen.
#Insert your own path to the file here:
rawdata = pd.read_excel("C:\\Users\\your location and file name")

#Sorting the data based on company id and year
rawdata = rawdata.sort_values(by =["orgnr", "aar"])
rawdata = rawdata.reset_index(drop = True)

#Converting data to dataframe
df = pd.DataFrame(rawdata)
#Creating the "ma1" variable as a empty column. This will later be market as years past and prior to acquisition
df.insert(4,"ma1", "")
#sorting dataset by organization number and then by year
df = df.sort_values(by =["orgnr", "aar"])
#reset index after the sorting
df = df.reset_index(drop = True)
#df = df.drop("Unnamed: 0", axis = 1)

df["orgnr"] = df["orgnr"].astype(int)

#verifying time-frame loop which runs thorugh df and marks observartions with 5 or more observations per company.
df.insert(5,"timeframe", "")
time = df.columns.get_loc("timeframe")
a = 0
for a in range(len(df)-5):
    if df.iloc[a,0] == df.iloc[a+1,0] and df.iloc[a,0] == df.iloc[a+2,0] and df.iloc[a,0] == df.iloc[a+3,0] and df.iloc[a+4,0] == df.iloc[a,0]:
        df.iloc[a,time] = 1
        df.iloc[a+1,time] = 1
        df.iloc[a+2,time] = 1
        df.iloc[a+3,time] = 1
        df.iloc[a+4,time] = 1

#creates new df with only the companies with sufficient timeframe.
df = df.loc[df["timeframe"] == 1, :]

#Main-loop for finding and marking M&A's

#Getting the location for the "ma1" variable, year, and organization number from mother company
ma1p = df.columns.get_loc("ma1")
aarp = df.columns.get_loc("aar")
mornr = df.columns.get_loc("mors_orgnr")
sel = df.columns.get_loc("orgnr")
mornavn = df.columns.get_loc("mors_navn")
selnavn = df.columns.get_loc("navn")


#preparing loop and convrting mother name to string
t = 1
df["mors_navn"] = df["mors_navn"].astype(str)

df["aar"] = df["aar"].astype(int)
df["navn"] = df["navn"].astype(str)
df["mors_orgnr"] = df["mors_orgnr"].astype(int)
#the main loop runs for the length of the datasett minus 2, since we are performing actions for 2 years in advance
for t in range(len(df)-3):
    selskap = df.iloc[t, sel]
    #i is determined as t+1 for all runs
    # first condition. orgnr must be equal in both t and t+1 timeframe
    if selskap == df.iloc[t+1, sel] and selskap == df.iloc[t+2, sel] and selskap == df.iloc[t-1, sel] and selskap == df.iloc[t+3, sel]:
        # Locating the year column, creating year variables for each of the mentioned timeframes
        år = df.iloc[t, aarp]
        år1 = år +1
        år2 = år +2
        årm1 = år -1
        år3 = år +3
  
        # second condition. both the mother name and mother organization number must be different from t to i
        if df.iloc[t,mornr] != df.iloc[t+1,mornr] and df.iloc[t,mornavn] != df.iloc[t+1,mornavn]:
            #Columns with text are formated as sentences. split each word from the sentences to a list of words for several columns

            mor1 = df.iloc[t, mornavn].split()
            mor2 = df.iloc[t+1, mornavn].split()
            morm_1 = df.iloc[t-1, mornavn].split()
            sel1 = df.iloc[t, selnavn].split()
            #Geting the location of orgnr and storing as a variable
      
            # third condition. the length of the mother name must be longer than one word. Else, pass on the observation
            if len(mor1) > 1 and len(mor2) > 1 and len(morm_1) > 1:
                # Fourth condition. Checking for similarites between the list of words from the mother name and company name. Also, checks if new mother name has similarites whit the old mother name.
                # Mainly checking if the first and or second words are similar
                if mor1[0] != mor2[0] and mor1[1] != mor2[0] and mor1[0] != mor2[1] and mor1[0] != sel1[0] and mor2[0] != sel1[0] and morm_1[0] != mor2[0] and morm_1[1] != mor2[0] and morm_1[0] != mor2[1] and mor2[1] != sel1[0] and mor2[0] != sel1[1] and mor2[0] != f"{mor1[0][0]}.":
                       
                    # Sixth condition. Checking if the observations are in consecutive years, and not have any gaps
                    if år1 == df.iloc[t+1, aarp] and år2 == df.iloc[t+2, aarp] and årm1 == df.iloc[t-1, aarp] and år3 == df.iloc[t+3, aarp]:
                        # Seventh and final condition. Checks if the new mother number is the same for the following two years after i, and that it is not the same as i-2 and i-3.
                        if df.iloc[t+1,mornr] == df.iloc[t+2,mornr]  and df.iloc[t+1,mornr] == df.iloc[t+3,mornr] and df.iloc[t+1,mornr] != df.iloc[t-1,mornr] and df.iloc[t,mornr] == df.iloc[t-1,mornr]:
                            #Now as all conditions are met, we mark t as 0, marking it as beofre M&A. Then 1,2,3 or -1 for eac respective year after and prior to t.

                            df.iloc[t, ma1p] = 0
                            df.iloc[t+1, ma1p] = 1
                            df.iloc[t+2, ma1p] = 2
                            df.iloc[t-1, ma1p] = -1
                            df.iloc[t+3, ma1p] = 3
                            
                            #A clean-up loop that erases earlier instances of ma1, as we only want one M&A per company, the last one.
                            # if loop finds an M&A, check if company is the same up to 21 years past (longer than dataset) and erase any ma1.
                            b = 0
                      
                            for b in range(19):
                                if df.iloc[t, ma1p] == 0:
                                   if selskap == df.iloc[t-b-3, sel]:
                                      df.iloc[t-b-3, ma1p] = ""
            else:
                pass
                                        
# inserting the "ma2" as a empty column and storing location as variable ma2.
df.insert(5, "ma2", "")
ma2p = df.columns.get_loc("ma2")

#Loop for marking ma2. if ma1 is equal to 1, ma2 is also 1. else ma2 is 0. essensialy marks "post M&A".

x = 0
for x in range(len(df)-1):
    if df.iloc[x,ma1p] == 0:
        df.iloc[x,ma2p] = 1
    else:
        df.iloc[x,ma2p] = 0

#deleting the variables we don't need anymore
del t,a,x,time,ma2p,aarp,ma1p,mor1,mor2, morm_1,sel1,år1,år3,år2,årm1,selskap,mornavn,mornr,sel,selnavn,år

#extracting all the columns we need from the df and adding them to a new dataframe "sample".
sample = df[["orgnr","navn", "aar", "timeframe","ma1", "ma2", "mors_navn","mors_orgnr", "drmarg", "ebitdamarg", "ekandel", "sumgjek","totinn",
          "aarsrs", "ebitda", "sentral_20",  "drmarg", "gjeld",  "utb",  "ansatte", "max_eiera", "sector", "anl",  "rentekost","sumeiend",
          "landsdel","eierstruktur","ratingkode","timeframe","lonnsos"]].copy()  


# Lines 130 to 196 extract the sectors and creates new columns for them to be used in the horisontal data set
sample.insert(30,"sectorvector",0)
sample.insert(31, "agriculture", 0)
sample.insert(32, "offshore&shipping", 0)
sample.insert(33, "transport", 0)
sample.insert(34, "manufacturing", 0)
sample.insert(35, "it", 0)
sample.insert(36, "electricity", 0)
sample.insert(37, "construction", 0)
sample.insert(38, "retail", 0)
sample.insert(39, "finance", 0)
sample.insert(40,"other",0)

#defining the location of the needed variables for the sector identification
vector = sample.columns.get_loc("sectorvector")
sector = sample.columns.get_loc("sector")
agri = sample.columns.get_loc("agriculture")
offshore = sample.columns.get_loc("offshore&shipping")
transport = sample.columns.get_loc("transport")
manu = sample.columns.get_loc("manufacturing")
it = sample.columns.get_loc("it")
el = sample.columns.get_loc("electricity")
con = sample.columns.get_loc("construction")
retail = sample.columns.get_loc("retail")
fin = sample.columns.get_loc("finance")
other = sample.columns.get_loc("other")
m = 1
#loop for revenue
for m in range(len(sample)):
    if sample.iloc[m,sector] == "Agriculture":
        sample.iloc[m,agri] = 1
        sample.iloc[m,vector] = 1
    
    elif sample.iloc[m,sector] == "Offshore/Shipping":
        sample.iloc[m,offshore] = 1
        sample.iloc[m,vector] = 2
        
    elif sample.iloc[m,sector] == "Transport":
        sample.iloc[m,transport] = 1
        sample.iloc[m,vector] = 3
        
    elif sample.iloc[m,sector] == "Manufacturing":
        sample.iloc[m,manu] = 1
        sample.iloc[m,vector] = 4
        
    elif sample.iloc[m,sector] == "Telecom/IT/Tech":
        sample.iloc[m,it] = 1
        sample.iloc[m,vector] = 5
        
    elif sample.iloc[m,sector] == "Electricity":
        sample.iloc[m,el] = 1
        sample.iloc[m,vector] = 6
        
    elif sample.iloc[m,sector] == "Construction":
        sample.iloc[m,con] = 1
        sample.iloc[m,vector] = 7
        
    elif sample.iloc[m,sector] == "Wholesale/Retail":
        sample.iloc[m,retail] = 1
        sample.iloc[m,vector] = 8
        
    elif sample.iloc[m,sector] == "Finance":
        sample.iloc[m,fin] = 1 
        sample.iloc[m,vector] = 9
        
    elif sample.iloc[m,sector] == "Other services":
        sample.iloc[m,other] = 1

del other, sector, vector, transport, offshore, manu,it, el, m ,agri, con, fin, retail


#exporting the data excel. Insert your wanted file and location.
sample.to_excel("C:\\Users\\your wanted location and user\\finalsample.xlsx")
