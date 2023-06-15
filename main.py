import dbbact_api_call

dbbact_api_call.find_human_associated_bacteria()

try:
    dbbact_api_call.compare_phage()

except Exception as e:
    print(f"Damn, didn't find these bacteria you gave me, make sure you wrote them the right way: {e}")
