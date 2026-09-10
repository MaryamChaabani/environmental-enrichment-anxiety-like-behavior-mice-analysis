import os

import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt

#Dataset loading
df=pd.read_csv("data/behavioural_data.txt", sep=" ")

#Rename ambiguous FET variable
df=df.rename(columns={"FET.outside.time": "FET.novel_arena_time"})

#Dataset inspection
print(df.shape)
print(df.columns)
print(df["genotype"].unique())
print(df["environment"].unique())
print(df["TS"].unique())
print(df["cage"].unique())

#Dataset selection & cleaning
df_B6D2F1N=df[df["genotype"]=="B6D2F1N"] #df with only mice that we want

list_columns_to_drop=['LM.duration1', 'LM.distance1', 'LM.mistakes1', 'LM.duration2','LM.distance2', 'LM.mistakes2']
df_B6D2F1N=df_B6D2F1N.drop(columns=list_columns_to_drop) #removing columns we won't use

missing_values=df_B6D2F1N.isnull().sum() #knowing the number of null values per column

#knowing the number of trained/non-trained mice by group environment (scarce or complex)
number_of_TS_by_group=df_B6D2F1N.groupby("environment")["TS"].value_counts()


type_for_EPM_related_columns=df_B6D2F1N[["EPM.entries.OA","EPM.duration.OA","EPM.entries.CA","EPM.duration.CA","EPM.distance"]].dtypes
type_for_OFT_related_columns=df_B6D2F1N[["OFT.distance","OFT.entries","OFT.duration.center"]].dtypes
type_for_FET_related_columns=df_B6D2F1N[["FET.novel_arena_time","FET.entries","FET.distance","FET.latency"]].dtypes

#Assay-specific analysis
#Create EPM, OFT and FET DataFrames
droplist_OFT=["OFT.distance","OFT.entries","OFT.duration.center"]
droplist_EPM=["EPM.entries.OA","EPM.duration.OA","EPM.entries.CA","EPM.duration.CA","EPM.distance"]
droplist_FET=["FET.novel_arena_time","FET.entries","FET.distance","FET.latency"]

columns_to_drop_dfEPM= droplist_OFT + droplist_FET
df_EPM=df_B6D2F1N.drop(columns=columns_to_drop_dfEPM)
check_EPM=df_EPM.columns

columns_to_drop_dfOFT= droplist_FET + droplist_EPM
df_OFT=df_B6D2F1N.drop(columns=columns_to_drop_dfOFT)
check_OFT=df_OFT.columns

columns_to_drop_dfFET= droplist_EPM + droplist_OFT
df_FET=df_B6D2F1N.drop(columns=columns_to_drop_dfFET)
check_FET=df_FET.columns


#Descriptive statistics
#EPMdataframe

def descriptive_stat(variable1_complex,variable2_scarce): 
    mean_complex=round(variable1_complex.mean(),4)
    mean_scarce=round(variable2_scarce.mean(),4)
    
    median_complex=round(variable1_complex.median(),4)
    median_scarce=round(variable2_scarce.median(),4)
    
    stdev_complex=round(variable1_complex.std(),4)
    stdev_scarce=round(variable2_scarce.std(),4)
    
    return (
    f"For the complex environment, the mean is {mean_complex}, "
    f"the median is {median_complex}, and the standard deviation is {stdev_complex}.\n"
    f"For the scarce environment, the mean is {mean_scarce}, "
    f"the median is {median_scarce}, and the standard deviation is {stdev_scarce}."
)

###EPM
##duration
durationOA_complex_EPM=df_EPM[df_EPM["environment"]=="complex"]["EPM.duration.OA"]
durationOA_scarce_EPM=df_EPM[df_EPM["environment"]=="scarce"]["EPM.duration.OA"]
stat_durationOA_EPM=descriptive_stat(durationOA_complex_EPM, durationOA_scarce_EPM)

#for the group, complex environment, the mean is 45.9, its median is 54.6 and its standard deviation is 22.3611
#for the group, scarce environment, the mean is 42.9167, its median is 37.2 and its standard deviation is 29.7755

##entriesOA
entriesOA_complex_EPM=df_EPM[df_EPM["environment"]=="complex"]["EPM.entries.OA"]
entriesOA_scarce_EPM=df_EPM[df_EPM["environment"]=="scarce"]["EPM.entries.OA"]
stat_entriesOA_EPM=descriptive_stat(entriesOA_complex_EPM, entriesOA_scarce_EPM)

#for the group, complex environment, the mean is 7.5, its median is 8.0 and its standard deviation is 3.5978
#for the group, scarce environment, the mean is 6.9167, its median is 6.5 and its standard deviation is 4.3996

##distance
distance_complex_EPM=df_EPM[df_EPM["environment"]=="complex"]["EPM.distance"]
distance_scarce_EPM=df_EPM[df_EPM["environment"]=="scarce"]["EPM.distance"]
stat_distance_EPM=descriptive_stat(distance_complex_EPM, distance_scarce_EPM)

#for the group, complex environment, the mean is 9.2116, its median is 9.925 and its standard deviation is 2.612
#for the group, scarce environment, the mean is 8.8839, its median is 8.627 and its standard deviation is 1.6006


###OFTdataframe
##durationcenter
durationcenter_complex_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.duration.center"]
durationcenter_scarce_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.duration.center"]
stat_durationcenter_OFT=descriptive_stat(durationcenter_complex_OFT, durationcenter_scarce_OFT)

#for the group, complex environment, the mean is 17.03, its median is 15.75 and its standard deviation is 11.7402
#for the group, scarce environment, the mean is 13.1917, its median is 12.55 and its standard deviation is 9.1412

##entries
entries_complex_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.entries"]
entries_scarce_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.entries"]
stat_entries_OFT=descriptive_stat(entries_complex_OFT, entries_scarce_OFT)

#for the group, complex environment, the mean is 10.3, its median is 9.0 and its standard deviation is 6.929
#for the group, scarce environment, the mean is 7.9167, its median is 6.0 and its standard deviation is 5.7912

##distance
distance_complex_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.distance"]
distance_scarce_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.distance"]
stat_distance_OFT=descriptive_stat(distance_complex_OFT, distance_scarce_OFT)

#for the group, complex environment, the mean is 28.9481, its median is 29.5975 and its standard deviation is 10.3161
#for the group, scarce environment, the mean is 26.3033, its median is 26.811 and its standard deviation is 7.3532



###FETdataframe
##latency
latency_complex_FET=df_FET[df_FET["environment"]=="complex"]["FET.latency"]
latency_scarce_FET=df_FET[df_FET["environment"]=="scarce"]["FET.latency"]
stat_latency_FET=descriptive_stat(latency_complex_FET,latency_scarce_FET)

#for the group, complex environment, the mean is 124.85, its median is 59.25 and its standard deviation is 158.5405
#for the group, scarce environment, the mean is 224.8667, its median is 204.1 and its standard deviation is 119.5851

#novel arena time
novel_arena_time_complex_FET=df_FET[df_FET["environment"]=="complex"]["FET.novel_arena_time"]
novel_arena_time_scarce_FET=df_FET[df_FET["environment"]=="scarce"]["FET.novel_arena_time"]
stat_novel_arena_time_FET=descriptive_stat(novel_arena_time_complex_FET,novel_arena_time_scarce_FET)

#for the group, complex environment, the mean is 695.19, its median is 690.75 and its standard deviation is 55.5618
#for the group, scarce environment, the mean is 702.175, its median is 688.25 and its standard deviation is 123.5322

#distance
distance_complex_FET=df_FET[df_FET["environment"]=="complex"]["FET.distance"]
distance_scarce_FET=df_FET[df_FET["environment"]=="scarce"]["FET.distance"]
stat_distance_FET=descriptive_stat(distance_complex_FET,distance_scarce_FET)

#for the group, complex environment, the mean is 17.0227, its median is 20.4305 and its standard deviation is 7.2005
#for the group, scarce environment, the mean is 12.1955, its median is 11.1945 and its standard deviation is 8.0092



###Compare complex vs scarce groups

#def of statistical test we are going to use 

#FISHER TEST
def fisher_f_test(group1, group2): 
    # 1. Calculate variances
    var1 = group1.var()
    var2 = group2.var()

    # 2. Sample sizes
    n1 = len(group1)
    n2 = len(group2)

    # 3. Put the largest variance in the numerator
    if var1 >= var2:
        F = var1 / var2
        df1 = n1 - 1
        df2 = n2 - 1
    else:
        F = var2 / var1
        df1 = n2 - 1
        df2 = n1 - 1

    # 4. Two-sided p-value
    pvalue =min(1,2 * stats.f.sf(F, df1, df2))

    # 5. Return results
    return F, pvalue


#STUDENT-T TEST
#Bilateral
def student_t_test_bilateral(group1,group2): 
    #for the distance variable
    #H0 :  μ₁ = μ₂
    #H1 :  μ₁ != μ₂
    print(f"both variances are equal, let's use the student-t test")
    
    result_student=stats.ttest_ind(group1,group2,equal_var=True)
    pvalue_student=result_student.pvalue
    
    if pvalue_student >= 0.05: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is < 0.05, so we reject H0 and the two group means are significantly different ")

    return result_student.statistic, result_student.pvalue

#Unilateral 
def student_t_test_alternative_greater(group1,group2): 
    #for the EPM, OFT and FET(novel arena time) test
    #H0 :  μ₁ <= μ₂
    #H1 :  μ₁ > μ₂
    print(f"both variances are equal, let's use the student-t test")
    
    result_student=stats.ttest_ind(group1,group2,equal_var=True,alternative="greater")
    pvalue_student=result_student.pvalue
    
    if pvalue_student >= 0.05: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is < 0.05, so we reject H0 and μ₁ > μ₂ ")

    return result_student.statistic, result_student.pvalue

def student_t_test_alternative_less(group1,group2): 
    #for the FET (latency) test
    #H0 :  μ₁ >= μ₂
    #H1 :  μ₁ < μ₂
    print(f"both variances are equal, let's use the student-t test")
    
    result_student=stats.ttest_ind(group1,group2,equal_var=True,alternative="less")
    pvalue_student=result_student.pvalue
    
    if pvalue_student >= 0.05: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the student-t test is {pvalue_student} and is < 0.05, so we reject H0 and μ₁ < μ₂ ")
    
    return result_student.statistic, result_student.pvalue

#WELCH TEST
#bilateral
def welch_test_bilateral(group1,group2): 
    #for the distance variable
    #H0 :  μ₁ = μ₂
    #H1 :  μ₁ != μ₂
    
    print(f"both variances can't be considered as equal, let's use the welch test")
    
    result_welch=stats.ttest_ind(group1,group2,equal_var=False)
    pvalue_welch=result_welch.pvalue
    
    if pvalue_welch >= 0.05: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is < 0.05, so we reject H0 and the two group means are significantly different")
    
    return result_welch.statistic, result_welch.pvalue

#unilateral
def welch_test_alternative_greater(group1,group2): 
    #for the EPM, OFT and FET(novel arena time) test
    #H0 :  μ₁ <= μ₂
    #H1 :  μ₁ > μ₂

    print(f"both variances can't be considered as equal, let's use the welch test")
    
    result_welch=stats.ttest_ind(group1,group2,equal_var=False,alternative="greater")
    pvalue_welch=result_welch.pvalue
    
    if pvalue_welch >= 0.05: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is < 0.05, so we reject H0 and μ₁ > μ₂")
    
    return result_welch.statistic, result_welch.pvalue

def welch_test_alternative_less(group1,group2): 
    #for the FET (latency) test
    #H0 :  μ₁ >= μ₂
    #H1 :  μ₁ < μ₂
    
    print(f"both variances can't be considered as equal, let's use the welch test")
    
    result_welch=stats.ttest_ind(group1,group2,equal_var=False,alternative="less")
    pvalue_welch=result_welch.pvalue
    
    if pvalue_welch >= 0.05: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is >= 0.05, so we don't reject H0")
    else: 
        print(f"the pvalue of the welch test is {pvalue_welch} and is < 0.05, so we reject H0 and μ₁ < μ₂")
   
    return result_welch.statistic, result_welch.pvalue

#WILCOXON-MANN-WHITNEY TEST
#bilateral
#for the distance variable
def Wilcoxon_Mann_Whitney_test_bilateral(group1,group2): 
    # H0: the two groups have the same distribution
    # H1: the two groups have different distributions
    
    print(f"at least one of the two datasets is not compatible with a normal distribution, we have to use the Wilcoxon-Mann-Whitney test")
    
    result_MannW=stats.mannwhitneyu(group1, group2, alternative="two-sided")
    pvalue_MannW=result_MannW.pvalue
    
    if pvalue_MannW >= 0.05 : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is >= 0.05, so we don't reject H0")
    else : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is < 0.05, so we reject H0")

    return result_MannW.statistic, result_MannW.pvalue

#unilateral
def Wilcoxon_Mann_Whitney_test_alternative_greater(group1,group2): 
    #H0: values in group1 do not tend to be greater than values in group2
    #H1: values in group1 tend to be greater than values in group2
    
    print(f"at least one of the two datasets is not compatible with a normal distribution, we have to use the Wilcoxon-Mann-Whitney test")
    
    result_MannW=stats.mannwhitneyu(group1, group2, alternative="greater")
    pvalue_MannW=result_MannW.pvalue
    
    if pvalue_MannW >= 0.05 : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is >= 0.05, so we don't reject H0")
    else : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is < 0.05, so we reject H0")

    return result_MannW.statistic, result_MannW.pvalue

def Wilcoxon_Mann_Whitney_test_alternative_less(group1,group2): 
    #H0: values in group1 do not tend to be lower than values in group2
    #H1: values in group1 tend to be lower than values in group2
    
    print(f"at least one of the two datasets is not compatible with a normal distribution, we have to use the Wilcoxon-Mann-Whitney test")
    
    result_MannW=stats.mannwhitneyu(group1, group2, alternative="less")
    pvalue_MannW=result_MannW.pvalue
    
    if pvalue_MannW >= 0.05 : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is >= 0.05, so we don't reject H0")
    else : 
        print(f"the pvalue for the Wilcoxon-Mann-Whitney test is {pvalue_MannW} and is < 0.05, so we reject H0")

    return result_MannW.statistic, result_MannW.pvalue

#PRINCIPAL FUNCTION FOR VARIABLES WITH THE ALTERNATIVE HYPOTHESIS: COMPLEX > SCARCE
def complex_vs_scarce_groups_EPM_OFT(group1,group2): 
    #verify if distribution of data can be considered normal 
    #Shapiro_test
    group1_distribution=stats.shapiro(group1)
    pvalue_group1=group1_distribution.pvalue
    
    group2_distribution=stats.shapiro(group2)
    pvalue_group2=group2_distribution.pvalue
    
    print(f"for the shapiro test, p-value group1 = {pvalue_group1} and p-value group2 = {pvalue_group2}")
    
    if pvalue_group1>= 0.05 and pvalue_group2 >= 0.05 : #both datasets are compatible with a normal distribution
        print(f"both dataset are compatible with a normal distribution, let's use the Fisher test to verify equality of variance")
        F_value, pvalue_fisher=fisher_f_test(group1,group2)
        print(f"the pvalue for the fisher test is {pvalue_fisher}")
        
        if pvalue_fisher >=0.05 : #both variances are equal  
            #Student-t test 
            statistic_student, pvalue_student=student_t_test_alternative_greater(group1,group2)
            return "student-t test", statistic_student, pvalue_student
            
        else : #both variances can't be considered as equal
            #Welch test
            statistic_welch, pvalue_welch=welch_test_alternative_greater(group1,group2)
            return "welch test", statistic_welch, pvalue_welch
        
    else : #at least one of the two datasets is not compatible with a normal distribution
        #Mann-Whitney test
        statistic_MannW, pvalue_MannW =Wilcoxon_Mann_Whitney_test_alternative_greater(group1,group2)
        return "Wilcoxon-Mann-Whitney test", statistic_MannW, pvalue_MannW 

#PRINCIPAL FUNCTION FOR FET TEST
def complex_vs_scarce_groups_FET_latency(group1,group2):
    #verify if distribution of data can be considered normal 
    #Shapiro_test
    group1_distribution = stats.shapiro(group1)
    pvalue_group1 = group1_distribution.pvalue
       
    group2_distribution = stats.shapiro(group2)
    pvalue_group2 = group2_distribution.pvalue
       
    print(f"for the shapiro test, p-value group1 = {pvalue_group1} and p-value group2 = {pvalue_group2}")
          
    if pvalue_group1 >= 0.05 and pvalue_group2 >= 0.05:
        print("both datasets are compatible with a normal distribution, let's use the Fisher test to verify equality of variance")

        F_value, pvalue_fisher = fisher_f_test(group1,group2)
        print(f"the pvalue for the fisher test is {pvalue_fisher}")
           
        if pvalue_fisher >= 0.05:
            # Student-t test
            statistic_student, pvalue_student = student_t_test_alternative_less(group1,group2)
            return "student-t test", statistic_student, pvalue_student
            
        else:
            # Welch test
            statistic_welch, pvalue_welch = welch_test_alternative_less(group1,group2)
            return "welch test", statistic_welch, pvalue_welch
        
    else:
        # Mann-Whitney test
        statistic_MannW, pvalue_MannW = Wilcoxon_Mann_Whitney_test_alternative_less(group1,group2)
        return "Wilcoxon-Mann-Whitney test", statistic_MannW, pvalue_MannW

#PRINCIPAL FUNCTION FOR THE DISTANCE VARIABLE OF EACH TEST 
def compare_two_groups_bilateral(group1, group2):
    #verify if distribution of data can be considered normal 
    #Shapiro_test
    group1_distribution = stats.shapiro(group1)
    pvalue_group1 = group1_distribution.pvalue
       
    group2_distribution = stats.shapiro(group2)
    pvalue_group2 = group2_distribution.pvalue
       
    print(f"for the shapiro test, p-value group1 = {pvalue_group1} and p-value group2 = {pvalue_group2}")
          
    if pvalue_group1 >= 0.05 and pvalue_group2 >= 0.05:
        print("both datasets are compatible with a normal distribution, let's use the Fisher test to verify equality of variance")

        F_value, pvalue_fisher = fisher_f_test(group1,group2)
        print(f"the pvalue for the fisher test is {pvalue_fisher}")
           
        if pvalue_fisher >= 0.05:
            # Student-t test
            statistic_student, pvalue_student = student_t_test_bilateral(group1,group2)
            return "student-t test", statistic_student, pvalue_student
            
        else:
            # Welch test
            statistic_welch, pvalue_welch = welch_test_bilateral(group1,group2)
            return "welch test", statistic_welch, pvalue_welch
        
    else:
        # Mann-Whitney test
        statistic_MannW, pvalue_MannW = Wilcoxon_Mann_Whitney_test_bilateral(group1,group2)
        return "Wilcoxon-Mann-Whitney test", statistic_MannW, pvalue_MannW


###Create groups 

#EPM
#EPMdurationOA
durationOA_complex_environment_EPM=df_EPM[df_EPM["environment"] == "complex"]["EPM.duration.OA"]
durationOA_scarce_environment_EPM=df_EPM[df_EPM["environment"] == "scarce"]["EPM.duration.OA"]

#EPMentriesOA
entriesOA_complex_environment_EPM=df_EPM[df_EPM["environment"]=="complex"]["EPM.entries.OA"]
entriesOA_scarce_environment_EPM=df_EPM[df_EPM["environment"]=="scarce"]["EPM.entries.OA"]

#EPMdistance
distance_complex_environment_EPM=df_EPM[df_EPM["environment"]=="complex"]["EPM.distance"]
distance_scarce_environment_EPM=df_EPM[df_EPM["environment"]=="scarce"]["EPM.distance"]


#OFT
#OFTduration center
durationcenter_complex_environment_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.duration.center"]
durationcenter_scarce_environment_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.duration.center"]

#OFTentries
entries_complex_environment_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.entries"]
entries_scarce_environment_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.entries"]

#OFTdistance
distance_complex_environment_OFT=df_OFT[df_OFT["environment"]=="complex"]["OFT.distance"]
distance_scarce_environment_OFT=df_OFT[df_OFT["environment"]=="scarce"]["OFT.distance"]


#FET
#FETlatency
latency_complex_environment_FET=df_FET[df_FET["environment"]=="complex"]["FET.latency"]
latency_scarce_environment_FET=df_FET[df_FET["environment"]=="scarce"]["FET.latency"]

#FET novel arena time
novel_arena_time_complex_environment_FET=df_FET[df_FET["environment"]=="complex"]["FET.novel_arena_time"]
novel_arena_time_scarce_environment_FET=df_FET[df_FET["environment"]=="scarce"]["FET.novel_arena_time"]

#FETdistance
distance_distribution_complex_environment_FET=df_FET[df_FET["environment"]=="complex"]["FET.distance"]
distance_distribution_scarce_environment_FET=df_FET[df_FET["environment"]=="scarce"]["FET.distance"]

###Apply tests
### colors in the terminal
#BLUE = "\033[94m"
#RESET = "\033[0m"

#EPM
print("\033[94mRESULTS FOR THE EPM TEST:\033[0m")
print("Result for the variable - duration in open arms - : ")
result_EPM_durationOA=complex_vs_scarce_groups_EPM_OFT(durationOA_complex_environment_EPM,durationOA_scarce_environment_EPM)

print("Result for the variable - entries in open arms - : ")
result_EPM_entriesOA=complex_vs_scarce_groups_EPM_OFT(entriesOA_complex_environment_EPM,entriesOA_scarce_environment_EPM)

print("Result for the locomotor control variable - distance - : ")
result_EPM_distance=compare_two_groups_bilateral(distance_complex_environment_EPM,distance_scarce_environment_EPM)

#OFT 
print("\033[94mRESULTS FOR THE OFT TEST:\033[0m")
print("Result for the variable - duration at the center - : ")
result_OFT_durationcenter=complex_vs_scarce_groups_EPM_OFT(durationcenter_complex_environment_OFT,durationcenter_scarce_environment_OFT) 

print("Result for the variable - entries - : ")
result_OFT_entries=complex_vs_scarce_groups_EPM_OFT(entries_complex_environment_OFT,entries_scarce_environment_OFT)

print("Result for the locomotor control variable - distance - : ")
result_OFT_distance=compare_two_groups_bilateral(distance_complex_environment_OFT,distance_scarce_environment_OFT)

#FET
print("\033[94mRESULTS FOR THE FET TEST:\033[0m")
print("Result for the variable - latency - : ")
result_FET_latency=complex_vs_scarce_groups_FET_latency(latency_complex_environment_FET,latency_scarce_environment_FET)

print("Result for the variable - time spent in the novel arena - : ")
result_FET_novel_arena_time=complex_vs_scarce_groups_EPM_OFT(novel_arena_time_complex_environment_FET,novel_arena_time_scarce_environment_FET)

print("Result for the locomotor control variable - distance - : ")
result_FET_distance=compare_two_groups_bilateral(distance_distribution_complex_environment_FET,distance_distribution_scarce_environment_FET)



### Assess potential touchscreen-training effects
# H0: The trained and non-trained groups have the same mean/distribution.
# H1: The trained and non-trained groups have different means/distributions.

###Create groups

#EPM
#EPMdurationOA
durationOA_trained_EPM=df_EPM[df_EPM["TS"] == "trained"]["EPM.duration.OA"]
durationOA_non_trained_EPM=df_EPM[df_EPM["TS"] == "non-trained"]["EPM.duration.OA"]

#EPMentriesOA
entriesOA_trained_EPM=df_EPM[df_EPM["TS"]=="trained"]["EPM.entries.OA"]
entriesOA_non_trained_EPM=df_EPM[df_EPM["TS"]=="non-trained"]["EPM.entries.OA"]

#OFT
#OFTduration center
durationcenter_trained_OFT=df_OFT[df_OFT["TS"]=="trained"]["OFT.duration.center"]
durationcenter_non_trained_OFT=df_OFT[df_OFT["TS"]=="non-trained"]["OFT.duration.center"]

#OFTentries
entries_trained_OFT=df_OFT[df_OFT["TS"]=="trained"]["OFT.entries"]
entries_non_trained_OFT=df_OFT[df_OFT["TS"]=="non-trained"]["OFT.entries"]

#FET
#FETlatency
latency_trained_FET=df_FET[df_FET["TS"]=="trained"]["FET.latency"]
latency_non_trained_FET=df_FET[df_FET["TS"]=="non-trained"]["FET.latency"]

#FET novel arena time
novel_arena_time_trained_FET=df_FET[df_FET["TS"]=="trained"]["FET.novel_arena_time"]
novel_arena_time_non_trained_FET=df_FET[df_FET["TS"]=="non-trained"]["FET.novel_arena_time"]

###APPLY TESTS
###colors in the terminal
#GREEN = "\033[92m"
#RESET = "\033[0m"

print("\033[92mRESULTS FOR TOUCHSCREEN TRAINING EFFECTS:\033[0m")

#EPM
print("\033[92mRESULTS FOR THE EPM TEST:\033[0m")
print("Result for the variable - duration in open arms - : ")
result_EPM_durationOA_training=compare_two_groups_bilateral(durationOA_trained_EPM,durationOA_non_trained_EPM)

print("Result for the variable - entries in open arms - : ")
result_EPM_entriesOA_training=compare_two_groups_bilateral(entriesOA_trained_EPM,entriesOA_non_trained_EPM)

#OFT
print("\033[92mRESULTS FOR THE OFT TEST:\033[0m")
print("Result for the variable - duration in center - : ")
result_OFT_durationcenter_training=compare_two_groups_bilateral(durationcenter_trained_OFT,durationcenter_non_trained_OFT)

print("Result for the variable - entries - : ")
result_OFT_entries_training=compare_two_groups_bilateral(entries_trained_OFT,entries_non_trained_OFT)

#FET
print("\033[92mRESULTS FOR THE FET TEST:\033[0m")
print("Result for the variable - latency - : ")
result_FET_latency_training=compare_two_groups_bilateral(latency_trained_FET,latency_non_trained_FET)

print("Result for the variable - time spent in the novel arena - : ")
result_FET_novel_arena_time_training=compare_two_groups_bilateral(novel_arena_time_trained_FET,novel_arena_time_non_trained_FET)

###Figure 

os.makedirs("figures", exist_ok=True) #Creates a folder to store all the figures

def add_significance_bar(group1,group2,pvalue): 
    #Add a significance bar and significance stars above two boxplots.
    # Parameters:
    #group1 : first group of numerical values
    #group2 : second group of numerical values
    #pvalue : p-value returned by the statistical test
    
    max_value=max(group1.max(),group2.max()) #to place significance bar above data
    y=max_value*1.02 ##to place significance bar above data, and 2% above the highest observed value
    
    if pvalue < 0.001:
        stars = "***"
    elif pvalue < 0.01:
        stars = "**"
    elif pvalue < 0.05:
        stars = "*"
    else:
        stars = "ns"
        
    #Draw the significance bar
    #x positions : 1 = first boxplot, 2 = second boxplot
    #y coordinates create a bar shape by linking max_value for the 1st and 2nd group
    
    plt.plot([1, 1, 2, 2],[y,y+y*0.02,y+y*0.02,y])
    
    #x = 1.5 places the text exactly between boxplots 1 and 2
    #y * 1.03 places the text slightly above the bar
    #"center" to center the text horizontally
    plt.text(1.5,y*1.03,stars,ha="center")

##Figures assessing potential training effects
#EPM test
#Duration in open arms
plt.figure()  

plt.boxplot([durationOA_complex_environment_EPM,durationOA_scarce_environment_EPM])
plt.xticks([1, 2], ["Complex", "Scarce"])
plt.ylabel("Duration in open arms (s)")
plt.title("EPM - Open arm duration according to housing environment: complex vs scarce")
add_significance_bar(durationOA_complex_environment_EPM,durationOA_scarce_environment_EPM,result_EPM_durationOA[2])

plt.savefig("figures/EPM_duration_open_arms_environment.png", bbox_inches="tight")
plt.close()

#Entries in open arms
plt.figure() 

plt.boxplot([entriesOA_complex_environment_EPM,entriesOA_scarce_environment_EPM])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Number of entries into open arms")
plt.title("EPM - Entries in open arms according to housing environment: complex vs scarce")

add_significance_bar(entriesOA_complex_environment_EPM,entriesOA_scarce_environment_EPM,result_EPM_entriesOA[2])

plt.savefig("figures/EPM_entries_in_open_arms_environment.png", bbox_inches="tight")
plt.close()

#Distance
plt.figure() 

plt.boxplot([distance_complex_environment_EPM,distance_scarce_environment_EPM])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Distance travelled (unit not specified)")
plt.title("EPM - Distance travelled according to housing environment: complex vs scarce")

add_significance_bar(distance_complex_environment_EPM,distance_scarce_environment_EPM,result_EPM_distance[2])

plt.savefig("figures/EPM_distance_environment.png", bbox_inches="tight")
plt.close()

#OFT test
#Duration at the center
plt.figure() 

plt.boxplot([durationcenter_complex_environment_OFT,durationcenter_scarce_environment_OFT])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Time spent in the center zone (s)")
plt.title("Open Field Test - Time spent in the center zone of the arena according to housing environment: complex vs scarce")

add_significance_bar(durationcenter_complex_environment_OFT,durationcenter_scarce_environment_OFT,result_OFT_durationcenter[2])

plt.savefig("figures/OFT_duration_center_environment.png", bbox_inches="tight")
plt.close()

#Entries at the center of the arena
plt.figure() 

plt.boxplot([entries_complex_environment_OFT,entries_scarce_environment_OFT])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Number of entries into the center zone of the arena")
plt.title("Open Field Test - Entries at the center of the arena according to housing environment: complex vs scarce")

add_significance_bar(entries_complex_environment_OFT,entries_scarce_environment_OFT,result_OFT_entries[2])

plt.savefig("figures/OFT_entries_center_environment.png", bbox_inches="tight")
plt.close()

#Distance
plt.figure() 

plt.boxplot([distance_complex_environment_OFT,distance_scarce_environment_OFT])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Distance travelled (unit not specified)")
plt.title("OFT - Distance travelled according to housing environment: complex vs scarce")

add_significance_bar(distance_complex_environment_OFT,distance_scarce_environment_OFT,result_OFT_distance[2])

plt.savefig("figures/OFT_distance_environment.png", bbox_inches="tight")
plt.close()

#FET Test
#Latency
plt.figure()

plt.boxplot([latency_complex_environment_FET,latency_scarce_environment_FET])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Latency to enter the novel arena (s)")
plt.title("Free Exploration Test - Latency to enter the novel arena according to housing environment: complex vs scarce")

add_significance_bar(latency_complex_environment_FET,latency_scarce_environment_FET,result_FET_latency[2])

plt.savefig("figures/FET_latency_to_enter_novelarena_environment.png", bbox_inches="tight")
plt.close()

#Novel arena time
plt.figure()

plt.boxplot([novel_arena_time_complex_environment_FET,novel_arena_time_scarce_environment_FET])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Time spent in the novel arena (s)")
plt.title("Free Exploration Test - Time spent in the novel arena according to housing environment: complex vs scarce")

add_significance_bar(novel_arena_time_complex_environment_FET,novel_arena_time_scarce_environment_FET,result_FET_novel_arena_time[2])

plt.savefig("figures/FET_time_spent_in_the_novelarena_environment.png", bbox_inches="tight")
plt.close()

#Distance
plt.figure() 

plt.boxplot([distance_distribution_complex_environment_FET,distance_distribution_scarce_environment_FET])
plt.xticks([1,2],["Complex", "Scarce"])
plt.ylabel("Distance travelled (unit not specified)")
plt.title("FET - Distance travelled according to housing environment: complex vs scarce")

add_significance_bar(distance_distribution_complex_environment_FET,distance_distribution_scarce_environment_FET,result_FET_distance[2])

plt.savefig("figures/FET_distance_environment.png", bbox_inches="tight")
plt.close()

##Figure to assess potential training effect
#EPM test
#Duration in open arms
plt.figure()  

plt.boxplot([durationOA_trained_EPM,durationOA_non_trained_EPM])
plt.xticks([1, 2], ["Trained", "Non-trained"])
plt.ylabel("Time spent in open arms (s)")
plt.title("EPM - Time spent in open arms depending on touchscreen training for the Cognitive Judgment Bias task")
add_significance_bar(durationOA_trained_EPM,durationOA_non_trained_EPM,result_EPM_durationOA_training[2])

plt.savefig("figures/EPM_duration_open_arms_training.png", bbox_inches="tight")
plt.close()

#Entries in open arms
plt.figure() 

plt.boxplot([entriesOA_trained_EPM,entriesOA_non_trained_EPM])
plt.xticks([1,2],["Trained", "Non-trained"])
plt.ylabel("Number of entries into open arms")
plt.title("EPM - Entries in open arms depending on touchscreen training for the Cognitive Judgment Bias task")

add_significance_bar(entriesOA_trained_EPM,entriesOA_non_trained_EPM,result_EPM_entriesOA_training[2])

plt.savefig("figures/EPM_entries_in_open_arms_training.png", bbox_inches="tight")
plt.close()

#OFT test
#Duration at the center
plt.figure() 

plt.boxplot([durationcenter_trained_OFT,durationcenter_non_trained_OFT])
plt.xticks([1,2],["Trained", "Non-trained"])
plt.ylabel("Time spent in the center zone of the arena (s)")
plt.title("Open Field Test - Time spent in the center zone of the arena depending on touchscreen training for the Cognitive Judgment Bias task")

add_significance_bar(durationcenter_trained_OFT,durationcenter_non_trained_OFT,result_OFT_durationcenter_training[2])

plt.savefig("figures/OFT_duration_center_training.png", bbox_inches="tight")
plt.close()

#Entries at the center of the arena
plt.figure() 

plt.boxplot([entries_trained_OFT,entries_non_trained_OFT])
plt.xticks([1,2],["Trained", "Non-trained"])
plt.ylabel("Number of entries into the center zone of the arena")
plt.title("Open Field Test - Entries at the center of the arena depending on touchscreen training for the Cognitive Judgment Bias task")

add_significance_bar(entries_trained_OFT,entries_non_trained_OFT,result_OFT_entries_training[2])

plt.savefig("figures/OFT_entries_center_training.png", bbox_inches="tight")
plt.close()

#FET Test
#Latency
plt.figure()

plt.boxplot([latency_trained_FET,latency_non_trained_FET])
plt.xticks([1,2],["Trained", "Non-trained"])
plt.ylabel("Latency to enter the novel arena (s)")
plt.title("Free Exploration Test - Latency to enter the novel arena depending on touchscreen training for the Cognitive Judgment Bias task")

add_significance_bar(latency_trained_FET,latency_non_trained_FET,result_FET_latency_training[2])

plt.savefig("figures/FET_latency_to_enter_novelarena_training.png", bbox_inches="tight")
plt.close()

#Novel arena time
plt.figure()

plt.boxplot([novel_arena_time_trained_FET,novel_arena_time_non_trained_FET])
plt.xticks([1,2],["Trained", "Non-trained"])
plt.ylabel("Time spent in the novel arena (s)")
plt.title("Free Exploration Test - Time spent in the novel arena depending on touchscreen training for the Cognitive Judgment Bias task")

add_significance_bar(novel_arena_time_trained_FET,novel_arena_time_non_trained_FET,result_FET_novel_arena_time_training[2])

plt.savefig("figures/FET_time_spent_in_the_novelarena_training.png", bbox_inches="tight")
plt.close()

