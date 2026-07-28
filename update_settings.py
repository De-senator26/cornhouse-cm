import os
import re

settings_file = 'cornhouse/settings.py'

with open(settings_file, 'r') as f:
    content = f.read()

# ---- 1. Add imports if missing ----
if 'import dj_database_url' not in content:
    # Insert after the last import line
    lines = content.split('\n')
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and (line.startswith('import ') or line.startswith('from ')):
            if 'import dj_database_url' not in content:
                new_lines.append('import dj_database_url')
                inserted = True
            if 'from decouple import config' not in content:
                new_lines.append('from decouple import config')
                inserted = True
    if not inserted:
        # fallback: add after the docstring
        new_lines.insert(2, 'import dj_database_url')
        if 'from decouple import config' not in content:
            new_lines.insert(3, 'from decouple import config')
    content = '\n'.join(new_lines)

# ---- 2. Replace DATABASES block (safe method) ----
# Find the start of DATABASES =
start = content.find('DATABASES =')
if start != -1:
    # Find the opening brace
    brace_start = content.find('{', start)
    if brace_start != -1:
        # Count braces to find the matching closing brace
        brace_count = 0
        i = brace_start
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
            i += 1
        else:
            end = len(content)
        # Replace from start to end with new DATABASES
        new_db = """DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}"""
        content = content[:start] + new_db + content[end:]

# ---- 3. Update ALLOWED_HOSTS ----
# Replace the existing ALLOWED_HOSTS line with ['*']
pattern = r"ALLOWED_HOSTS\s*=\s*\[.*?\]"
content = re.sub(pattern, "ALLOWED_HOSTS = ['*']", content, flags=re.DOTALL)

# Write back
with open(settings_file, 'w') as f:
    f.write(content)

print("✅ settings.py updated safely!")
