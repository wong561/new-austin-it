
#import importlib
from operator import index
from sqlite3 import Row
import pandas as pd
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
#import test2
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
#from kivymd.uix.toolbar import MDTopAppBar
#from kivymd.uix.textfield import MDTextField
import babel.numbers
#from kivy.uix.image import Image
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from amortization.amount import calculate_amortization_amount
from amortization.schedule import amortization_schedule
from tabulate import tabulate
from amortization.period import calculate_amortization_period
import numpy as np
from datetime import date
from kivy.uix.anchorlayout import AnchorLayout

from main2 import get_data_table






__version__ = "1.0.3" 








class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

class SimpleLoanCalculator(MDApp):
    #abc=StringProperty('test2')

    dialog = None

    def build(self):
        #self.icon = 'icon.png'
        self.root_widget = Builder.load_file('main1.kv')
        self.theme_cls.primary_palette = "Blue"        
        #return self.root_widget

    def calculate(self):
        self.root.ids.test.text = f'Montant total: {self.root.ids.totaal.text}!' 

        totaal = f'{self.root.ids.totaal.text}'
        aanbetaling = f'{self.root.ids.aanbetaling.text}'
        interest = f'{self.root.ids.interest.text}'
        aflossing = f'{self.root.ids.aflossing.text}'
        voldaan = f'{self.root.ids.voldaan.text}' 

        

        percentage = float(aanbetaling) * 0.01 
        saldo = float(totaal) - (float(percentage)*float(totaal))

        interestInUS = float(interest) * (float(saldo) / 100)

        bedrag = (float(saldo) + float(interestInUS)) / float(aflossing)
        aanbetalingUSD = float(percentage)*float(totaal)

        huidigSaldo = (float(totaal) - float(aanbetalingUSD)) - (float(bedrag) * float(voldaan))

        afgelost = float(bedrag) * float(voldaan)

        terugBetalen = float(totaal) + float(interestInUS)


        self.data_tables = MDDataTable(
            
            size_hint=(0.9, 0.6),
            # name column, width column
            column_data=[
                ("Column 1", dp(30)),
                ("Column 2", dp(30)),
                ("Column 3", dp(30)),
                ("Column 4", dp(30)),
                ("Column 5", dp(30)),
                ("Column 6", dp(30)),
            ],
        )
        
                 
        if not self.dialog:
            self.dialog = MDDialog(
                title="Resultaat van de berekening",
                type="simple",
                items=[
                    Item(text= f"Totale leensom: {babel.numbers.format_currency(totaal, 'USD', locale='en_US')}", source="user-1.png"),
                    Item(text= f"Terug te betalen: {babel.numbers.format_currency(terugBetalen, 'USD', locale='en_US')}", source="user-1.png"),
                    Item(text= f'Aanbetaling: {self.root.ids.aanbetaling.text}% ', source="user-2.png"),
                    Item(text= f'Interest: {self.root.ids.interest.text}% ', source="add-icon.png"),
                    Item(text= f'Aantal maanden: {self.root.ids.aflossing.text}', source="add-icon.png"),
                    Item(text= f'Maanden afgelost: {self.root.ids.voldaan.text}', source="add-icon.png"),
                    Item(text= f"Interest: {babel.numbers.format_currency(interestInUS, 'USD', locale='en_US')}", source="add-icon.png"),
                    Item(text= f"Aanbetaling: {babel.numbers.format_currency(aanbetalingUSD, 'USD', locale='en_US')}", source="add-icon.png"),
                    Item(text= f"Saldo na aanbetaling: {babel.numbers.format_currency(saldo, 'USD', locale='en_US')}", source="add-icon.png"),
                    Item(text= f"Aflossing: {babel.numbers.format_currency(bedrag, 'USD', locale='en_US')} per maand ", source="add-icon.png"),
                    Item(text= f"Afgelost: {babel.numbers.format_currency(afgelost, 'USD', locale='en_US')}", source="add-icon.png"),
                    Item(text= f"Huidig saldo: {babel.numbers.format_currency(huidigSaldo, 'USD', locale='en_US')}", source="add-icon.png"),
                ],
            )
        
    
    #Calculate the results.
    def get_data_table(df):
        column_data = list(df.columns)
        row_data = df.to_records(index=False)
        
        return column_data, row_data


    def calculateResults(self):
        '''p_num=float(self.root.ids.totaal.text)
        apr=float(self.root.ids.interest.text)
        per_int=int(self.root.ids.aflossing.text)
        MDY=amortization_schedule(p_num,apr,per_int)
        df = pd.DataFrame(MDY)
        column_data = list(df.columns)
        row_data = df.to_records(index=False)
        xx=get_data_table(df)'''
        totaal = f'{self.root.ids.totaal.text}'
        aanbetaling = f'{self.root.ids.aanbetaling.text}'
        interest = f'{self.root.ids.interest.text}'
        aflossing = f'{self.root.ids.aflossing.text}'
        voldaan = f'{self.root.ids.voldaan.text}' 

        percentage = float(aanbetaling) * 0.01 

        interestPercentage = float(interest) * 0.01

        saldo = float(totaal) - (float(percentage)*float(totaal))

        interestInUS = float(interest) * (float(saldo) / 100)        

        aanbetalingUSD = float(percentage)*float(totaal)

        leenBedrag = float(totaal) - float(aanbetalingUSD)

        bedrag = calculate_amortization_amount(float(leenBedrag), float(interestPercentage), float(aflossing))

        afgelost = float(bedrag) * float(voldaan)

        terugBetalen = float(saldo) + float(interestInUS)

        huidigSaldo = float(terugBetalen) - (float(bedrag) * float(voldaan)) 

        
        self.root.ids.totale_leensom.secondary_text=f"{babel.numbers.format_currency(totaal, 'USD', locale='en_US')}"
        self.root.ids.aanbetaling_in_usd.secondary_text=f"{babel.numbers.format_currency(aanbetalingUSD, 'USD', locale='en_US')}"
        self.root.ids.leen_bedrag.secondary_text=f"{babel.numbers.format_currency(leenBedrag, 'USD', locale='en_US')}"
        self.root.ids.res_aanbetaling.secondary_text=f"{self.root.ids.aanbetaling.text}% "
        self.root.ids.interest_percentage.secondary_text=f"{self.root.ids.interest.text}% "
        self.root.ids.aantal_maanden.secondary_text=f"{self.root.ids.aflossing.text}"
        self.root.ids.reeds_afgelost.secondary_text=f"{self.root.ids.voldaan.text}"        
        #self.root.ids.saldo_na_aanbetaling.secondary_text=f"{babel.numbers.format_currency(saldo, 'USD', locale='en_US')}"
        self.root.ids.aflossing_per_maand.secondary_text=f"{babel.numbers.format_currency(bedrag, 'USD', locale='en_US')}"
        #self.root.ids.reeds_afgelost_in_USD.secondary_text=f"{babel.numbers.format_currency(afgelost, 'USD', locale='en_US')}"
        
        '''print(schedule) 
        print(period_int) 
        print(p_float)
        print(apr_float)'''        
        '''print(df.tail(4))'''
        print("*****************************************************************************")
        #print("row_data",row_data)
        #print("column data",column_data)
        #print("xx",xx)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.screen_manager.current = "scr 3"
        
    
    # Clear the input boxes.
    def clearInput(self):        
        self.root.ids.totaal.text=''
        self.root.ids.aanbetaling.text=''
        self.root.ids.interest.text=''
        self.root.ids.aflossing.text=''
        self.root.ids.voldaan.text ='' 
    #def amort_schedule(principal, interest_rate,period):
    

    


    def showSchedule(self):
        p_num=float(self.root.ids.totaal.text)
        apr=float(self.root.ids.interest.text)
        per_int=int(self.root.ids.aflossing.text)
        MDY=amortization_schedule(p_num,apr,per_int)
        df = pd.DataFrame(MDY)
        column_data = list(df.columns)
        rows = df.to_records(index=False)
       
        
        
        #xx=get_data_table(df)
        #principal = f'{self.root.ids.totaal.text}'
        p_float=float(self.root.ids.totaal.text)

        interest_rate = f'{self.root.ids.interest.text}'
        apr_float=float(self.root.ids.interest.text)
        period = f'{self.root.ids.aflossing.text}'
        period_int=int(self.root.ids.aflossing.text)
        schedule=amortization_schedule(p_float,apr_float,period_int)
        voldaan = f'{self.root.ids.voldaan.text}' 
        

            
        
        screen=Screen()
        #layout=MDDataTable()
        table=MDDataTable(
            size_hint=(0.5,0.5),

            pos_hint={"center_x":0.5,'center_y':0.5},
            #check=False,
            column_data = [("prenom",dp(25)),
                ("nom",dp(25)),
                ("adresse e-mail",dp(35)),
                ("numero de telephone",dp(30)),
                ("Column 5",dp(30))],
            row_data=[('1','2','3','4','5')]
            
                
                
            #use_pagination=False
        )
        
            
            
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.screen_manager.current = "scr 4"
        return screen
        
    
         
            
    def backButton(self):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.screen_manager.current = "scr 1"



        
            

    def open_table(self):
        self.root.ids.data_tables.open()
        
        #self.root.ids.nav_drawer.set_state("close")
        self.root.ids.screen_manager.current = "scr 4"   

    def build(self):
        #self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Blue" 
        self.root_widget = Builder.load_file('main1.kv')
        return self.root_widget
        
    
    
    
        

        
             
        



SimpleLoanCalculator().run()