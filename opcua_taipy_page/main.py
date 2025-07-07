from taipy.gui import Gui
import taipy.gui.builder as tgb
import datetime
import random
from threading import Timer
import pandas as pd
ip_address = " "
model = "CJ2M-CPU15"
status = "Connected"
mode = "Run"
clockset = "2025-07-01 10:30"

os_version = "v2.3.5"
boot_version = "v1.1.9"


data_type_list = ["INT16", "UINT16","INT32", "UINT32", "INT64", "UINT64", "FLOAT", "DOUBLE", "BOOL"]

register_address = " "
data_type = "INT16"
trigger_type = "Continuous Trigger"
trigger_interval = 1  # in seconds
register_address_details = {}
table_data = []
cols = ["timestamp"]

# Global variable for the table
table_df = pd.DataFrame()
update_needed = False
count = 1
def generate_data(state):
    global table_df
    global count
    if count == 1:
    
        start_time = datetime.datetime.now()
        timestamps = [start_time + datetime.timedelta(seconds=i) for i in range(100)]
        values = [random.randint(15, 20) for _ in range(100)]

        # Create a DataFrame
        table_df = pd.DataFrame({
            "timestamp": [ts.strftime("%H:%M:%S") for ts in timestamps],
            "D100": values
        })

        # Assign to state for Taipy GUI to render
        # print(table_df.head())
        state.table_df = table_df
        table_df.to_csv("dummy_data.csv")
        count = 2
    else:
        start_time = datetime.datetime.now()
        timestamps = [start_time + datetime.timedelta(seconds=i) for i in range(100)]
        values = [random.randint(15, 20) for _ in range(100)]
        boolean_values = [random.choice([0, 1]) for _ in range(100)]
        # Create a DataFrame
        table_df = pd.DataFrame({
            "timestamp": [ts.strftime("%H:%M:%S") for ts in timestamps],
            "D100": values,
            "W100.01": boolean_values
        })

        # Assign to state for Taipy GUI to render
        # print(table_df.head())
        state.table_df = table_df
        table_df.to_csv("dummy_data.csv")
        
dummy_data = pd.read_csv("dummy_data.csv")
print(dummy_data.head())
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
                            tgb.text("**MODE**: *{mode}*", mode="md",class_name = "row-bold")
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
                                    lov = ["Continuous Trigger", "Event Trigger"],
                                    mode="radio",)
                            print("trigger_type", trigger_type) 
                        with tgb.part():
                            tgb.input(value="{trigger_interval}", label= "Ex 1s,5s,10s", placeholder="Ex: 1s,5s,10s") 
                            tgb.text("Default 1s", mode="md")
            
            
            with tgb.part(class_name="button-wrapper"):
                tgb.button(label="Add to table", class_name="Add-to-table-button", on_action=generate_data)      
        with tgb.part():
            tgb.table(data="{dummy_data}")


gui = Gui(page=page, css_file="style.css")
gui.run(use_reloader=True, dark_mode=False)