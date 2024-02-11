# palworld-server-save-transfer
Script for transfering Palworld saves between servers.

Can be used to transfert from host game to dedicated server, or between two dedicated servers (Windows->Linux, etc).

As far as I tested it, this script also transfers guild informations.

Only uses python.

### Credit
I made this script to automate the long and tedious process described at [https://gist.github.com/mojobojo/c9e1e3d05d074408ed4bd6fbe04e62ef].

I also used (and slightly modified) palworld-save-tools [https://github.com/cheahjs/palworld-save-tools].

The following links also provided usefull informations [https://www.reddit.com/r/Palworld/comments/19cb8su], [https://github.com/xNul/palworld-host-save-fix]


## How to use

### 0 - Download the script 

1. Download the latest release from [https://github.com/Matheo-Moinet/palworld-server-save-transfer/releases/latest].
1. Unzip the file into a folder.

### 1 - Copy the world save

1. Copy the folder of the world save you wish to transfer in the folder named: `1_YOUR_WORLD_SAVE`
   - For example, the folder with the name `4779E0844F461BA5218C5592A7D5007C`. If you do not know where your save folder is located, please visit the reddit link provided above for more info.

### 2 - Gather the new player files

On palworld servers, each player is identified by the server using a `player_id`. When migrating servers, the `player_id` associated with each player can change. When it happens, if you try to connect to this world on your new server, you will be prompted to create a new character. This is because the server thinks you are a different player (even if your old player information is still there).

To explain it simply, this script corrects this by replacing your old `player_id` with your new `player_id` everywhere in the sav files. After this, the new server will still see you as having the new `player_id`, but now this `player_id` will be the one associated with your old data. This has to be done for every player whose `player_id` changed during the transfer. (Don't worry, its automated by the script)


You first have to find out in which of the 3 following situations you are:

1. (Host -> Dedicated with **same OS**) Only the host's `player_id` has changed, and every other player can connect like nothing happened (no new character creation screen for them).
2. (Host/Dedicated -> Host/Dedicated with a **different OS**) Every player's `player_id` has changed, everyone is asked to create a new character upon login. This often happens when migrating from a host game to a paid dedicated server service, as most of them are running Linux and not Windows.
3. (Dedicated -> Dedicated with the **same OS**) Every `player_id` should be the same so everyone should be able to connect without using this script. If not, you can still try to follow this guide.


Now for the script to work, we need the new `player_id` of every player whose's `player_id` has changed. This is done simply by having each of these player connect onto the new server. In case N°1, only the host is required. In case N°2, every player need to connect onto the new server.

Here are the steps to do so:

1. Shutdown the new server.
2. Copy the same world save folder (as in step 1) into your new server world directory.
   - The path should be looking like this `PalServer\Pal\Saved\SaveGames\0\`
   - Make sure you also modify the `GameUserSettings.ini` file accordingly in `PalServer\Pal\Saved\Config\WindowsServer`. Refer to the reddit link for more information.
3. Start the new server.
4. Have every player you care about connect to the server. (In case N°1, only you. In case N°2, every player)
   - If they have a different `player_id`, they will be asked to create a new character. This is normal. Please proceed to create this new character so that an associated .sav file is created.
   - This script has an option to automatically find which player is associated with which old and new `player_id`. However, this functionnality relies on the assumption that the old and new player names will be the same. If you wish to use this, please ask your players that the new character they create have **exactly** the same character name as the old one.
5. Shutdown the new server.
6. Copy back the world save folder with the new player saves from the new server to the `2_YOUR_SAVE_AFTER_JOIN` folder in the script folder.


### 3 - Run the scripts

1. Go into the `_Script_code` folder and open up a terminal.
   - If you do not know how to do this, please refer to the reddit link.
1. If you wish to automatically extract the old and new `player_id` for each player who connected to your server,
   - run the following command : 
        ```
        python ./extract_players_ids <YOUR_WORLD_SAVE_NAME>
        ```
        where you replace `<YOUR_WORLD_SAVE_NAME>` by the name of the folder of your save. Eg: 
        ```
        python ./extract_players_ids 4779E0844F461BA5218C5592A7D5007C
        ```
   - The file `CONFIG.txt` should should now be pre-filed with the correct player ids.
1. Otherwise, you can fill in the `CONFIG.txt` manually.
2. Still into `_Script_code`,
   - run the following command: 
        ```
        python ./transfer_save
        ```

Et voila ! Your transfered save awaits you in `3_TRANSFERED_SAVE`.

### 4 - Copy the transfered save to your server
  
1. Shut down the new server.
2. Delete the world save already located in your new server.
3. Copy the transfered world save from `3_TRANSFERED_SAVE` to your new server (again, at `PalServer\Pal\Saved\SaveGames\0\`).
4. Start the new server.


If everything went well, every player should now be able to login and have everything exactly the same as on the old server.


