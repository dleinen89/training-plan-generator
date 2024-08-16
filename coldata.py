# Specify column names
col_names = ["RegoNum", "EmployeeNum", "TrainerName", "PT_FT", "StudentLastName", "StudentFirstName",
             "BranchName", "BranchLocation", "BranchCode", "State", "Area", "QualCode", "Status",
             "CancellationDate", "BM_Name", "BM_Email", "RL_Name", "UnitsStarted", "UnitsCompleted",
             "UnitsNotComp", "CompletionRate", "TC_Start", "TC_End", "DaysRemaining", "LastAssessment",
             "LastVisit", "LastContact", "NextContact", "TLIL0007_Start", "TLIL0007_Comp", "TLIF0025_Start",
             "TLIF0025_Comp", "TLID0020_Start", "TLID0020_Comp","TLIF3003_Start","TLIF3003_Comp","AK", "TLIF0009_Start", 
             "TLIF0009_Comp", "TLID0015_Start", "TLID0015_Comp","AP", "TLIA0015_Start", "TLIA0015_Comp",
             "TLIA0004_Start","TLIA0004_Comp","AU","TLIA0008_Start", "TLIA0008_Comp", "TLIA0010_Start", 
             "TLIA0010_Comp", "TLIA3026_Start", "TLIA3026_Comp", "BB", "BSBOPS304_Start", "BSBOPS304_Comp",
             "SIRXSLS001_Start", "SIRXSLS001_Comp", "SIRXPDK001_Start", "SIRXPDK001_Comp"]

# Specify date columns
date_cols = ["CancellationDate", "TC_Start", "TC_End", "LastAssessment", "LastVisit", "LastContact", "NextContact", 
             "TLIL0007_Start", "TLIL0007_Comp", "TLIF0025_Start", "TLIF0025_Comp", "TLID0020_Start", "TLID0020_Comp",
             "TLIF3003_Start", "TLIF3003_Comp", "TLIF0009_Start", "TLIF0009_Comp", "TLID0015_Start", "TLID0015_Comp", 
             "TLIA0015_Start", "TLIA0015_Comp", "TLIA0004_Start", "TLIA0004_Comp", "TLIA0008_Start", "TLIA0008_Comp", 
             "TLIA0010_Start", "TLIA0010_Comp", "TLIA3026_Start", "TLIA3026_Comp","BSBOPS304_Start", "BSBOPS304_Comp", 
             "SIRXSLS001_Start", "SIRXSLS001_Comp", "SIRXPDK001_Start", "SIRXPDK001_Comp"]

# Specify string columns
str_cols = ["TrainerName", "PT_FT", "StudentLastName", "StudentFirstName", "BranchName", "BranchLocation", 
            "BranchCode", "State", "Area", "QualCode", "Status", "BM_Name", "BM_Email", "RL_Name", "AK", 
            "AP", "AU", "BB"]

# Specify integer columns
int_cols = ["RegoNum", "EmployeeNum", "UnitsStarted", "UnitsCompleted", "UnitsNotComp", "DaysRemaining"]

# Specify float columns
float_cols = ["CompletionRate"]