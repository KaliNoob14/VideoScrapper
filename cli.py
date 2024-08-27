import argparse
import importlib
import os
from utils.logger import log
from utils.assets import save_json_file


def list_modules():
    # List available modules dynamically except BaseModule
    module_dir = 'modules'
    return [f.replace('.py', '') for f in os.listdir(module_dir) if
            f.endswith('.py') and f != '__init__.py' and f != 'BaseModule.py']


def get_module_class(module_name):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        return getattr(module, module_name)
    except (ImportError, AttributeError) as e:
        log(f'Error importing module {module_name}: {e}', 'red')
        return None


def main():
    parser = argparse.ArgumentParser(description='VideoScrapper CLI', epilog='Examples:\n'
                                                                             '  python cli.py search --module Animewatchto --keyword "example" --limit_page 5\n'
                                                                             '  python cli.py crawl --module Animewatchto\n'
                                                                             '  python cli.py download --module Animewatchto --video_url "http://example.com/video.mp4" --save_path "videos/video.mp4"')

    parser.add_argument('command', choices=['search', 'crawl', 'download'], help='Command to execute')
    parser.add_argument('--module', help='Module to use', choices=list_modules(), required=True)
    parser.add_argument('--keyword', help='Search keyword')
    parser.add_argument('--absolute', help='Absolute URL for search')
    parser.add_argument('--limit_page', type=int, help='Limit the number of pages for search')
    parser.add_argument('--video_url', help='URL of the video to download')
    parser.add_argument('--save_path', help='Path to save the downloaded video')

    args = parser.parse_args()

    if args.command == 'search':
        if not args.keyword:
            log('Keyword is required for search', 'red')
            return
        module_class = get_module_class(args.module)
        if not module_class:
            return
        module = module_class()  # Instantiate without 'domain' argument
        # Implement search functionality
        results = module.search_by_keyword(args.keyword, args.absolute)
        save_json_file(f'{args.keyword}_search_results.json', results)
        log(f'Search results saved to {args.keyword}_search_results.json', 'green')

    elif args.command == 'crawl':
        module_class = get_module_class(args.module)
        if not module_class:
            return
        module = module_class()  # Instantiate without 'domain' argument
        # Implement crawl functionality
        db = module.get_db()
        save_json_file(f'{args.module}_database.json', db)
        log(f'Database saved to {args.module}_database.json', 'green')

    elif args.command == 'download':
        if not args.video_url or not args.save_path:
            log('Video URL and save path are required for download', 'red')
            return
        module_class = get_module_class(args.module)
        if not module_class:
            return
        module = module_class()  # Instantiate without 'domain' argument
        # Implement download functionality
        saved_path = module.download_video(args.video_url, args.save_path)
        log(f'Video downloaded to {saved_path}', 'green')


if __name__ == '__main__':
    main()
