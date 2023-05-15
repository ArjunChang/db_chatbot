import re


def extract_code(string):
    pattern = r"```(?:sql)?([\s\S]*?)```"
    match = re.search(pattern, string, re.IGNORECASE)
    
    if match:
        code = match.group(1)
        return code.strip()  # Optional: Remove leading/trailing whitespace
    else:
        return None