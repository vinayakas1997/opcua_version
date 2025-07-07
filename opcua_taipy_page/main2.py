from taipy.gui import Gui
import taipy.gui.builder as tgb
import datetime
import random
from threading import Timer
ip_address = " "
model = "FINS-XYZ123"
status = "Connected"
clockset = "2025-07-01 10:30"

os_version = "v2.3.5"
boot_version = "v1.1.9"


data_type = " "
data_type_list = ["INT16", "UINT16","INT32", "UINT32", "INT64", "UINT64", "FLOAT", "DOUBLE"]

register_address = " "
data_type = "INT"  # or BOOL, FLOAT
trigger_type = "Continuous"
trigger_interval = 1  # in seconds
register_address_details = {}
table_data = []
cols = ["timestamp"]
register_address_details ={}
def add_to_table(state):
    if state.register_address not in state.register_address_details:
        state.register_address_details[state.register_address] = {
            "data_type": state.data_type,
            "trigger_type": state.trigger_type,
            "trigger_interval": state.trigger_interval
        }
        state.cols.append(state.register_address)
        # notify()
def update_table(state):
    row = {"timestamp": datetime.datetime.now().strftime("%H:%M:%S")}
    for reg, config in state.register_address_details.items():
        dtype = config["data_type"]
        if dtype in ["INT16", "UINT16","INT32", "UINT32", "INT64", "UINT64"]:
            row[reg] = random.randint(10, 15)
        elif dtype == "BOOL":
            row[reg] = random.choice([0, 1])
        elif dtype == "FLOAT":
            row[reg] = round(random.uniform(0.1, 2.0), 2)
    state.table_data.append(row)
    
def schedule_update(state):
    update_table(state)
    Timer(1, lambda: schedule_update(state)).start()
schedule_update = lambda state: Timer(1, lambda: (update_table(state), schedule_update(state))).start()
# ip_address = "192.168.1.1"
with tgb.Page() as page:
    with tgb.part("container"):
        tgb.text("# **UDP** FINS PROTOCOL CHECK", mode="md", class_name="container-title")
        with tgb.part("card",class_name="card compact-card"):
            with tgb.layout(columns="2 3"):
                with tgb.part():
                    # tgb.text("Column 1")
                    tgb.text("### Enter IP Address", mode="md")
                    tgb.input(value="{ip_address}" ,label = "Ex: 192.168.1.1")
                    tgb.button(label="Check", class_name="check-button")
                # Column 2 with nested layout
                with tgb.part():
                    with tgb.layout(columns="1 1"):
                        # Subcolumn 1
                        with tgb.part():
                            tgb.text("**MODEL**: *{model}*", mode="md",class_name = "row-bold")
                            tgb.text("**STATUS**: *{status}*", mode="md",class_name = "row-bold")
                            tgb.text("**CLOCKSET**: *{clockset}*", mode="md",class_name = "row-bold")
                        
                        # Subcolumn 2
                        with tgb.part():
                            tgb.text("**OS Version**: *{os_version}*", mode="md",class_name = "row-bold")
                            tgb.text("**BOOT Version**: *{boot_version}*", mode="md",class_name = "row-bold")
        
        # tgb.html("br")            
        with tgb.part("card",class_name="card compact-card"):
            tgb.text("### Enter Register details", mode="md", class_name="card-title")
            with tgb.layout(columns="1 1 1"):
                # Column 1
                with tgb.part():
                    tgb.text("**Register Address**", mode="md", )
                    tgb.input(value="{register_address}", label="Ex: D100, D100.01")
                    tgb.text("Available Memeory areas: [D,H,A,W,T,C]")
                    tgb.text(" *Note: For CIO use 100,100.01")
                # Column 2
                with tgb.part():
                    tgb.text("**Data Type**", mode="md")
                    tgb.selector(
                        value="{data_type}",
                        lov="{data_type_list}",
                        dropdown=True,
                        label ="default = INT16",
                    )
                # Column 3 
                with tgb.part():
                    tgb.text("**Trigger Type**", mode="md")
                    with tgb.layout(columns="1 1"):
                        with tgb.part():
                            tgb.selector("{trigger_type}", 
                                    lov = ["Continuos Trigger", "Event Trigger"],
                                    mode="check",)
                            
                        with tgb.part():
                            tgb.input(value="{trigger_interval}", label= "Ex 1s,5s,10s", placeholder="Ex: 1s,5s,10s") 
                            tgb.text("Default 1s", mode="md")
            
            
            with tgb.part(class_name="button-wrapper"):
                tgb.button(label="Add to table", class_name="Add-to-table-button", on_action=add_to_table)      
            tgb.table(data="{table_data}", columns="{cols}")
    # Add the table to display the register details 
                
            

                    
                
            
    #     # tgb.text(value="# UDP FINS PROTOCOL CHECK", mode="md")
        
# Gui(page=page,data={"table_data": table_data, "cols": cols},css_file="style.css").run(use_reloader=True,dark_mode=False)
gui = Gui(page=page, css_file="style.css")
gui.run(use_reloader=True, dark_mode=False)