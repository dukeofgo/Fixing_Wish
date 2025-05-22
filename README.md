# Fixing_Wish

<br>

This take-home technical assessment involved fixing several issues that caused the web application to malfunction.
Problems were identified, and appropriate solutions have been applied to restore the application's expected behavior and improve its functionality.

<br>
<br>

## Description on Commits

| Commit                                    | Problems                                                      | Solutions
|-------------------------------------------|---------------------------------------------------------------|-----------------------
| Fix "User Dashboard"                      | User object retrieved by .get() does not support indexing     | Remove indexing and pass the user object directly      
| Fix like & unlike buttons                 | Incomplete URLs path were assigned in templates               | Reassign correct URLs path
| Remove stray F-string                     | Unused f-string                                               | Remove f-string 
| Fix incorrect redirect URL                | Redirect URL was assigned incorectly                          | Reassign redirect URL to the correct URL
| Prevent future dates in birthday input    | Birthday fields can be set to future dates                    | Limiting birthday input from current date to past only
| Avoid hardcoding to ensure reusability    | Hard-coding User model                                        | Replace with self to accomodate different manager instances
| Implement .first() for clarity            | Not utilizing .first() introduces many redundant code         | Implement .first() 
| Remove redundant code & simplify logic    | Duplicated password validation and redirect code              | Remove the duplication and redundancy
| Incorrect redirect url                    | Incorrect redirect url                                        | Replace with correct redirect url
