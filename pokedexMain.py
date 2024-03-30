"""
Created By: nickwyman
Created on: Thu Mar 21 18:03:23 2024
Name of File: pokedexMain.py

Algorithm:

    Input:
        Gets the name of the pokemon they would like to know about using input()
        
    Processing:
        Search through the pokemonData.csv file for the requested pokemons information
        Find average Stat Total from generation their requested pokemon is from using math (Finding Mean of total stats)
        Find Average of all different stat types for the generation the requested pokemon is from (Finding Mean of all individual stats)
        

    Output:
        Display an image of their requested pokemon
        Display a plot of the average stats
        display where the requested pokemon falls on the average plot
        Display all stats of requested pokemon

"""
#Imports
import pokedexConstants as C
from PIL import Image
import urllib.request
from restart import restart
import matplotlib.pyplot as plt
from title import printTitle

#Functions

#1st Main Function, beginning of program
def main():
    #ask user what pokemon they would like to learn about
    pokemonName = input("\nWhat is the name of the pokemon you're looking for? > ")
    #open the CSV file
    searchfile = open("pokemonData.csv", "r")
    
    found = 0
    #for loop that loops through the file for requested pokemon
    for column in searchfile:
        for line in searchfile:
            #when pokemon is found it will run program
            found = getInfo(searchfile, pokemonName, line, found)
    #if the pokemon is found the program will run, if not it will promt them to try again
    if found == 1:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        restart(main)
    elif found == 0:
        print("\nWe couldn't find the requested Pokemon, Please Try Again!!")
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        restart(main)
            
#2nd Main Function, rest of program
def getInfo(searchfile, pokemonName, line, found):
    pokemonData = line.split(",")
    if pokemonName.casefold() == pokemonData[C.NAME].casefold():
        found = 1
        #Calling different Functions
        printEm(pokemonData)
        showImage(pokemonData)
        xvals, yvals, average = getAverage(searchfile, pokemonData)
        makePlot(xvals, yvals, pokemonData, average)
        recordData(pokemonData)
    return found

#Image Function
def showImage(pokemonData):
    urllib.request.urlretrieve(pokemonData[C.IMAGE],"Image.png")
    im = Image.open("Image.png")
    im.show()

#Print Data Function
def printEm(pokemonData):
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #Name of pokemon
    print("\nThe name of the Pokemon is: %s" %(pokemonData[C.NAME]), "\n")
    #Generation of Pokemon
    print("This Pokemon is part of Generation: %s" %(pokemonData[C.GEN]), "\n")
    #Pokedex Entry
    print("Pokedex Entry: %s" %(pokemonData[C.DESC]), "\n")
    #Stats of pokemon
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\nHere are %s's Stats:\n" %pokemonData[C.NAME])
    print("Stat Total: %s" %(pokemonData[C.TOTAL]))
    print("HP: %s" %(pokemonData[C.HP]))
    print("Attack: %s" %(pokemonData[C.ATK]))
    print("Defense: %s" %(pokemonData[C.DEF]))
    print("Sp. Atk: %s" %(pokemonData[C.SPATK]))
    print("Sp. Def: %s" %(pokemonData[C.SPDEF]))
    print("Speed: %s\n" %(pokemonData[C.SPEED]))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    
#Averaging function
def getAverage(searchfile, pokemonData):
    searchfile2 = open("pokemonData.csv", "r")
    #initial values
    totalPokemon = 1
    num = 1
    statTotal = int(pokemonData[C.TOTAL])
    stat = int(pokemonData[C.TOTAL])
    #lists to be returned
    yvals = []
    xvals = []
    #value of generation the requested pokemon is from
    generation = pokemonData[C.GEN]
    for line in searchfile2:
        pokemonData2 = line.split(",")
        if str(generation) == pokemonData2[C.GEN]:
            #stat stuff
            stat = int(pokemonData2[C.TOTAL])
            yvals.append(stat)
            statTotal = statTotal + stat
            #num stuff
            xvals.append(num)
            num = num + 1
            totalPokemon = totalPokemon + 1
    #Math to get Average
    average = statTotal/totalPokemon
    print("The Stat Average in Generation %s is: %s" %(generation, int(average)))
    difference = int(average) - int(pokemonData[C.TOTAL])
    if difference < 0:
        difference = difference * -1
        print("\nYour Pokemon is Stronger than the Average by %s points\n" %(int(difference)))
    elif difference > 0:
        print("\nYour Pokemon is Weaker than the Average by %s points\n" %(int(difference)))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return xvals, yvals, average

#Plotting Function
def makePlot(xvals, yvals, pokemonData, average):
    #Variables
    gen = pokemonData[C.GEN]
    #Sort the y values (Pokemon Stat totals)
    yvals.sort()
    #Plot the lines
    #All stats for generation requested pokemon is from
    plt.plot(xvals, yvals, color="r", label="Stat Totals for Gen %s" %(gen))
    #specified pokemon's stat total
    plt.axhline(y = int(pokemonData[C.TOTAL]), color = 'b', linestyle = '--', label="%s's Stat Total" %(pokemonData[C.NAME]))
    #Average stat total for generation of requested pokemon
    plt.axhline(y = average, color = 'g', linestyle = ':', label="Stat Average for Gen %s" %(gen)) 
    #Naming the x axis
    plt.xlabel("Number of Pokemon")
    #Naming the y axis
    plt.ylabel("Stat Total")
    #Giving a title to the graph
    plt.title("Distribution of Stats")
    #Show the legend
    plt.legend()
    #Save the graph as an image
    try:
        plt.savefig("statDistribution.png")
        print("\nImage of Graph Saved Succsesfully")
    except:
        print("\nPlot Couldn't save correctly for some reason!!")
    #show the graph
    plt.show()
    pltIm = Image.open("statDistribution.png")
    pltIm.show()

#Output File Function
def recordData(pokemonData):
    try:
        #open or make a file called PokemonData.txt to write information to
        f = open("PokemonData.txt", "w")
        #write all of the information to the PokemonData.txt file (one line of code, used escape character to break it up)
        f.write("Name of Pokemon: %s\nPokedex Entry: %s\n~~~~~~~~~~~~~~~~~~~~\nStat Total: %s\nHealth Points: %s \
        \nAttack Points: %s\nDefense Points: %s\nSpecial Attack Points: %s\nSpecial Defense Points: %s\
        \nSpeed Points: %s\nGeneration: %s\n~~~~~~~~~~~~~~~~~~~~" \
        %(pokemonData[C.NAME], pokemonData[C.DESC], pokemonData[C.TOTAL], pokemonData[C.HP], \
        pokemonData[C.ATK],pokemonData[C.DEF],pokemonData[C.SPATK],pokemonData[C.SPDEF],\
        pokemonData[C.SPEED],pokemonData[C.GEN]))
        #close the output file
        f.close()
        print("\nPokemon Stat File Saved Successfully")
    except:
        print("\nFile failed to work for some reason!!")

#Main Code Area
if __name__ == "__main__":
    #print the title and description of the program
    printTitle("Fully Functional Pokedex!!", "This is a fully functioning Pokedex for all current genetarions of Pokemon")
    #call the main function to kick things off
    main()