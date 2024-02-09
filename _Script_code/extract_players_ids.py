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

	parser = argparse.ArgumentParser(
		prog="palworld-save-tools",
		description="Converts Palworld save files to and from JSON",
	)
	parser.add_argument(
		"world_folder_name",
		help="Please specify the name of your world (copy the name of the folder)",
		)
	args = parser.parse_args()


	world_name = args.world_folder_name

	configFileName = "CONFIG.txt"
	configPath = "../"+configFileName


	cleanInputPath = "../"+cleanInputFolderName+"/"+world_name+"/"
	joinInputPath = "../"+afterJoinInputFolderName+"/"+world_name+"/"
	outputPath_Level = "../"+outputFolderName+"/"+world_name+"/Level.sav"
	outputPath_Player_Folder = "../"+outputFolderName+"/"+world_name+"/Players/"

	"""
	convert.convert_sav_to_json(joinInputPath+"Level.sav","../res/Level.json" , True)
	with open("../res/Level.json", 'r') as LevelJsonFile:
		level_join_json_string = LevelJsonFile.read()
	"""

	level_join_json = convert.read_and_convert_sav_to_json(joinInputPath+"Level.sav")
	level_join_json_string = json.dumps(level_join_json,  indent='\t', cls=CustomEncoder, allow_nan=True)


	found_players = {}


	# In the Level.sav file, all the guilds are listed, with each player belonging to each guild listed (players with no guild are in a default guild anyway).
	# There, the name of each player along its player_uid and last connection time are listed together
	# By finding two player_uid with the same name, we can assume the one who connected last is the new player_uid and the other the old player_id

	current_str_index = 0
	current_str_index = level_join_json_string.find("\"players\":", current_str_index)
	while (current_str_index != -1) :

		players_str_index = current_str_index + 11
		current_str_index = level_join_json_string.find("]", current_str_index)
		players_end_str_index = current_str_index

		players_str = level_join_json_string[players_str_index: players_end_str_index+1]
		players_json = json.loads(players_str)

		for player_json in players_json:
			# print(player_json)
			player_uid = player_json["player_uid"]
			last_online_real_time = player_json["player_info"]["last_online_real_time"]
			player_name = player_json["player_info"]["player_name"]

			if (found_players.get(player_name) == None):
				found_players[player_name] = {'old':{'player_uid':player_uid, 'last_online_real_time':last_online_real_time}, 'new':{'player_uid':"NotFound", 'last_online_real_time':"NotFound"}}
			else:
				found_players[player_name]['new'] = {'player_uid':player_uid, 'last_online_real_time':last_online_real_time}

				if ( found_players[player_name]['old']['last_online_real_time'] > last_online_real_time):
					temp = found_players[player_name]['old']
					found_players[player_name]['old'] = found_players['player_name']['new']
					found_players[player_name]['new'] = temp


		current_str_index = level_join_json_string.find("\"players\":", current_str_index)

	print("Automaticaly extracted players :")
	for player_name in found_players.keys():
		print(player_name +": "+ str(found_players[player_name]))

	players_csv_data=[]
	players_csv_data.append(['Your world name goes next line:'])
	players_csv_data.append([world_name])
	players_csv_data.append(['Your players info',' with 1 player per line formated as follows: old_player_uid',' new_player_uid',' <optional> player name'])

	for player_name in found_players.keys():
		player_old_uid = found_players[player_name]['old']['player_uid']
		player_old_uid = player_old_uid.replace("-","").upper()
		player_new_uid = found_players[player_name]['new']['player_uid']
		player_new_uid = player_new_uid.replace("-","").upper()
		player_data = [player_old_uid, player_new_uid, player_name]
		players_csv_data.append(player_data)
	print("")
	print("Writing to config file :")

	print(players_csv_data)

	# Write CSV file
	with open(configPath, "wt") as fp:
		writer = csv.writer(fp, delimiter=",", lineterminator="\n")
		# writer.writerow(["your", "header", "foo"])  # write header
		writer.writerows(players_csv_data)



#players_str = "{"+players_str+"}"
#players_str = players_str.replace("\t", "")
#players_str = players_str.replace("\n", "")
#players_str = players_str.replace(" ", "")

#print(players_str)
#players_json = json.loads(players_str,  indent='\t', cls=CustomEncoder, allow_nan=True)
#players_json = json.dumps(players_str, cls=CustomEncoder, allow_nan=True)

#print(level_join_json_string[players_str_index: players_end_str_index])

#print(players_str_index)
#print(players_end_str_index)






# print(oldPlayerJsonFile_data)


#oldPlayerJsonFile_data = oldPlayerJsonFile_data.replace(oldPlayer_play_id, newPlayer_play_id)
#oldPlayerJsonFile_data = oldPlayerJsonFile_data.replace(oldPlayer_inst_id, newPlayer_inst_id)



if __name__ == "__main__":
    main()