def longest_subsequent_pal(s):
    l=len(s)
    myDinamicMatrix=[[0 for i in range(l)] for j in range(l)]
    for i in range(l, 0, -1): #we always use i-1 because the range dont consider the last element [0]
        myDinamicMatrix[i-1][i-1]=1#all single letter is palindromic
        for j in range(i, l, 1):
            if s[i-1]==s[j]:
                myDinamicMatrix[i-1][j]=myDinamicMatrix[i][j-1]+2# we can update the matrix by add 2 at the lenght of partial lenght stored in the
                                                                  # previus left cell obtaining the next max lenght for the string start from i-1 to j
            else:
                myDinamicMatrix[i-1][j]=max(myDinamicMatrix[i][j], myDinamicMatrix[i-1][j-1]) # the max lenght after this step inluded is the max
                                                                                               # from the previus left cell(same start) and
                                                                                               # the previus down cell (sart one position right;
                                                                                               # dont consider string starting from i-1)
    return(myDinamicMatrix[0][l-1])

print('Give me a string:')
s=input()
print('The lenght of the longhest substring is: {}'.format(longest_subsequent_pal(s.lower())))
