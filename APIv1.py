from collections import defaultdict
from enum import Enum

class APIFieldConstants(Enum):
    current_comments = "currentComments"
    track_id = "trackId"
    track_duration = "trackDuration"
    daily_aggregate_plays = "dailyAggregatePlays"
    current_reposts = "currentReposts"
    track_url = "trackUrl"
    current_likes = "currentLikes"
    commentable = "commentable"
    track_title = "trackTitle"
    track_user_id = "trackUserId"
    track_genre = "trackGenre"
    time_stamp = "timeStamp"
    track_user_name = "trackUsername"
    current_downloads = "currentDownloads"
    _id = "_id"
    current_plays = "currentPlays"
    track_created_at = "trackCreatedAt"
    track_tag_list = "trackTagList"


class APIFilterConstants(Enum):
    current_comments = "currentComments"
    current_reposts = "currentReposts"
    current_likes = "currentLikes"
    track_title = "trackTitle"
    track_user_id = "trackUserId"
    track_genre = "trackGenre"
    time_stamp = "timeStamp"
    track_user_name = "trackUsername"
    current_downloads = "currentDownloads"
    current_plays = "currentPlays"
    track_created_at = "trackCreatedAt"
    track_tag_list = "trackTagList"


class APIv1:
    def is_valid_field(self, argval):
        return str(argval) in APIFieldConstants.__members__

    def to_field_params(self, arglist):
        d = defaultdict()
        d["_id"] = 0
        if type(arglist) == list:
            for x in arglist:
                if(self.is_valid_field(x)):
                    d[APIFieldConstants[str(x)].value] = 1
                else:
                    raise ValueError(
                        "The following field is not recognized by the API",
                        str(x),
                        )
        else:
            raise ValueError("The method requires a list to be passed to it.")
        return d

    def to_sort_params(self, args):
        d = list()
        if type(args) == str:
            d.append((APIFieldConstants[str(args)].value, -1))
        elif type(args) == list:
            for x in args:
                if(self.is_valid_field(x)):
                    d.append((APIFieldConstants[str(x)].value, -1))
                else:
                    raise ValueError(
                        "The following field is not recognized by the API",
                        str(x),
                        )
        else:
            raise ValueError("The method requires a list to be passed to it.")
        return d
