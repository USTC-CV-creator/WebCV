from webcv import app, CONFIG_FILE, DEFALUT_CONFIG_FILE
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bind', '-b',
        default='127.0.0.1:5000', help='address listening on'
    )
    cmd_args = parser.parse_args()
    ip, port = cmd_args.bind.split(':')
    if not ip:
        ip = '127.0.0.1'
    port = int(port)

    args = {
        'host': ip,
        'port': port,
        'debug': True,
        # watch config file for change.
        'extra_files': [ CONFIG_FILE, DEFALUT_CONFIG_FILE ],
    }
    app.run(**args)


if __name__ == '__main__':
    main()
