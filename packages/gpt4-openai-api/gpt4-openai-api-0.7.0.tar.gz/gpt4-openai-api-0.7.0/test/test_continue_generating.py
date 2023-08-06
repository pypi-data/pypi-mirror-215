import os

from gpt4_openai import GPT4OpenAI

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJlcm9sMTIzNDQ0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLTJHS09OenUzaVBzNVI5ZnZISGRZM3B4ViJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDU2MzMxNDAwNjUxOTMwMzgwMDgiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjg3MTgxMzcxLCJleHAiOjE2ODgzOTA5NzEsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIn0.swZuXs2yLTAgR-KlTtm6Ze_odKsyprmXvyk5YCK7GvY940e_zgoacI-LV7x_OKrxOjSfK2q_d_c6NmrYjnoefZGJQjbz2_9cgV328JrWHlVxZ7ghR3dZiNXS_XK9P8Clhok3br5IFlMu-JOe4JME_bMMwpCGCNlJt_pWq2w90NjpQMCmxCB8x71utRfvD8N_b0zvGVfBSLZDR9STff5J8Pt6-k0ze4pZc9fQrye6s3cr4VwpqPN82FYWBsQgJH_tTMwyqqMF-BH_Jzd_lxBBKrPAzdbfGc1YUZI7VkRcR2-iqzIfrmQEmruHfnAiaGpOMiUA1O_T4M9G1EEpzbiUwA"

# accessToken from https://chat.openai.com/api/auth/session
llm = GPT4OpenAI(token=token, model='gpt-4', auto_continue=True)

prompt = """
Please write a detailed and comprehensive guide to developing a small business, starting from a business idea and
going through all the necessary steps, such as writing a business plan, choosing a legal structure, obtaining financing,
choosing a location, setting up your workspace, recruiting and hiring employees, developing products and services,
marketing, sales, customer service, accounting and bookkeeping, reviewing business performance, and finally planning for
growth and expansion. Be sure to include examples, tips, and potential pitfalls to watch out for along the way.
"""
response = llm(prompt)

# GPT4 should now return all 15 different steps of the business plan, one by one
print(response)
