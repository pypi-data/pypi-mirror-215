from csup_analyzer.replay.FileHandler import FileHandler
from csup_analyzer.event.Event import Race, Quali, Event
from csup_analyzer.event.LineUp import LineUp

fh = FileHandler(
    [
        "example_replay_files/from_patch_1_5_0/20230621T19-18-00Z.header",
        "example_replay_files/from_patch_1_5_0/20230621T19-22-24Z.header",
    ]
)

quali = Quali(fh.get_quali_file_content())
race = Race(fh.get_race_file_content())
lineup = LineUp(fh.get_race_file_content())

event = Event(lineup=lineup, race=race, quali=quali)
event.create_result_dataframe()
event.run_result_calculations()

print(event.result_df)
print(event.result_df.lap_position_table)
