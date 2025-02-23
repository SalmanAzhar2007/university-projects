def find_edit_distance(string1,string2):
    len1 = len(string1)
    len2 = len(string2)
    
    grid = [[0 for x in range(len2+1)] for y in range(len1+1)]           #Creates a dynamic programming grid, in the form of a 2D array of dimensions
                                                                         #(len1+1)x(len2+1) where len1 and len2 are the length of the strings.
                                                                         # 1 is added to represent the base case, the number of ooperations it would take
    #This loop traverses through and populates the 2D array              #to make each word from an empty string
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if j == 0:
                grid[i][j] = i                 #Solves for the base case and string1
                                              
            elif i == 0:
                grid[i][j] = j                 #Solves for the base case and string2
                                               
            elif string1[i-1] == string2[j-1]:
                grid[i][j] = grid[i-1][j-1]    #Solves for if the corresponding characters in each string are the same.
                                               # 1 is subtracted from the position of the character being accessed in each string
                                               #to adjust for the base case. Grid[i][j] is set to grid[i-1][j-1] as that is the
                                               #previous minimum and no extra operations are added since the characters are the same
            else:
                grid[i][j] = min(grid[i-1][j],grid[i][j-1],grid[i-1][j-1])+1 #If the characters are different, the previous solution is checked
                                                                             #and one is added since another operation must occur
                
    for row in grid: #Displays the grid
        print(row)
        
    return grid[i][j]

str1 = input("Enter the first word ")
str2 = input("Enter the second word ")

print("The edit distance is",find_edit_distance(str1,str2))