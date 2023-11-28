# bg3genitalmodcreator

### A small python script for Baldur's Gate 3 that takes in gr2 genital models and spits out mod files to put them in game.

To Use run `python .\insertWangs.py ModName ModAuthor` to generate the files and folders.

#### Naming Conventions

In order for the script to detect and insert your model into the game correctly you need a specific naming convention.

The in game name will be the beginning text of your file name using _(underscore) as a seperator.
- My_Custom_Junk

There are 3 variations in the game for genitals.

- Genital_A (Vulva)
- Genital_B (Uncircumcised Penis)
- Genital_C (Circumcised Penis)

By default your genital choice will come with pubic hair. If your model does not support pubic hair you need to add

- _NoHair

### Example
Your filename `My_Custom_Junk_Genital_B_NoHair.GR2` will use the settings for an uncircumcised penis without pubic hair.
The in game name will display as "My Custom Junk".


### Where to put your GR2 files

`MyModName/Generated/Public/MyModName/Race/BodyType`

For "Elves", "HalfElves", and "Drow" use the "Humans" folder as they share the same base body. The script will create entries in the game for all compatible races. 

For everyone else a folder should have been created for the race and sub-folders for the body type.

Copy your GR2 model files in the appropriate folder for example a large female tiefling will go in the `Tieflings/_FemaleStrong` folder.

### Lets create the mod

Run `python .\insertWangs.py ModName ModAuthor -g`. You will be asked if you want to overwrite the files. If you have only added your GR2 models this is perfectly safe.

Any edits you make to the lsx files will be overwritten though. So make backups if you have made any edits to the generated files.
