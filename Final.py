#Burning Question:  Do younger/newer senators (those with less seniority) vote more on the issue and less on partisan lines

import requests, json, matplotlib.pyplot as plt, csv, numpy as np, matplotlib.patches as mpatches
from statistics import mean

#API key for ProPublica is in pro_publica_api.txt and is not uploaded to Git
with open("pro_publica_api.txt") as f:
    pro_publica_key = f.read()

#Sessions of Congress with necessary voting percentage data start at session 101 year 1989 to 1991 and end at current, session 117

#string template for get_congress_session to allow modification of sessions pulled depending on need 
pro_publica_req = 'https://api.propublica.org/congress/v1/{}/senate/members.json'


#This is a wrapper function that requires the pro_publica_req variable, and the parameter is the session of congress that is desired (necessary for the request to work)
# as well as the required header and propublica key required to authenticate the request by propublica
#Required input:  desired session number in range of 110 to 117 to be supplied by the user in the form of an integer
#Output Api get request of specified session of Congress 
def get_congress_session(number):
    return requests.get(pro_publica_req.format(number), headers = {"X-API-Key" : pro_publica_key})

#This function places the the response.json for results and members, where in the actual response the desired data is.
#Following this, the .csv is made based on the session of congress (supplied by user when the program is activated)
#When the file is opened the headers are written (last name, first name, votes with party pct, votes against party pct and missed votes)
#using the header names, it loops through the information and writes the columns based on the information with the key words (which are also the column names)

def get_CSV_data(response):
    senators = response.json()['results'][0]['members']
    file_name = "Congressional Session " + response.json()['results'][0]['congress'] + ".csv"
    with open (file_name, mode="w", newline="") as csv_file:
        fieldnames = ["last_name", "first_name", "votes_with_party_pct", "votes_against_party_pct", "votes_against_party_pct", "missed_votes_pct"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for senator in senators:
            writer.writerow(senator)

#scatter plot functions 

#Function is taking seniority information from ProPublica and creating a ranking system by taking the maximum seniority, 
# subtracting each senators listed senority and assigning it 
#a number.  Lowser the number the more senior the senator is.  This is used in the display_scatter_plots as the Y axis when called
def calculate_senority(senators):
    seniority = [int (senator["seniority"]) for senator in senators]
    maximum = max (seniority)
    return [ maximum - i for i in seniority]

#Function loops through obtained information extracting the data that represents the votes with party information to display 
# on the X access when called in the display_scatter_plot function

def calculate_votes_with_party(senators):
    return [float(senator["votes_with_party_pct"]) for senator in senators]

#Function used by display_scatter_plot to create key on graph.  It loops through the obtained information 
# and based on the party affiliation provided, assigns it a color to be used.

def display_party_affiliation (senators):
    key = {"R": "red", "D" : "blue", "ID": "green"}
    return [key [senator["party"]] for senator in senators]


#function to create scatter plot based on user input to obtain the .json information from ProPublica,
#calculate_senorit, calculate_votes_with_party, and display_party_affiliation to generate a graph,
#that plots each member of congress, color coded by party, on a field based on their seniority and how often they vote in line with their party

def display_scatter_plot (response):
    senators = response.json()['results'][0]['members']
    senority_list = calculate_senority(senators)
    votes_with_party = calculate_votes_with_party(senators)
    party_affiliation = display_party_affiliation(senators)
    plt.scatter(votes_with_party, senority_list, c=party_affiliation)
    plt.xlabel("Votes with Party Percentage")
    plt.ylabel("Seniority")
    plt.title("Seniority vs. Votes with Party" )
    democrat_blue = mpatches.Patch(color="blue", label="Democrat")
    republican_red = mpatches.Patch(color="red", label="Republican")
    other_green = mpatches.Patch(color="green", label="Other")
    plt.legend(handles=[democrat_blue, republican_red, other_green])
    plt.show()

#line graph items

#function that calculates the mean for Democrats, Republicans, and Independents (when available) that demonstrates how often each party votes togehter on average. 

def calculate_votes_with_party_average(senators, party):
    filter_senators = [ senator for senator in senators if senator ["party"] ==party]
    return mean(calculate_votes_with_party(filter_senators)) if filter_senators else [0]

#function that createss a line graph for each party by applying calculate_votes_with_party_average for each party for sessions 101 - 117

def display_line_graph (response):
    congressional_sessions_range = range (101, 118)
    senators_by_sessions = [get_congress_session(session).json()['results'][0]['members'] for session in congressional_sessions_range]
    republican_mean = [calculate_votes_with_party_average(senators, "R") for senators in senators_by_sessions]
    democrat_mean = [calculate_votes_with_party_average(senators, "D") for senators in senators_by_sessions]
    independent_mean = [calculate_votes_with_party_average(senators, "ID") for senators in senators_by_sessions]
    x = np.arange(len(congressional_sessions_range))
    width = 0.25
    fig, ax = plt.subplots()
    item_1 = ax.bar(x - width, republican_mean, width, label='Republican', color="red")
    item_2 = ax.bar(x, democrat_mean, width, label='Democrat', color="blue")
    item_3 = ax.bar (x + width, independent_mean, width, label= "Independent", color="green")
    plt.xlabel("Session of Congress")
    plt.ylabel("Average Vote with Party Percentage")
    plt.title("Political Party vs. Votes with Party")
    ax.set_xticks(x)
    ax.set_xticklabels(congressional_sessions_range)
    ax.legend()
    fig.tight_layout()
    plt.show()

#user interface requiring int input between 101 - 117.

print("Welcome to Congressional Voting Data""\n""\n"
"This program is designed to utilize ProPublica API and pull voting statistics on senators.""\n" 
"Specifically, it examines the percentage that members of the Senate vote with their Party." "\n"
"Output includes:""\n" 
"1. .csv of senators and their in line party voting percentavge," "\n" 
"2. Line graph comparing each party by session of Congress and the percentage each party on average votes together,""\n" 
"3. Scatter plot for the session of the Senate you request that breaks down by party and seniority voting trends." "\n")
user_input = input("Please enter the session of the senate (101 - 117) you wish to view.  ")
user_input = int(user_input)


#Calling Functions

get_congress_session(user_input)

get_CSV_data(get_congress_session(user_input))

display_line_graph(get_congress_session(user_input))

display_scatter_plot(get_congress_session(user_input))
#demonstrate when Democrats hold majority
#congressional_session_117 = get_congress_session(117)
#display_scatter_plot(congressional_session_117)

#congressional_session_115 = get_congress_session(115)
#demonstrate when Republicans hold Majority
#display_scatter_plot(congressional_session_115)

#get_CSV_data(congressional_session_117)
#display_line_graph(congressional_session_117)
#display_scatter_plot(congressional_session_117)

#Cynical view:  if in minority, consequences for bucking the party are minor 
#Slighty less cynical:  if in minority, legislation that comes to the vote is from the majority party and depending on vote, opposition is preferred in order to appease local constituents 