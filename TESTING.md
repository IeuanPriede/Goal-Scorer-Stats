# Testing

Once the portal was operational I set about testing it for errors and to ensure any possible errors that can be made were caught.

The deployed project live link is [HERE](https://goal-scorer-stats-d418002caeb6.herokuapp.com/) - ***Use Ctrl (Cmd) and click to open in a new window.***


The following tests were carried out to ensure the portal is working correctly

| **Feature**   | **Action**                    | **Expected Result**          | **Actual Result** |
| ------------- | ----------------------------- | ---------------------------- | ----------------- |
| Player's name input | User is asked to enter the player's name | Player's name input| Works as expected | 
| Position input | User inputs player's position from options | Player's position input | Works as expected | 
| Position input | User inputs player's position incorrectly | Error message appears | Works as expected | 
| Goals input | User inputs amount of goals | Goals input | Works as expected | 
| Goals input | User inputs amount of goals incorrectly | Error message appears | Works as expected |
| Matches input | User inputs matches played | Matches input | Works as expected |
| Matches input | User inputs matches played incorrectly | Error message appears | Works as expected |
| Minutes input | User inputs minutes played | Minutes input | Works as expected |
| Minutes input  | User inputs minutes played incorrectly | Error message appears | Works as expected |
| Minutes per goal calculated | Everything entered presented | Calculated sum presented | Works as expected |
| Press 'Enter' instead of player's name input | Press the 'Enter' button | List of players presented | Works as expected |
| List of players | Everything entered presented | List of players presented | Works as expected |
| Select player from list | User inputs player's name from the list | Player input | Works as expected |
| Select player from list | User inputs Player's name incorrectly | Error message appears | Works as expected |
| Selected player stats | Everything entered presented | Selected player's stats presented | Works as expected |
| Options | User inputs an available option | Option input | Works as expected |
| Options | User inputs an unavailable option | Error message appears | Works as expected |
| Edit | User edits player's information | Edited data input | Works as expected |
| Remove | User removes player from list | Remove input | Works as expected |
| Go back | User returns to input player's name | Back input | Works as expected |
| Exit | User exits the program | Exit input | Works as expected |

## Testing Google Sheets

I used ficticious players to add to the Google Sheets file to ensure it was connected and working properly.

## Validation

PEP8 - Python style checker - https://pep8ci.herokuapp.com/ All code validated and where lines were showing as too long they were adjusted.

### [BACK TO README](https://github.com/IeuanPriede/goal-scorer-stats/blob/main/README.md)