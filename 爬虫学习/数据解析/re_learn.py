import re

result = re.findall(r"\d+", "The year 2021 saw a rise in AI technologies, with significant advancements in 2022 and beyond.")
print(result)

result_iter = re.finditer(r"\d+", "The year 2021 saw a rise in AI technologies, with significant advancements in 2022 and beyond.")
for match in result_iter:
    print(match.group(), match.span())

result_search = re.search(r"\d+", "In 2023, new breakthroughs are expected 234.")
print(result_search.group(), result_search.span())
#search只返回第一个匹配项
result_match = re.match(r"\d+", "2024 will be another year of growth."  )
print(result_match)  # match必须从字符串开头匹配，否则返回None


obj = re.compile(r"\d+")
result = obj.findall("The years 2021, 2022, and 2023")
print(result)

s = "CommandNotFoundError: <Your>24376892345468<shell> has not been properly configured to use 'conda activate'."

obj_1 = re.compile(r"<Your>(?P<number>\d+)<shell>")#(?P<number>命名捕获组)
result_1 = obj_1.finditer(s)
for match in result_1:
    print(match.group("number"))        
