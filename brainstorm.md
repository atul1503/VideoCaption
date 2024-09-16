is using postgresql 15 and redis and ffmpeg

when doing in docker remember to created media folder in BASE_DIR( which has manage.py )



videoplayer component needs to know: src of file, dispatch current time to store.
caption component needs to know : timestamp, playerref to change timestamp of video.

who will provide:
        src of file: can be changed by anybody.
        timestamp: videoplayer will dispatch change to store.
        playerref: videoplayer will dispatch to store.
