from qtl_xtp_api import consts


def main():
    print(f'Consts: {consts}')
    for key, value in consts.__dict__.items():
        if not key.startswith('__'):
            print(f'{key} = {value}')


if __name__ == '__main__':
    main()
