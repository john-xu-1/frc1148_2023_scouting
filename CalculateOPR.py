import numpy # has matrix calculations
import TBA_Functions as tba
import pandas as pd




def coneNcubeOPR(event):   
    allTeam = tba.TBA_EventTeamsRaw(event)
    matches = tba.TBA_EventMatchKeys(event)
    
    coneMatrix = [] 
    cubeMatrix = []
    teamMatrix = []
    
    print ("len " + str(len(matches)) + " if this is zero that means matches isn't up")
    
    i = 0

    for match in matches:
        
        print (match)
        
        print (i)
        
        
        
        cur_match_data= tba.TBA_GetCurMatch(match)
        
        
        
        if (type(cur_match_data['score_breakdown']) is not type(None)):
         
            blueTeams = tba.GetBlueTeams(cur_match_data)
            
            print (i)
            
            
            
            redTeams = tba.GetRedTeams(cur_match_data)
            
            
            # for redTeam in redTeams:
            #     count = 0
            #     for team in allTeam:
            #         if (redTeam == team):
            #             isTeamsArray[count] = 1
            #         else: isTeamsArray[count] += 0
            #         count += 1
            
            # print (isTeamsArray)
            # teamMatrix.append(isTeamsArray)
            
            
            
            r = []
            for team in allTeam:
                if redTeams[0] == team or redTeams[1] == team or redTeams[2] == team:
                    r.append(1)
                else:
                    r.append(0)
            teamMatrix.append(r)
        
            b = []
            for team in allTeam:
                if blueTeams[0] == team or blueTeams[1] == team or blueTeams[2] == team:
                    b.append(1)
                else:
                    b.append(0)
            teamMatrix.append(b)
            
            
            
            blueTotalPiece = tba.GetBlueTeleopGamePiecePoints(cur_match_data)
            blueBototmPiece = tba.GetBlueTeleopGamePieceB(cur_match_data)
            blueMiddlePiece = tba.GetBlueTeleopGamePieceM(cur_match_data)
            blueTopPiece = tba.GetBlueTeleopGamePieceT(cur_match_data)
            
            redTotalPiece = tba.GetRedTeleopGamePiecePoints(cur_match_data)
            redBototmPiece = tba.GetRedTeleopGamePieceB(cur_match_data)
            redMiddlePiece = tba.GetRedTeleopGamePieceM(cur_match_data)
            redTopPiece = tba.GetRedTeleopGamePieceT(cur_match_data)
            
            coneBlueScore = 0
            
            for bottoms in blueBototmPiece:
                if (bottoms == "Cone"):
                    coneBlueScore += 2
            
            for middle in blueMiddlePiece:
                if (middle == "Cone"):
                    coneBlueScore += 3
            
            for top in blueTopPiece:
                if (top == "Cone"):
                    coneBlueScore += 5
                    
            cubeMatrix.append([blueTotalPiece - coneBlueScore])
            
            coneMatrix.append([coneBlueScore])
            
                    
            coneRedScore = 0
                    
            for bottoms in redBototmPiece:
                if (bottoms == "Cone"):
                    coneRedScore += 2
            
            for middle in redMiddlePiece:
                if (middle == "Cone"):
                    coneRedScore += 3
            
            for top in redTopPiece:
                if (top == "Cone"):
                    coneRedScore += 5
                
            cubeMatrix.append([redTotalPiece - coneRedScore])
            
            coneMatrix.append ([coneRedScore])
        
        
        
        
        # print(coneScore)
        # print (int(blueTotalPiece) - coneScore)
        
        
        
        
        #prettyPrint( TBA_MatchWinner(match))
        #we have the mathc data now, we fill in each match with the data, code not implemented yet
    
    
    
    teamMatrix = numpy.matrix(teamMatrix)
    coneMatrix = numpy.matrix(coneMatrix)
    cubeMatrix = numpy.matrix(cubeMatrix)
    
    pseudoinverse = numpy.linalg.pinv (teamMatrix)
    
    coneOPR = numpy.matmul(pseudoinverse, coneMatrix)
    cubeOPR = numpy.matmul(pseudoinverse, cubeMatrix)
    
    # print (coneOPR)
    
    
    coneArray = []
    cubeArray = []
    
    for cone in coneOPR:
        coneArray.append(float(cone[0][0]))
    for cube in cubeOPR:
        cubeArray.append(float(cube[0][0]))
    
    # print (coneArray)
    # print (cubeArray)
    # print("alteam:"+str(len(allTeam)))
    # print("coneOP:"+str(len(coneArray)))
    # print("cubeOP:"+str(len(cubeArray)))

#temp fix so that the write to sheets can run    
    noneArray = [0]*len(allTeam)
    
    if((len(coneArray)<len(allTeam))):
        coneArray = noneArray
        
    if((len(cubeArray)<len(allTeam))):
        cubeArray = noneArray
    
    df = pd.DataFrame( {"team": allTeam, "coneOPR": coneArray, "cubeOPR": cubeArray})

    print (df)
    return df
    

    

#coneNcubeOPR("2023cala")
# teamNames = []

# for i in range (0, len(team),1):
#     teamNames.append(tba.TBA_TeamNickname(team[i]))

# print (teamNames)

# df = pd.DataFrame ({'Names': teamNames, 'Number': team})

#print (df)


    
