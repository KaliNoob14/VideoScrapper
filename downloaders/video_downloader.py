import os
from utils import assets, exceptions, logger
from requests.exceptions import HTTPError, Timeout

def download_single(video, url, module, last, ranged, videos):
    videos_to_download = get_videos_to_download(video, url, module, last, ranged, videos)
    inconsistencies = download_videos(video, module, videos_to_download)
    if inconsistencies:
        logger.log(f'There were some inconsistencies with the following videos: {", ".join(inconsistencies)}', 'red')

def get_videos_to_download(video, url, module, last, ranged, c_videos):
    videos_to_download = []
    logger.log_over(f'\r{video}: Getting videos...')
    videos = module.get_videos(url)
    if last:
        reached_last_downloaded_video = False
        for v in videos:
            if last in v['name']:
                reached_last_downloaded_video = True
                continue
            if reached_last_downloaded_video:
                videos_to_download.append(v)
    elif ranged:
        reached_beginning_video = False
        for v in videos:
            if ranged[0] in v['name']:
                reached_beginning_video = True
            if reached_beginning_video:
                videos_to_download.append(v)
            if ranged[1] in v['name']:
                break
    elif c_videos:
        for c in c_videos:
            for v in videos:
                if c in v['name']:
                    videos_to_download.append(v)
                    break
    else:
        videos_to_download = videos
    logger.log(f'\r{video}: {len(videos_to_download)} video{"" if len(videos_to_download) == 1 else "s"} to download.')
    return videos_to_download

def download_videos(video, module, videos):
    inconsistencies = []
    fixed_video = assets.fix_name_for_folder(video)
    assets.create_folder(fixed_video)
    while videos:
        try:
            video_name = videos[0]['name']
            logger.log_over(f'\r{video}: {video_name}: Downloading video...')
            video_url = videos[0]['url']
            save_path = f'{fixed_video}/{assets.fix_name_for_folder(video_name)}.mp4'
            if not os.path.exists(save_path):
                assets.sleep()
                saved_path = module.download_video(video_url, save_path)
                if not saved_path:
                    logger.log(f' Warning: Video {video_name} could not be downloaded. URL: {video_url}', 'red')
            else:
                logger.log(f'\r{video}: {video_name}: Video already exists, skipping.', 'yellow')
            del videos[0]
        except (Timeout, HTTPError, exceptions.DownloadException) as error:
            logger.log(error, 'red')
    return inconsistencies
