STARCODER_BETA = """

col_name,data_type,comment
Source,string, The insurance company that submitted the claim, only used when insurance provider iinformation is needed
NetworkID,int,
DiagCode,string,
DiagDesc,string, described in text form the diagnosis
CPTDesc,string, service or procedure rendered for the claim
IncurredDate,date, the date the serviced was rendered
SubmittedDate,date, the date the claim was submitted
PaidDate,date,
SubmittedAmount,int,
PaidAmount,int,
ClaimStatus,string,
ServicingProviderNPI,bigint,
ServicingProviderName,string,
BillingProviderNPI,bigint,
BillingProviderName,string,
PlaceofService,string, used for where the patient was treated
DrugName,string, The prescribed drug
DrugClass,string, The type of drug prescribed
GPI,bigint, 
NDC,string,
DaysSupplied,int, the number of days the drug was supplied
LengthOfStay,int, the number of days the patient was admitted
PatientFirstName,string, 
PatientLastName,string,
PatientGender,string,
PatientDateOfBirth,date, use this today's age minus this column for age related questions
PatientAddress,string,
PatientState,string, the full name of the patient state
PatientZIP,int, the patient zip code
PatientID,string.

When completing the code request use the describe listed above and the examples following the describe, do not make up column names and do not place additional conditions.
"""
