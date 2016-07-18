from webcv import app, CONFIG_FILE, DEFALUT_CONFIG_FILE


def main():
    args = {
        'debug': True,
        # watch config file for change.
        'extra_files': [ CONFIG_FILE, DEFALUT_CONFIG_FILE ],
    }
    app.run(**args)


if __name__ == '__main__':
    main()
