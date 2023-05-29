import pandas as pd
from sogongapp.models import CodingTestCase, CodingProblem

df2 = pd.read_csv('testcases.csv', encoding='EUC-KR')

for _, row in df2.iterrows():
    problem_title = row['problem']
    coding_problem = CodingProblem.objects.get(title=problem_title)

    coding_test_case = CodingTestCase.objects.create(
        problem=coding_problem,
        case_input1=row['case_input1'],
        case_input2=row['case_input2'],
        case_input3=row['case_input3'],
        case_input4=row['case_input4'],
        case_output1=row['case_output1'],
        case_output2=row['case_output2'],
        case_output3=row['case_output3'],
        case_output4=row['case_output4']
    )