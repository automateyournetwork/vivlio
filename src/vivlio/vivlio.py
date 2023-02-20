import os
import json
import requests
import aiohttp
import asyncio
import aiofiles
import rich_click as click
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class Vivlio():
    def __init__(self,
                token):
        self.token = token

    def vivlio(self):
        self.make_directories()
        # self.device_list = asyncio.run(self.build_device_list())
        # asyncio.run(self.add_device_apis())
        asyncio.run(self.main())

    def make_directories(self):
        api_list = ['Organizations'
                    ]
        current_directory = os.getcwd()
        for api in api_list:
            final_directory = os.path.join(current_directory, rf'{ api }/JSON')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/YAML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/CSV')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/HTML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Markdown')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ api }/Mindmap')
            os.makedirs(final_directory, exist_ok=True)

    # async def build_device_list(self):
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(f"{self.vManage}/dataservice/device",cookies = self.cookie, verify_ssl=False) as resp:
    #             response_dict = await resp.json()
    #             print(f"Status Code {resp.status}")
    #             return (response_dict)    

    # async def add_device_apis(self):
    #     #ARP
    #     for device in self.device_list['data']:
    #         arp_api = f"/dataservice/device/arp?deviceId={ device['deviceId'] }"
    #         self.api_list.append(arp_api)
            
    api_list = ["organizations"
                ]

    async def get_api(self, api_url):
        payload={}
        headers = {
        'X-Cisco-Meraki-API-Key': f'{self.token}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.meraki.com/api/v1/{api_url}",headers = headers, data=payload, verify_ssl=False) as resp:
                response_dict = await resp.json()
                print(f"{api_url} Status Code {resp.status}")
                return (api_url,response_dict)

    async def main(self):
        results = await asyncio.gather(*(self.get_api(api_url) for api_url in self.api_list))
        await self.all_files(json.dumps(results, indent=4, sort_keys=True))

    async def json_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            if api == "organizations":
                async with aiofiles.open('Organizations/JSON/Organizations.json', mode='w') as f:
                    await f.write(json.dumps(payload, indent=4, sort_keys=True))

    async def yaml_file(self, parsed_json):
        for api, payload in json.loads(parsed_json):
            clean_yaml = yaml.dump(payload, default_flow_style=False)
            if api == "organizations":
                async with aiofiles.open('Organizations/YAML/Organizations.yaml', mode='w' ) as f:
                    await f.write(clean_yaml)

    async def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        for api, payload in json.loads(parsed_json):        
            csv_output = await csv_template.render_async(api = api,
                                         data_to_template = payload)
            if api == "organizations":
                async with aiofiles.open('Organizations/CSV/Organizations.csv', mode='w' ) as f:
                    await f.write(csv_output)

    async def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')
        for api, payload in json.loads(parsed_json):        
            markdown_output = await markdown_template.render_async(api = api,
                                         data_to_template = payload)
            if api == "organizations":
                async with aiofiles.open('Organizations/Markdown/Organizations.md', mode='w' ) as f:
                    await f.write(markdown_output)

    async def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        for api, payload in json.loads(parsed_json):
            html_output = await html_template.render_async(api = api,
                                             data_to_template = payload)
            if api == "":
                async with aiofiles.open('Organizations/HTML/Organizations.html', mode='w' ) as f:
                    await f.write(html_output)

    async def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        for api, payload in json.loads(parsed_json):
            mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = payload)
            if api == "organizations":
                async with aiofiles.open('Organizations/Mindmap/Organizations.md', mode='w' ) as f:
                    await f.write(mindmap_output)

    async def all_files(self, parsed_json):
        await asyncio.gather(self.json_file(parsed_json),
                             self.yaml_file(parsed_json),
                             self.csv_file(parsed_json),
                             self.markdown_file(parsed_json),
                             self.html_file(parsed_json),
                             self.mindmap_file(parsed_json)
                             )

@click.command()
@click.option('--token',
    prompt="Meraki API Token",
    help="Meraki API Token",
    required=True, hide_input=True,envvar="TOKEN")
def cli(token):
    invoke_class = Vivlio(token)
    invoke_class.vivlio()

if __name__ == "__main__":
    cli()
