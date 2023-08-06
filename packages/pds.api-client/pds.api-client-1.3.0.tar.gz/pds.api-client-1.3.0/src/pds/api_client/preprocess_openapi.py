import yaml
import argparse
import tempfile
import subprocess

def preprocess(input: dict):

    new_tags_dict = {t['name']: t['name'][3:] for t in input['tags']}
    for path in input['paths'].keys():
        tags = input['paths'][path]['get']['tags']
        new_tags = [new_tags_dict.get(tag, tag) for tag in tags]
        input['paths'][path]['get']['tags'] = new_tags

    # remove the * object which is confusing for the api generator
    for k, r in input['components']['responses'].items():
        del r['content']['*']

    return input


def main():

    parser = argparse.ArgumentParser(
                    prog='Process yaml openapi',
                    description='Remove features unsupported by openapi-generator, python-nextgen language',
    )
    parser.add_argument('input_yaml')
    parser.add_argument('-v', '--version', help="version of the package to be generated")

    args = parser.parse_args()

    with open(args.input_yaml, "r") as stream:
        try:
            input = yaml.safe_load(stream)
            preprocess(input)

        except yaml.YAMLError as exc:
            print(exc)

    with tempfile.NamedTemporaryFile(mode='w', delete=True) as file:
        yaml.dump(input, file)
        clean_cmd = ['rm', '-fr', 'pds', 'test']
        subprocess.run(clean_cmd)

        # to test with the latest version of the openapi-generator
        #openapi_generator_cmd = [
        #    'java',
        #    '-jar',
        #    '.../openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar'
        #    ]

        openapi_generator_cmd = ['openapi-generator']
        openapi_generator_cmd.extend([
            'generate',
            '-g',
            'python-nextgen',
            '-i',
            file.name,
            '--package-name',
            'pds.api_client',
            f'--additional-properties=packageVersion={args.version}'
        ])
        subprocess.run(openapi_generator_cmd)

        replace_gitignore_cmd = ['cp', '.gitignore-orig',  '.gitignore']
        subprocess.run(replace_gitignore_cmd)


if __name__ == '__main__':
    main()