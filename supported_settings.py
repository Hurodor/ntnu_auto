
# This only works when there is one area to choose from
valid_room_settings = [{
    "Gløshaugen": {
        "Elektro E/F": {
            'E204': 'input_341E204',
            'F204': 'input_341F204',
            'E304': 'input_341E304',
            'EL23': 'input_341EL23',
            'F404': 'input_341F404',
            'F304': 'input_341F304'
        }
    }
}
]

# default settings, should work
default_room_settings = {
    "start_time": "08:00",
    "duration": "04:00",
    "days": 14,
    "area": "Gløshaugen",
    "building": "Elektro E/F",
    "min_people": 0,
    "room_id": "E204",
    "description_text": "Studering"
}
