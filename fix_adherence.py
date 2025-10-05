#!/usr/bin/env python
"""Fix the missing except block in adherence.py"""

with open('src/api/routers/adherence.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insert the except block after line 100 (index 100, which is after "return missed_doses")
except_block = """    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving missed doses: {str(e)}"
        )

"""

# Insert after line 100 (the blank line after return)
lines.insert(101, except_block)

# Write back
with open('src/api/routers/adherence.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed! Added except block after line 100.")
