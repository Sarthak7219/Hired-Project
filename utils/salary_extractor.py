import re

def extract_upper_salary(salary_text):
    # Remove leading/trailing spaces
    salary_text = salary_text.strip()
    
    # Regular expression for valid cases
    salary_pattern = re.compile(
        r"^(\d{1,2})\s*(?:-\s*(\d{1,2})|L)",  # Match 1-2 digits followed by '–' and another 1-2 digits or 'L'
        re.IGNORECASE
    )
    
    # Match the pattern
    match = salary_pattern.match(salary_text)
    if match:
        lower_range = match.group(1)  # First number
        upper_range = match.group(2)  # Second number (if available)
        
        # Return upper range if exists, otherwise lower range
        ans = int(upper_range) if upper_range else int(lower_range)
        return ans
    
    # print("salary not enough!")
    return 0  # Return None for invalid cases
