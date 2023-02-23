import os
import json
import rich_click as click
import meraki.aio
import asyncio
import aiofiles
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

urllib3.disable_warnings()

class Vivlio():
    def vivlio(self):
        self.make_directories()
        self.api_count = 0
        # asyncio.run(self.organizations())
        # asyncio.run(self.networks())
        # asyncio.run(self.devices())
        asyncio.run(self.clients())
        print(f"Vivlio has transformed { self.api_count } Meraki APIs into Business Ready Documents")

    def make_directories(self):
        folder_list = ['Clients',
                    'Devices',
                    'Networks',
                    'Organizations'
                    ]
        
        current_directory = os.getcwd()
        for folder in folder_list:
            final_directory = os.path.join(current_directory, rf'{ folder }/JSON')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ folder }/YAML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ folder }/CSV')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ folder }/HTML')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ folder }/Markdown')
            os.makedirs(final_directory, exist_ok=True)
            final_directory = os.path.join(current_directory, rf'{ folder }/Mindmap')
            os.makedirs(final_directory, exist_ok=True)

    async def get_clients(self,network_id):
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            try:
                print(network_id)
                my_clients = await aiomeraki.networks.getNetworkClients(network_id)
                self.api_count += 1
                return(my_clients)
            except:
                print("API Not Enabled")

    async def clients(self):
        api = "clients"
        network_list = await self.networks()
        results = await asyncio.gather(*(self.get_clients(network['id']) for hit in network_list if hit for network in hit))
        async with aiofiles.open(f"Clients/JSON/Clients.json", mode="w") as f:
            await f.write(json.dumps(results, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(results, default_flow_style=False)
        async with aiofiles.open(f"Clients/YAML/Clients.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Clients/CSV/Clients.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = results)
        async with aiofiles.open(f"Clients/Markdown/Clients.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Clients/HTML/Clients.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = results)
        async with aiofiles.open(f"Clients/Mindmap/Clients.md", mode='w' ) as f:
            await f.write(mindmap_output)

    async def get_devices(self,org_id):
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            try:
                my_devices = await aiomeraki.organizations.getOrganizationDevices(org_id)
                self.api_count += 1
                return(my_devices)
            except:
                print("API Not Enabled") 

    async def devices(self):
        api = "devices"
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            my_orgs = await aiomeraki.organizations.getOrganizations()
            results = await asyncio.gather(*(self.get_devices(org['id']) for org in my_orgs))
        async with aiofiles.open(f"Devices/JSON/Devices.json", mode="w") as f:
            await f.write(json.dumps(results, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(results, default_flow_style=False)
        async with aiofiles.open(f"Devices/YAML/Devices.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Devices/CSV/Devices.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = results)
        async with aiofiles.open(f"Devices/Markdown/Devices.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Devices/HTML/Devices.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = results)
        async with aiofiles.open(f"Devices/Mindmap/Devices.md", mode='w' ) as f:
            await f.write(mindmap_output)

    async def get_networks(self,org_id):
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            try:
                my_networks = await aiomeraki.organizations.getOrganizationNetworks(org_id)
                self.api_count += 1
                return(my_networks)
            except:
                print("API Not Enabled")                

    async def networks(self):
        api = "networks"
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            my_orgs = await aiomeraki.organizations.getOrganizations()
            results = await asyncio.gather(*(self.get_networks(org['id']) for org in my_orgs))
        async with aiofiles.open(f"Networks/JSON/Networks.json", mode="w") as f:
            await f.write(json.dumps(results, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(results, default_flow_style=False)
        async with aiofiles.open(f"Networks/YAML/Networks.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Networks/CSV/Networks.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = results)
        async with aiofiles.open(f"Networks/Markdown/Networks.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open(f"Networks/HTML/Networks.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = results)
        async with aiofiles.open(f"Networks/Mindmap/Networks.md", mode='w' ) as f:
            await f.write(mindmap_output)
        return(results)
        
    async def organizations(self):
        api = "organizations"
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            my_orgs = await aiomeraki.organizations.getOrganizations()
            self.api_count += 1
        
        async with aiofiles.open("Organizations/JSON/Organizations.json", "w") as f:
            await f.write(json.dumps(my_orgs, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(my_orgs, default_flow_style=False)
        async with aiofiles.open("Organizations/YAML/Organizations.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = my_orgs)
        async with aiofiles.open("Organizations/CSV/Organizations.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = my_orgs)
        async with aiofiles.open("Organizations/Markdown/Organizations.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = my_orgs)
        async with aiofiles.open("Organizations/HTML/Organizations.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = my_orgs)
        async with aiofiles.open("Organizations/Mindmap/Organizations.md", mode='w' ) as f:
            await f.write(mindmap_output)
          
@click.command()
def cli():
    invoke_class = Vivlio()
    invoke_class.vivlio()

if __name__ == "__main__":
    cli()
