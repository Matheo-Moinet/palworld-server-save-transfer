import argparse
import json
import os
import csv


from lib.json_tools import CustomEncoder
import convert


def main():

    cleanInputFolderName = "1_YOUR_WORLD_SAVE"
    afterJoinInputFolderName = "2_YOUR_SAVE_AFTER_JOIN"
    outputFolderName = "3_FIXED_SAVE"

    configFileName = "CONFIG.txt"
    configPath = "../"+configFileName



    # Read CSV Config file
    with open("../"+configFileName, "r") as fp:
        csv_reader = csv.reader(fp, delimiter=",")
        # writer.writerow(["your", "header", "foo"])  # write header
        data_read = [row for row in csv_reader]
        world_name = data_read[1][0]
        player_ids = data_read[3:]
        player_infos = player_ids
        len(player_ids)
        print(world_name)
        print(player_ids)


    cleanInputPath = "../"+cleanInputFolderName+"/"+world_name+"/"
    joinInputPath = "../"+afterJoinInputFolderName+"/"+world_name+"/"
    joinInputPath_Player_Folder = "../"+afterJoinInputFolderName+"/"+world_name+"/Players/"
    outputPath_Level = "../"+outputFolderName+"/"+world_name+"/Level.sav"
    outputPath_Player_Folder = "../"+outputFolderName+"/"+world_name+"/Players/"

    # Copy clean dir into output dir
    import shutil
    shutil.copytree("../"+cleanInputFolderName+"/"+world_name, "../"+outputFolderName+"/"+world_name, dirs_exist_ok=True)


    print("Converting player save files ...")
    # Read each player old and new sav file to gather player_uid and instance_id
    # Write new player sav file combining old player sav data and new player ids
    for i in range(len(player_ids)):
        oldPlayerSav = player_ids[i][0]
        newPlayerSav = player_ids[i][1]

        j_old = convert.read_and_convert_sav_to_json(joinInputPath_Player_Folder+oldPlayerSav+".sav")
        j_new = convert.read_and_convert_sav_to_json(joinInputPath_Player_Folder+newPlayerSav+".sav")
            
        oldPlayer_play_id = j_old["properties"]["SaveData"]["value"]["PlayerUId"]["value"]
        oldPlayer_play_id2 = j_old["properties"]["SaveData"]["value"]["IndividualId"]["value"]["PlayerUId"]["value"] # should be same ?
        oldPlayer_inst_id = j_old["properties"]["SaveData"]["value"]["IndividualId"]["value"]["InstanceId"]["value"]

        newPlayer_play_id = j_new["properties"]["SaveData"]["value"]["PlayerUId"]["value"]
        newPlayer_play_id2 = j_new["properties"]["SaveData"]["value"]["IndividualId"]["value"]["PlayerUId"]["value"] # should be same ?
        newPlayer_inst_id = j_new["properties"]["SaveData"]["value"]["IndividualId"]["value"]["InstanceId"]["value"]

        player_infos[i] = {'oldPlayer_play_id':oldPlayer_play_id, 'oldPlayer_inst_id':oldPlayer_inst_id, 'newPlayer_play_id': newPlayer_play_id, 'newPlayer_inst_id':newPlayer_inst_id}

        print(player_infos)


        # Replace the target string
        oldPlayerJsonFile_data = json.dumps(j_old,  indent='\t', cls=CustomEncoder, allow_nan=True)
        # print(oldPlayerJsonFile_data)
        oldPlayerJsonFile_data = oldPlayerJsonFile_data.replace(oldPlayer_play_id, newPlayer_play_id)
        oldPlayerJsonFile_data = oldPlayerJsonFile_data.replace(oldPlayer_inst_id, newPlayer_inst_id)

        convert.write_and_convert_jsons_to_sav(oldPlayerJsonFile_data, outputPath_Player_Folder+newPlayerSav+".sav", True)

        print("Done converting player save file from "+oldPlayerSav+" to "+newPlayerSav)
        
    print("Done converting player save files")

    print("Now reading and correcting Level.sav ...")

    clean_level_json = convert.read_and_convert_sav_to_json(cleanInputPath+"Level.sav")
    clean_level_json_string = json.dumps(clean_level_json,  indent='\t', cls=CustomEncoder, allow_nan=True)

    for i in range(len(player_ids)):
        # Replace the target string
        clean_level_json_string = clean_level_json_string.replace(player_infos[i]['oldPlayer_play_id'], player_infos[i]['newPlayer_play_id'])
        clean_level_json_string = clean_level_json_string.replace(player_infos[i]['oldPlayer_inst_id'], player_infos[i]['newPlayer_inst_id'])

    print("Done reading and correcting Level.sav")
    print("Now writting Level.sav ...")

    convert.write_and_convert_jsons_to_sav(clean_level_json_string, outputPath_Level, True)

    print("Done writting Level.sav")

    print("Script finished ! You can find the fixed world save in "+"./"+outputFolderName+"/")



if __name__ == "__main__":
    main()