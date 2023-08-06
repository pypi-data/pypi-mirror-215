import csv
import numpy as np
import itertools

class Hypo():
	def Format(self,file):
		X = []
		with open(file) as fileR :
			data = csv.reader(fileR)
			for i in data :
				del i[0]
				X.append(i)
		Head = X[0]
		del X[0]
		return X

	def FindS(self,data,CorrectP = "Yes",CorrectN = "No"):
		S = ['']*(len(data[0])-1)
		for data_X in data:
			if data_X[-1] in CorrectP:
				for i in range(len(data_X)-1) :
					if data_X[i] == S[i] or S[i] == '':
						S[i] = data_X[i] 
					if data_X[i] != S[i] and S[i] != '':
						S[i] = '?' 
		return [S]
 
	def HypoAll(self,data):
		global a
		Hd = np.array(data)
		n = Hd.shape[1]
		a,count_Hypo = [],1 
		point = 1
		# print(Hd)
		for i in range(n):
			a.append(sorted(list(set(Hd[:,i]))))
		# print(a)

		Hypo_all = list(itertools.product(*a))
		print("\nHypothesis all")
		for i in range(len(Hypo_all)) :
			Hypo_all_sort = list(Hypo_all[i])
			per = ""
			answer = Hypo_all_sort[-1]
			del Hypo_all_sort[-1]
			array_X = np.array(data)
			answer_X = list(array_X[:,-1])
			# print(answer_X)
			array_X = np.delete(array_X,len(data[0])-1,axis = 1).tolist()
			# print(array_X)
			for j in range(len(array_X)):
				if Hypo_all_sort == array_X[j] :
					if answer != answer_X[j] : per = "continue"
			if per == "continue" : continue
			print(count_Hypo,Hypo_all_sort,answer)
			count_Hypo += 1

	def Elimination(self,data,CorrectP = "Yes",CorrectN = "No"):
		def Candidate_Elimination(X):
			global S
			Sample = ['']*(len(X[0])-1)
			Geo,Geom = [],[]
			Hd = np.array(data)
			n = Hd.shape[1]
			a = []
			S = ['']*(len(data[0])-1)
			for data_X in data:
				if data_X[-1] in CorrectP:
					for i in range(len(data_X)-1) :
						if data_X[i] == S[i] or S[i] == '':
							S[i] = data_X[i] 
						if data_X[i] != S[i] and S[i] != '':
							S[i] = '?' 
			for result_01 in range(n):
				a.append(sorted(list(set(Hd[:,result_01]))))
			for i in range(len(X)):
				delete_Geo = []
				if X[i][-1] in CorrectP:
					for j in range(len(Geo)):
						for GeoFor in range(len(Geo[j])):
							for XFor in range(len(X[i])):
								if Geo[j][GeoFor] != '?':
									if X[i][XFor] != Geo[j][GeoFor] and XFor == GeoFor:
										delete_Geo.append(j)
										# print(j)
					count_delete = 0
					for delete in list(set(delete_Geo)):
						del Geo[delete-count_delete]
						count_delete += 1

				if X[i][-1] in CorrectN:
					if len(Geo) >= 1 :
						Gro_store,GeoF = [],[]
						for j in range(len(Geo)):
							B_count = "None"
							for k in range(len(Geo[j])):
								if Geo[j][k] != "?":
									for num in range(len(X[i])-1):
										if num == k and Geo[j][k] == X[i][num]:
											for num2 in range(len(X[i])-1):
												if num2 == num :
													continue
												for result in range(len(a[num2])-1):
													if X[i][num2] != a[num2][result] and B_count == "None":
														for lis in Geo[j] :
															GeoF.append(lis)
														GeoF[num2] = a[num2][result]
														Gro_store.append(GeoF)
														delete_Geo.append(j)
														GeoF = []
						delete_Geo = list(set(delete_Geo))
						count_delete = 0
						for delete in delete_Geo:
							del Geo[delete-count_delete]
							# print(Geo)
							count_delete += 1
						for dem in Gro_store:
							Geo.append(dem)

					else :
						for j in range(len(X[i])-1):
							if X[i][j] != Sample[j] and Sample[j] != "?":
								for k in range(len(a[j])):
									Geo_list = ['?']*j
									if a[j][k-1] != X[i][j]:
										Geo_list.append(a[j][k-1])
										while len(Geo_list) < len(Sample):
											Geo_list.append("?")
										Geo.append(Geo_list)
				# print(i+1,Geo)           # Step
			return Geo

		global S
		Geo = Candidate_Elimination(data)
		product = []

		if Geo != [S] :
			product.append(S)
			for i in Geo:
				product.append(i)

		if Geo == [S] : product = Geo

		return product

	def Checkpart(self,inp,product = [['?']]):
		score,scoreall = 0,0
		for i in range(len(inp)):
			for j in range(len(product)) :
				if inp[i] == product[j][i] : 
					score += 1
		for i in range(len(product)):
			for j in range(len(product[i])):
				if product[i][j] != "?" : scoreall += 1

		part = "UNSURE"
		if score > scoreall/2 : part = "ACCEPT"
		if score < scoreall/2 : part = "REJECT"
		return (score/3*100),part	


if __name__  == "__main__" :
	print("Lib Save")