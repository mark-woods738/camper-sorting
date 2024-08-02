# How to Use 
## Getting the Data
<!-- TODO get link to website -->
1. Go to Camp Brains.
2. Hover over `Reports` in the menu on the left side of the screen.
3. Click on `Camper Ad Hoc Reports`. 
4. Click on `View List`. This will show you a list of custom reports.
5. Select and open the `Activity Preference List 2 (Shortened)` report.
6. On the right, there is a filters pane. Inside the filters pane, find the variable called `Session name`. Change the varaible in the dropdown menu directly below session name to the desired Harbour Camp week, e.g. `Harbour 7 - Sr. Coed`.
7. Within the filters pane, click apply.
8. Export the file, selecting .csv (Comma Separated Values) as the desired file format. (The export icon looks like a page with writing on it with an arrow coming out of it).
9. Move the downloaded file into this folder and name it `camper-selections.csv`.

## Customising the Available Activities
1. Open `activity-details.csv`.
2. Alter the information to reflect that of the week. It must adhere to the following rules. An example can be found in `examples/example-activity-details.csv` : 
- Each line represents an activity block. Therefore, the file should have as many lines as activity blocks desired.
- Each line will contain all the activities for a given activity block. For example `archery, 10, riflery, 5` means that archery and riflery are the only activities available. Additionally, archery has 10 places and riflery has 5. **CAUTION each activity must be declared as a pair `name, capacity` if only one of these is present, it will not work.**
- The activities available in each activity block may vary. For example, archery may not be available in block 2 but available in blocks 1 and 3.
- **CAUTION the names of the activies must be spelt the same as those in the `camper-selections.csv` file. Otherwise, the program will not recognise them as the same activity**. It is case insensitive, meaning "Riflery", "RiflERy" and "riflery" will be accepted as the same.

## Getting the Optimal Activity Groups
**Ensure that the files described in the previous two sections match the format of the exmaple files**. The example files are `examples/example-activity-details.csv` and `examples/example-camper-selections.csv`.

1. Find your desired file and press the play icon in VS Code. Alternately, execute `python camper-sorting.py` in the command line.

### Using this Program for Tent Preferences
This program can be used for selecting tent preference for tent activity time. To do this:
1. Replace the camper name with a tent name. Do not have a tent column in the input file (see `example/example-tent-selections.csv`).
2. Enter the tent preferences. There is no limit to the number of preferences that can submitted - just continue to add more columns.

### What Does This Program Give Me?
This program outputs 4 files and some information in the console. The 4 `.csv` files can be opened with Excel or Google Sheets. The 4 files contain:
- An alphabetical list of campers and their allocation for each block. See `example/example-groups-by-camper-name.csv`.
- A list of campers, grouped by tent, and their allocation. See `example/example-groups-by-tent.csv`. **Note: This is only available if tent information is provided in the input file. See `examples/example-camper-selections-with-tents.csv`**. 
- A list of activities grouped by activity block and the campers participating. See `example/example-groups-by-activity-block.csv`.
- A list of activities grouped by activity type and the campers participating. See `example/example-groups-by-activity.csv`.

### Note on Scoring
Campers reveive a score based on how well their allocation matches their submitted preferences. 
- They receive 0 points if they are allocated an activity they didn't choose.
- They receive 1 point for their least preferred activity. 
- They receive as many points as they submitted preferences if they receive their 1st choice.

#### Example
If a camper submits 5 preferences and receives their 1st choice, 2nd choice and an acitivty they didn't choose, they will receive 5 points. 3 points for getting their 1st choice, 2 points for for getting thier 2nd choice and 0 points for the remaining activity.