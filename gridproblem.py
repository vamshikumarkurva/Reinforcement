import numpy as np

Gamma = 0.99
Rewards=dict()
for i in range(1,4):
	for j in range(1,5):
		if (i,j)==(3,4):
			Rewards[(i,j)]=1
		elif (i,j)==(2,4):
			Rewards[(i,j)]=-1
		elif (i,j)==(2,2):
			Rewards[(i,j)]=None
		else:
			Rewards[(i,j)]=0.2#-0.02

Actions=['N','E','W','S']
Prob=dict()
Prob['R']=0.1
Prob['L']=0.1
Prob['S']=0.8

outcome = dict()
for a in Actions:
	for p in Prob:
		if p=='S':
			a_n = a
		elif (a,p)==('N','L'):
			a_n = 'W'
		elif (a,p)==('N','R'):
			a_n = 'E'
		elif (a,p)==('E','L'):
			a_n = 'N'
		elif (a,p)==('E','R'):
			a_n = 'S'
		elif (a,p)==('S','L'):
			a_n = 'E'
		elif (a,p)==('S','R'):
			a_n = 'W'
		elif (a,p)==('W','L'):
			a_n = 'S'
		elif (a,p)==('W','R'):
			a_n = 'S'
		outcome[(a,p)]=(a_n,Prob[p])

Transitions=dict()
for i in range(1,4):
	for j in range(1,5):
		for key in outcome:
			a,d = key
			a_n,p = outcome[key]
			if a_n=='N':
				i_n,j_n = i+1,j
			if a_n=='S':
				i_n,j_n = i-1,j
			if a_n=='E':
				i_n,j_n = i,j+1
			if a_n=='W':
				i_n,j_n = i,j-1
			if i_n < 1:
				i_n = 1
			if j_n < 1:
				j_n = 1
			if i_n > 3:
				i_n = 3
			if j_n > 4:
				j_n = 4
			if (i,j)==(2,4) or (i,j)==(3,4):
				(i_n,j_n) = (i,j)
			if (i_n,j_n)==(2,2):
				(i_n,j_n)=(i,j)
			if (i,j) not in Transitions:
				Transitions[(i,j)]=[(i_n,j_n,a,d,p)]
			else:
				Transitions[(i,j)].append((i_n,j_n,a,d,p))

#print 'Transitions: ', Transitions

value=dict()
for i in range(1,4):
	for j in range(1,5):
		if (i,j)==(2,2):
			value[(i,j)]=None
		elif (i,j)==(2,4):
			value[(i,j)]=-1
		elif (i,j)==(3,4):
			value[(i,j)]=1
		else:
			value[(i,j)]=0

val_action=dict()

# Value iteration ------> optimal value function
diff = 100
while diff > 0.01:
	err = 0
	for i in range(1,4):
		for j in range(1,5):
			k = value[(i,j)]
			val_action['N']=0
			val_action['E']=0
			val_action['S']=0
			val_action['W']=0
			if (i,j)!=(2,2) and (i,j)!=(2,4) and (i,j)!=(3,4):
				for key in Transitions[(i,j)]:
					i_n,j_n=(key[0],key[1])
					action = key[2]
					prob = key[4]	
					val_action[action] += prob*value[(i_n,j_n)]
				value[(i,j)] = Rewards[(i,j)] + Gamma*max(val_action.values())
				err += abs(k-value[(i,j)])        
			diff = err

# optimal policy
policy = dict()
for i in range(1,4):
	for j in range(1,5):
		if (i,j)==(2,2) or (i,j)==(2,4) or (i,j)==(3,4):
			policy[(i,j)]=None
for i in range(1,4):
	for j in range(1,5):
		val_action['N']=0
		val_action['E']=0
		val_action['S']=0
		val_action['W']=0		
		if (i,j)!=(2,2) and (i,j)!=(2,4) and (i,j)!=(3,4):
			for key in Transitions[(i,j)]:
				i_n,j_n=(key[0],key[1])
				action = key[2]
				prob = key[4]	
				val_action[action] += prob*value[(i_n,j_n)]
			policy[(i,j)] = max(val_action,key=val_action.get)

print 'Optimal Policy: ', policy
print 'Optimal values: ', value
