# Hyposis
Hyposis is a tool for generating list of hypothesis , Which will be considered from examples (csv file) 

## example
Create a hypothesis based on this form. (csv file)
   * "+" -> Accept 
   * "-" -> Reject

Sample | Header1 | Header2 | ... | Result
----- | ----- | ----- | ----- | ----- |
1 | - | - | - | (+,-) |
2 | - | - | - | (+,-) |
3 | - | - | - | (+,-) |
4 | - | - | - | (+,-) |

!! Always write the rejected hypothesis first. !!

### _Ex_
file name "_Sample.csv_"
Sample | Citation | Size | InLibrary | Price | Edition | Buy
----- | ----- | ----- | ----- | ----- | ----- | ----- |
1 | Some | Small | No | Affordable | One | No |
2 | Many | Big | No | Expensive | Many | Yes |
3 | Many | Medium | No | Expensive | Few | Yes |
4 | Many | Small | No | Affordable | Many | Yes |

	# Find-S
	Hypo = hypos.Hypo()
	data = Hypo.Format("Sample.csv")
	find_s = Hypo.FindS(data,CorrectP = "Yes",CorrectN = "No")
	
	# find_s -> [['Many', '?', 'No', '?', '?']]

	#-------------------------------------------------------

	# Hypothesis all
	Hypo.HypoAll(data)
	
	-> Hypothesis all
		1 ['Many', 'Big', 'No', 'Affordable', 'Few'] No
		2 ['Many', 'Big', 'No', 'Affordable', 'Few'] Yes
		3 ['Many', 'Big', 'No', 'Affordable', 'Many'] No
		4 ['Many', 'Big', 'No', 'Affordable', 'Many'] Yes
		5 ['Many', 'Big', 'No', 'Affordable', 'One'] No
		6 ['Many', 'Big', 'No', 'Affordable', 'One'] Yes
		7 ['Many', 'Big', 'No', 'Expensive', 'Few'] No
		8 ['Many', 'Big', 'No', 'Expensive', 'Few'] Yes
		9 ['Many', 'Big', 'No', 'Expensive', 'Many'] Yes
		10 ['Many', 'Big', 'No', 'Expensive', 'One'] No
		11 ['Many', 'Big', 'No', 'Expensive', 'One'] Yes
		12 ['Many', 'Medium', 'No', 'Affordable', 'Few'] No
		13 ['Many', 'Medium', 'No', 'Affordable', 'Few'] Yes
		14 ['Many', 'Medium', 'No', 'Affordable', 'Many'] No
		15 ['Many', 'Medium', 'No', 'Affordable', 'Many'] Yes
		16 ['Many', 'Medium', 'No', 'Affordable', 'One'] No
		17 ['Many', 'Medium', 'No', 'Affordable', 'One'] Yes
		18 ['Many', 'Medium', 'No', 'Expensive', 'Few'] Yes
		19 ['Many', 'Medium', 'No', 'Expensive', 'Many'] No
		20 ['Many', 'Medium', 'No', 'Expensive', 'Many'] Yes
		21 ['Many', 'Medium', 'No', 'Expensive', 'One'] No
		22 ['Many', 'Medium', 'No', 'Expensive', 'One'] Yes
		23 ['Many', 'Small', 'No', 'Affordable', 'Few'] No
		24 ['Many', 'Small', 'No', 'Affordable', 'Few'] Yes
		25 ['Many', 'Small', 'No', 'Affordable', 'Many'] Yes
		26 ['Many', 'Small', 'No', 'Affordable', 'One'] No
		27 ['Many', 'Small', 'No', 'Affordable', 'One'] Yes
		28 ['Many', 'Small', 'No', 'Expensive', 'Few'] No
		29 ['Many', 'Small', 'No', 'Expensive', 'Few'] Yes
		30 ['Many', 'Small', 'No', 'Expensive', 'Many'] No
		31 ['Many', 'Small', 'No', 'Expensive', 'Many'] Yes
		32 ['Many', 'Small', 'No', 'Expensive', 'One'] No
		33 ['Many', 'Small', 'No', 'Expensive', 'One'] Yes
		34 ['Some', 'Big', 'No', 'Affordable', 'Few'] No
		35 ['Some', 'Big', 'No', 'Affordable', 'Few'] Yes
		36 ['Some', 'Big', 'No', 'Affordable', 'Many'] No
		37 ['Some', 'Big', 'No', 'Affordable', 'Many'] Yes
		38 ['Some', 'Big', 'No', 'Affordable', 'One'] No
		39 ['Some', 'Big', 'No', 'Affordable', 'One'] Yes
		40 ['Some', 'Big', 'No', 'Expensive', 'Few'] No
		41 ['Some', 'Big', 'No', 'Expensive', 'Few'] Yes
		42 ['Some', 'Big', 'No', 'Expensive', 'Many'] No
		43 ['Some', 'Big', 'No', 'Expensive', 'Many'] Yes
		44 ['Some', 'Big', 'No', 'Expensive', 'One'] No
		45 ['Some', 'Big', 'No', 'Expensive', 'One'] Yes
		46 ['Some', 'Medium', 'No', 'Affordable', 'Few'] No
		47 ['Some', 'Medium', 'No', 'Affordable', 'Few'] Yes
		48 ['Some', 'Medium', 'No', 'Affordable', 'Many'] No
		49 ['Some', 'Medium', 'No', 'Affordable', 'Many'] Yes
		50 ['Some', 'Medium', 'No', 'Affordable', 'One'] No
		51 ['Some', 'Medium', 'No', 'Affordable', 'One'] Yes
		52 ['Some', 'Medium', 'No', 'Expensive', 'Few'] No
		53 ['Some', 'Medium', 'No', 'Expensive', 'Few'] Yes
		54 ['Some', 'Medium', 'No', 'Expensive', 'Many'] No
		55 ['Some', 'Medium', 'No', 'Expensive', 'Many'] Yes
		56 ['Some', 'Medium', 'No', 'Expensive', 'One'] No
		57 ['Some', 'Medium', 'No', 'Expensive', 'One'] Yes
		58 ['Some', 'Small', 'No', 'Affordable', 'Few'] No
		59 ['Some', 'Small', 'No', 'Affordable', 'Few'] Yes
		60 ['Some', 'Small', 'No', 'Affordable', 'Many'] No
		61 ['Some', 'Small', 'No', 'Affordable', 'Many'] Yes
		62 ['Some', 'Small', 'No', 'Affordable', 'One'] No
		63 ['Some', 'Small', 'No', 'Expensive', 'Few'] No
		64 ['Some', 'Small', 'No', 'Expensive', 'Few'] Yes
		65 ['Some', 'Small', 'No', 'Expensive', 'Many'] No
		66 ['Some', 'Small', 'No', 'Expensive', 'Many'] Yes
		67 ['Some', 'Small', 'No', 'Expensive', 'One'] No
		68 ['Some', 'Small', 'No', 'Expensive', 'One'] Yes

	#-------------------------------------------------------

	# Candidate elimination
	elimination = Hypo.Elimination(data,CorrectP = "Yes",CorrectN = "No")

	# elimination -> [['Many', '?', 'No', '?', '?'], ['Many', '?', '?', '?', '?']]

	#-------------------------------------------------------

	# Check Hypothesis
	Input = ['Many','Small','Yes','Affordable','Few']
	Result = Hypo.Checkpart(Input,product = elimination)

	# Result -> (66.66666666666666, 'ACCEPT')   "(%,Result)"


_PrABpY_