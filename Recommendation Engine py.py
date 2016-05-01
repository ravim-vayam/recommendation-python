# Sample data

data = {
        
'Julie': 
{'Burger': 7, 'Icecream': 9, 'Cupcake': 9}, 

'Rob': 
{'Burger': 7, 'Icecream': 5, 'Cupcake': 8}, 

'Joe': 
{'Burger': 6, 'Icecream': 7, 'Cupcake': 9}, 

'Kathy': 
{'Burger': 7, 'Icecream': 5, 'Cupcake': 9}, 

'Ben': 
{'Burger': 8, 'Icecream': 9}

}

from math import sqrt

# Pearson correlation coefficient for Person records
def sim_pearson(preferences, person1, person2):
	
	# Get the list of mutually rated items
	si = {}
	for item in preferences[person1]:
		if item in preferences[person2]: si[item]=1

	# Find the number of elements
	n = float(len(si))

	# If they have no ratings in common, return 0
	if n==0: return 0

	# Add up all the preferences
	sum1Preferences = sum([preferences[person1][it] for it in si])
	sum2Preferences = sum([preferences[person2][it] for it in si])

	# Sum up the squares
	sumXSquare = sum([pow(preferences[person1][it],2) for it in si])
	sumYSquare = sum([pow(preferences[person2][it],2) for it in si])

	# Sum up the ratings
	sumRatings = sum([preferences[person1][it]*preferences[person2][it] for it in si])

	# Calculate Pearson score
	top = sumRatings - (sum1Preferences*sum2Preferences/n)
	bottom = sqrt((sumXSquare - pow(sum1Preferences,2)/n)*(sumYSquare - pow(sum2Preferences,2)/n))
	if bottom == 0: return 0

	pCoef = top/bottom
	return pCoef


# Gets recommendations for a person by using a weighted average of every other user's rankings
def getRecommendations(preferences,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in preferences:
		# don't compare to self
		if other==person: continue
		sim=similarity(preferences,person,other)

		# ignore scores of zero or lower
		if sim<=0:continue
		for item in preferences[other]:

			# only score movies I haven't seen yet
			if item not in preferences[person] or preferences[person][item]==0:
				# Similarity * score
				totals.setdefault(item,0)
				totals[item]+=preferences[other][item]*sim
				#Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim

		# Create the normalised list
		rankings=[(total/simSums[item],item) for item,total in totals.items()]

		# Return the sorted list
		rankings.sort()
		rankings.reverse()
		return rankings

print getRecommendations(data, 'Ben')