import os
import json
import openai
import rich_click as click
import meraki.aio
import asyncio
import aiofiles
import yaml
import urllib3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings()

openai.api_key = os.getenv("OPENAI_KEY")

class Vivlio():
    def vivlio(self):
        self.make_directories()
        self.api_count = 0
        asyncio.run(self.organizations())
        asyncio.run(self.networks())
        #asyncio.run(self.devices())
        asyncio.run(self.sub_apis())
        print(f"Vivlio has transformed { self.api_count } Meraki APIs into Business Ready Documents")

    def make_directories(self):
        folder_list = ['Devices',
                    'Devices Cellular Sims',
                    'Devices Clients',
                    'Devices LLDP CDP',
                    'Devices Management Interfaces',
                    'Networks',
                    'Networks Alert History',
                    'Networks Alert Settings',
                    'Networks Clients',
                    'Networks Events',
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

    async def sub_apis(self):
        await asyncio.gather(#self.network_clients(),
                            self.network_events(),
                            #self.device_clients(),
                            #self.management_interfaces(),
                            #self.alert_settings(),
                            #self.alert_history(),
                            #self.lldp_cdp(),
                            #self.device_cellular_sims()
                        )

    # async def get_device_cellular_sims(self,device_serial,device_name):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_device_celluar_sims = await aiomeraki.devices.getDeviceCellularSims(device_serial)
    #             self.api_count += 1
    #             my_device_celluar_sims['device_serial']=device_serial
    #             my_device_celluar_sims['name']=device_name
    #             return(my_device_celluar_sims)
    #         except:
    #             print("No Device Celluar Sims")

    # async def device_cellular_sims(self):
    #     api = "device_cellular_sims"
    #     results = await asyncio.gather(*(self.get_device_cellular_sims(device['serial'],device['name']) for hit in self.device_list if hit for device in hit))
    #     async with aiofiles.open("Devices Cellular Sims/JSON/Devices Cellular Sims.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Devices Cellular Sims/YAML/Devices Cellular Sims.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     # No Data to template with yet 
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # csv_template = env.get_template('vivlio_csv.j2')
    #     # csv_output = await csv_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices Cellular Sims/CSV/Devices Cellular Sims.csv", mode='w' ) as f:
    #     #     await f.write(csv_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # markdown_template = env.get_template('vivlio_markdown.j2')    
    #     # markdown_output = await markdown_template.render_async(api = api,
    #     #                             data_to_template = results)
    #     # async with aiofiles.open("Devices Cellular Sims/Markdown/Devices Cellular Sims.md", mode='w' ) as f:
    #     #     await f.write(markdown_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # html_template = env.get_template('vivlio_html.j2')
    #     # html_output = await html_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices Cellular Sims/HTML/Devices Cellular Sims.html", mode='w' ) as f:
    #     #     await f.write(html_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     # mindmap_output = await mindmap_template.render_async(api = api,
    #     #                                      data_to_template = results)
    #     # async with aiofiles.open("Devices Cellular Sims/Mindmap/Devices Cellular Sims.md", mode='w' ) as f:
    #     #     await f.write(mindmap_output)

    # async def get_device_clients(self,device_serial,device_name):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_device_clients = await aiomeraki.devices.getDeviceClients(device_serial)
    #             self.api_count += 1
    #             my_device_clients['device_serial']=device_serial
    #             my_device_clients['name']=device_name
    #             return(my_device_clients)
    #         except:
    #             print("No Device Clients")

    # async def device_clients(self):
    #     api = "device_clients"
    #     results = await asyncio.gather(*(self.get_device_clients(device['serial'],device['name']) for hit in self.device_list if hit for device in hit))
    #     async with aiofiles.open("Devices Clients/JSON/Devices Clients.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Devices Clients/YAML/Devices Clients.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     # No Data to template with yet 
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # csv_template = env.get_template('vivlio_csv.j2')
    #     # csv_output = await csv_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices Clients/CSV/Devices Clients.csv", mode='w' ) as f:
    #     #     await f.write(csv_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # markdown_template = env.get_template('vivlio_markdown.j2')    
    #     # markdown_output = await markdown_template.render_async(api = api,
    #     #                             data_to_template = results)
    #     # async with aiofiles.open("Devices Clients/Markdown/Devices Clients.md", mode='w' ) as f:
    #     #     await f.write(markdown_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # html_template = env.get_template('vivlio_html.j2')
    #     # html_output = await html_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices Clients/HTML/Devices Clients.html", mode='w' ) as f:
    #     #     await f.write(html_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     # mindmap_output = await mindmap_template.render_async(api = api,
    #     #                                      data_to_template = results)
    #     # async with aiofiles.open("Devices Clients/Mindmap/Devices Clients.md", mode='w' ) as f:
    #     #     await f.write(mindmap_output)
        
    # async def get_lldp_cdp(self,device_serial,device_name):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_lldp_cdp = await aiomeraki.devices.getDeviceLldpCdp(device_serial)
    #             self.api_count += 1
    #             my_lldp_cdp['device_serial']=device_serial
    #             my_lldp_cdp['name']=device_name
    #             return(my_lldp_cdp)
    #         except:
    #             print("No LLDP CDP")

    # async def lldp_cdp(self):
    #     api = "lldp_cdp"
    #     results = await asyncio.gather(*(self.get_lldp_cdp
    #                                      (device['serial'],device['name']) for hit in self.device_list if hit for device in hit))
    #     async with aiofiles.open("Devices LLDP CDP/JSON/Devices LLDP CDP.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Devices LLDP CDP/YAML/Devices LLDP CDP.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     # No Data to template with yet 
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # csv_template = env.get_template('vivlio_csv.j2')
    #     # csv_output = await csv_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices LLDP CDP/CSV/Devices LLDP CDP.csv", mode='w' ) as f:
    #     #     await f.write(csv_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # markdown_template = env.get_template('vivlio_markdown.j2')    
    #     # markdown_output = await markdown_template.render_async(api = api,
    #     #                             data_to_template = results)
    #     # async with aiofiles.open("Devices LLDP CDP/Markdown/Devices LLDP CDP.md", mode='w' ) as f:
    #     #     await f.write(markdown_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # html_template = env.get_template('vivlio_html.j2')
    #     # html_output = await html_template.render_async(api = api,
    #     #                                 data_to_template = results)
    #     # async with aiofiles.open("Devices LLDP CDP/HTML/Devices LLDP CDP.html", mode='w' ) as f:
    #     #     await f.write(html_output)
    #     # template_dir = Path(__file__).resolve().parent
    #     # env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     # mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     # mindmap_output = await mindmap_template.render_async(api = api,
    #     #                                      data_to_template = results)
    #     # async with aiofiles.open("Devices LLDP CDP/Mindmap/Devices LLDP CDP.md", mode='w' ) as f:
    #     #     await f.write(mindmap_output)

    # async def get_alert_history(self,network_id):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_alert_history = await aiomeraki.networks.getNetworkAlertsHistory(network_id)
    #             self.api_count += 1
    #             my_alert_history['network_id']=network_id
    #             return(my_alert_history)
    #         except:
    #             print("No Alert History")

    # async def alert_history(self):
    #     api = "alert_history"
    #     results = await asyncio.gather(*(self.get_alert_history(network['id']) for hit in self.network_list if hit for network in hit))
    #     async with aiofiles.open("Networks Alert History/JSON/Networks Alert History.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Networks Alert History/YAML/Networks Alert History.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     csv_template = env.get_template('vivlio_csv.j2')
    #     csv_output = await csv_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Alert History/CSV/Networks Alert History.csv", mode='w' ) as f:
    #         await f.write(csv_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     markdown_template = env.get_template('vivlio_markdown.j2')    
    #     markdown_output = await markdown_template.render_async(api = api,
    #                                 data_to_template = results)
    #     async with aiofiles.open("Networks Alert History/Markdown/Networks Alert History.md", mode='w' ) as f:
    #         await f.write(markdown_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     html_template = env.get_template('vivlio_html.j2')
    #     html_output = await html_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Alert History/HTML/Network Alerts History.html", mode='w' ) as f:
    #         await f.write(html_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     mindmap_output = await mindmap_template.render_async(api = api,
    #                                          data_to_template = results)
    #     async with aiofiles.open("Networks Alert History/Mindmap/Networks Alert History.md", mode='w' ) as f:
    #         await f.write(mindmap_output)

    # async def get_alert_settings(self,network_id):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_alert_settings = await aiomeraki.networks.getNetworkAlertsSettings(network_id)
    #             self.api_count += 1
    #             my_alert_settings['network_id']=network_id
    #             return(my_alert_settings)
    #         except:
    #             print("No Alert Settings")

    # async def alert_settings(self):
    #     api = "alert_settings"
    #     results = await asyncio.gather(*(self.get_alert_settings(network['id']) for hit in self.network_list if hit for network in hit))
    #     async with aiofiles.open("Networks Alert Settings/JSON/Networks Alert Settings.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Networks Alert Settings/YAML/Networks Alert Settings.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     csv_template = env.get_template('vivlio_csv.j2')
    #     csv_output = await csv_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Alert Settings/CSV/Networks Alert Settings.csv", mode='w' ) as f:
    #         await f.write(csv_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     markdown_template = env.get_template('vivlio_markdown.j2')    
    #     markdown_output = await markdown_template.render_async(api = api,
    #                                 data_to_template = results)
    #     async with aiofiles.open("Networks Alert Settings/Markdown/Networks Alert Settings.md", mode='w' ) as f:
    #         await f.write(markdown_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     html_template = env.get_template('vivlio_html.j2')
    #     html_output = await html_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Alert Settings/HTML/Network Alerts Settings.html", mode='w' ) as f:
    #         await f.write(html_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     mindmap_output = await mindmap_template.render_async(api = api,
    #                                          data_to_template = results)
    #     async with aiofiles.open("Networks Alert Settings/Mindmap/Networks Alert Settings.md", mode='w' ) as f:
    #         await f.write(mindmap_output)

    # async def get_management_interfaces(self,device_serial,device_name):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_management_interfaces = await aiomeraki.devices.getDeviceManagementInterface(device_serial)
    #             self.api_count += 1
    #             my_management_interfaces['device_serial']=device_serial
    #             my_management_interfaces['name']=device_name
    #             return(my_management_interfaces)
    #         except:
    #             print("No Management Interface")

    # async def management_interfaces(self):
    #     api = "management_interfaces"
    #     results = await asyncio.gather(*(self.get_management_interfaces(device['serial'],device['name']) for hit in self.device_list if hit for device in hit))
    #     async with aiofiles.open("Devices Management Interfaces/JSON/Devices Management Interfaces.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Devices Management Interfaces/YAML/Devices Management Interfaces.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     csv_template = env.get_template('vivlio_csv.j2')
    #     csv_output = await csv_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Devices Management Interfaces/CSV/Devices Management Interfaces.csv", mode='w' ) as f:
    #         await f.write(csv_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     markdown_template = env.get_template('vivlio_markdown.j2')    
    #     markdown_output = await markdown_template.render_async(api = api,
    #                                 data_to_template = results)
    #     async with aiofiles.open("Devices Management Interfaces/Markdown/Devices Management Interfaces.md", mode='w' ) as f:
    #         await f.write(markdown_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     html_template = env.get_template('vivlio_html.j2')
    #     html_output = await html_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Devices Management Interfaces/HTML/Devices Management Interfaces.html", mode='w' ) as f:
    #         await f.write(html_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     mindmap_output = await mindmap_template.render_async(api = api,
    #                                          data_to_template = results)
    #     async with aiofiles.open("Devices Management Interfaces/Mindmap/Devices Management Interfaces.md", mode='w' ) as f:
    #         await f.write(mindmap_output)

    # async def get_network_clients(self,network_id):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_clients = await aiomeraki.networks.getNetworkClients(network_id)
    #             self.api_count += 1
    #             return(my_clients)
    #         except:
    #             print("No Network Clients")

    # async def network_clients(self):
    #     api = "network_clients"
    #     results = await asyncio.gather(*(self.get_network_clients(network['id']) for hit in self.network_list if hit for network in hit))
    #     async with aiofiles.open("Networks Clients/JSON/Networks Clients.json", mode="w") as f:
    #         await f.write(json.dumps(results, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(results, default_flow_style=False)
    #     async with aiofiles.open("Networks Clients/YAML/Networks Clients.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     csv_template = env.get_template('vivlio_csv.j2')
    #     csv_output = await csv_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Clients/CSV/Networks Clients.csv", mode='w' ) as f:
    #         await f.write(csv_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     markdown_template = env.get_template('vivlio_markdown.j2')    
    #     markdown_output = await markdown_template.render_async(api = api,
    #                                 data_to_template = results)
    #     async with aiofiles.open("Networks Clients/Markdown/Networks Clients.md", mode='w' ) as f:
    #         await f.write(markdown_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     html_template = env.get_template('vivlio_html.j2')
    #     html_output = await html_template.render_async(api = api,
    #                                     data_to_template = results)
    #     async with aiofiles.open("Networks Clients/HTML/Networks Clients.html", mode='w' ) as f:
    #         await f.write(html_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     mindmap_output = await mindmap_template.render_async(api = api,
    #                                          data_to_template = results)
    #     async with aiofiles.open("Networks Clients/Mindmap/Networks Clients.md", mode='w' ) as f:
    #         await f.write(mindmap_output)

    # async def get_devices(self,org_id):
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         try:
    #             my_devices = await aiomeraki.organizations.getOrganizationDevices(org_id)
    #             self.api_count += 1
    #             return(my_devices)
    #         except:
    #             print("No Devices") 

    # async def devices(self):
    #     api = "devices"
    #     async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
    #         self.device_list = await asyncio.gather(*(self.get_devices(org['id']) for org in self.my_orgs))
    #     async with aiofiles.open("Devices/JSON/Devices.json", mode="w") as f:
    #         await f.write(json.dumps(self.device_list, indent=4, sort_keys=True))
    #     clean_yaml = yaml.dump(self.device_list, default_flow_style=False)
    #     async with aiofiles.open("Devices/YAML/Devices.yaml", mode='w' ) as f:
    #         await f.write(clean_yaml)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     csv_template = env.get_template('vivlio_csv.j2')
    #     csv_output = await csv_template.render_async(api = api,
    #                                     data_to_template = self.device_list)
    #     async with aiofiles.open("Devices/CSV/Devices.csv", mode='w' ) as f:
    #         await f.write(csv_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     markdown_template = env.get_template('vivlio_markdown.j2')    
    #     markdown_output = await markdown_template.render_async(api = api,
    #                                 data_to_template = self.device_list)
    #     async with aiofiles.open("Devices/Markdown/Devices.md", mode='w' ) as f:
    #         await f.write(markdown_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     html_template = env.get_template('vivlio_html.j2')
    #     html_output = await html_template.render_async(api = api,
    #                                     data_to_template = self.device_list)
    #     async with aiofiles.open("Devices/HTML/Devices.html", mode='w' ) as f:
    #         await f.write(html_output)
    #     template_dir = Path(__file__).resolve().parent
    #     env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
    #     mindmap_template = env.get_template('vivlio_mindmap.j2')
    #     mindmap_output = await mindmap_template.render_async(api = api,
    #                                          data_to_template = self.device_list)
    #     async with aiofiles.open("Devices/Mindmap/Devices.md", mode='w' ) as f:
    #         await f.write(mindmap_output)

    async def get_networks(self,org_id):
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            try:
                my_networks = await aiomeraki.organizations.getOrganizationNetworks(org_id)
                self.api_count += 1
                return(my_networks)
            except:
                print("No Networks")                

    async def networks(self):
        api = "networks"
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            self.network_list = await asyncio.gather(*(self.get_networks(org['id']) for org in self.my_orgs))
        async with aiofiles.open("Networks/JSON/Networks.json", mode="w") as f:
            await f.write(json.dumps(self.network_list, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(self.network_list, default_flow_style=False)
        async with aiofiles.open("Networks/YAML/Networks.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = self.network_list)
        async with aiofiles.open("Networks/CSV/Networks.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = self.network_list)
        async with aiofiles.open("Networks/Markdown/Networks.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = self.network_list)
        async with aiofiles.open("Networks/HTML/Networks.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = self.network_list)
        async with aiofiles.open("Networks/Mindmap/Networks.md", mode='w' ) as f:
            await f.write(mindmap_output)
        
    async def organizations(self):
        api = "organizations"
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            self.my_orgs = await aiomeraki.organizations.getOrganizations()
            self.api_count += 1       
        async with aiofiles.open("Organizations/JSON/Organizations.json", "w") as f:
            await f.write(json.dumps(self.my_orgs, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(self.my_orgs, default_flow_style=False)
        async with aiofiles.open("Organizations/YAML/Organizations.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = self.my_orgs)
        async with aiofiles.open("Organizations/CSV/Organizations.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = self.my_orgs)
        async with aiofiles.open("Organizations/Markdown/Organizations.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = self.my_orgs)
        async with aiofiles.open("Organizations/HTML/Organizations.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = self.my_orgs)
        async with aiofiles.open("Organizations/Mindmap/Organizations.md", mode='w' ) as f:
            await f.write(mindmap_output)

    async def get_network_events(self,network_id):
        async with meraki.aio.AsyncDashboardAPI() as aiomeraki:
            try:
                my_clients = await aiomeraki.networks.getNetworkEvents(network_id)
                self.api_count += 1
                return(my_clients)
            except:
                print("No Network Events")

    async def network_events(self):
        api = "network_clients"
        results = await asyncio.gather(*(self.get_network_events(network['id']) for hit in self.network_list if hit for network in hit))
        async with aiofiles.open("Networks Events/JSON/Networks Events.json", mode="w") as f:
            await f.write(json.dumps(results, indent=4, sort_keys=True))
        clean_yaml = yaml.dump(results, default_flow_style=False)
        async with aiofiles.open("Networks Events/YAML/Networks Events.yaml", mode='w' ) as f:
            await f.write(clean_yaml)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        csv_template = env.get_template('vivlio_csv.j2')
        csv_output = await csv_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open("Networks Events/CSV/Networks Events.csv", mode='w' ) as f:
            await f.write(csv_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        markdown_template = env.get_template('vivlio_markdown.j2')    
        markdown_output = await markdown_template.render_async(api = api,
                                    data_to_template = results)
        async with aiofiles.open("Networks Events/Markdown/Networks Events.md", mode='w' ) as f:
            await f.write(markdown_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        html_template = env.get_template('vivlio_html.j2')
        html_output = await html_template.render_async(api = api,
                                        data_to_template = results)
        async with aiofiles.open("Networks Events/HTML/Networks Events.html", mode='w' ) as f:
            await f.write(html_output)
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)), enable_async=True)
        mindmap_template = env.get_template('vivlio_mindmap.j2')
        mindmap_output = await mindmap_template.render_async(api = api,
                                             data_to_template = results)
        async with aiofiles.open("Networks Events/Mindmap/Networks Events.md", mode='w' ) as f:
            await f.write(mindmap_output)

        event_descriptions = []
        for hit in results:
            if hit:
                for event in hit['events']:
                    event_descriptions.append(event['description'])

                unique_events = set(event_descriptions)
                print(unique_events)
                for event in unique_events:
                    print(f"I'm asking chatGPT about the event { event }")
                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a network troubleshooting tool"},
                            {"role": "user", "content": f"Please describe the following network condition { event }"},
                        ]
                    )

                    result = ''
                    for choice in response.choices:
                        result += choice.message.content

                    print(f"We asked chatGPT Please describe the following network condition { event } - here was there response:")
                    print(result)

                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a chatbot"},
                            {"role": "user", "content": f"Please describe the following network condition { event } and explain it like I'm 5"},
                        ]
                    )

                    result = ''
                    for choice in response.choices:
                        result += choice.message.content

                    print(f"We asked chatGPT Please describe the following network condition { event } and explain it like I'm 5 - here was there response:")
                    print(result)

                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a network troubleshooting tool"},
                            {"role": "user", "content": f"Is the network event { event } a problem with the network?"},
                        ]
                    )

                    result = ''
                    for choice in response.choices:
                        result += choice.message.content

                    print(f"We asked chatGPT Is the network event { event } a problem with the network? - here was there response:")
                    print(result)

                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a network troubleshooting tool"},
                            {"role": "user", "content": f"How do I troubleshoot a { event } problem with Meraki?"},
                        ]
                    )

                    result = ''
                    for choice in response.choices:
                        result += choice.message.content

                    print(f"We asked chatGPTHow do I troubleshoot a { event } problem with Meraki? - here was there response:")
                    print(result)
                    
@click.command()
def cli():
    invoke_class = Vivlio()
    invoke_class.vivlio()

if __name__ == "__main__":
    cli()
