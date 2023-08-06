STARCODER_BETA = """

col_name,data_type,comment
Source,string,
NetworkID,int,
DiagCode,string,
DiagDesc,string,
CPTDesc,string,
IncurredDate,date,
SubmittedDate,date,
PaidDate,date,
SubmittedAmount,int,
PaidAmount,int,
ClaimStatus,string,
ServicingProviderNPI,bigint,
ServicingProviderName,string,
BillingProviderNPI,bigint,
BillingProviderName,string,
PlaceofService,string,
DrugName,string,
DrugClass,string,
GPI,bigint,
NDC,string,
DaysSupplied,int,
LengthOfStay,int,
PatientFirstName,string,
PatientLastName,string,
PatientGender,string,
PatientDateOfBirth,date,
PatientAddress,string,
PatientState,string,
PatientZIP,int,
PatientID,string,

"""
STARCODER_BETA += """
 When answering the request use the information listed above only, do not make up column names and do not place additional conditions
    """
