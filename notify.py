from win10toast import ToastNotifier
import argparse

toaster = ToastNotifier()

parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='URL to notify')

if __name__=='__main__':
    args = parser.parse_args()

    toaster.show_toast(
        title = 'Youtube Downloader',
        msg = f'Finished download from {args.url}',
        icon_path = 'Guillendesign-Variations-2-Script-Console.ico',
        duration = 5,
        threaded=True
    )