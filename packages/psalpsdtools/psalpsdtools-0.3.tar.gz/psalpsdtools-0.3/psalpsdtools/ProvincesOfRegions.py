class getPrvs:
    def __init__(self, regname):
        self.regname = regname

        if regname == "CAR":
            reg_Arr = ["Aurora","Bataan","Bulacan","Nueva Ecija","Pampanga","Tarlac","Zambales"]
        elif regname == "Ilocos Region":
            reg_Arr = ["Ilocos Norte","Ilocos Sur","La Union","Pangasinan"]
        elif regname == "Cagayan Valley":
            reg_Arr = ["Batanes","Cagayan","Isabela","Nueva Vizcaya","Quirino"]
        elif regname == "Central Luzon":
            reg_Arr = ["Aurora","Bataan","Bulacan","Nueva Ecija","Pampanga","Tarlac","Zambales"]
        elif regname == "CALABARZON":
            reg_Arr = ["Batangas","Cavite","Laguna","Quezon","Rizal"]
        elif regname == "MIMAROPA Region":
            reg_Arr = ["Marinduque","Occidental Mindoro","Oriental Mindoro","Palawan","Romblon"]
        elif regname == "Bicol Region":
            reg_Arr = ["Albay","Camarines Norte","Camarines Sur","Catanduanes","Masbate","Sorsogon"]
        elif regname == "Western Visayas":
            reg_Arr = ["Aklan","Antique","Capiz","Guimaras","Iloilo","Negros Occidental"]
        elif regname == "Central Visayas":
            reg_Arr = ["Bohol","Cebu","Negros Oriental","Siquijor"]
        elif regname == "Eastern Visayas":
            reg_Arr = ["Biliran","Eastern Samar","Leyte","Northern Samar","Samar","Southern Leyte"]
        elif regname == "Zamboanga Peninsula":
            reg_Arr = ["Zamboanga del Norte","Zamboanga del Sur","Zamboanga Sibugay"]
        elif regname == "Northern Mindanao":
            reg_Arr = ["Bukidnon","Camiguin","Lanao del Norte","Misamis Occidental","Misamis Oriental"]
        elif regname == "Davao Region":
            reg_Arr = ["Davao de Oro","Davao del Norte","Davao del Sur","Davao Occidental","Davao Oriental"]
        elif regname == "SOCCSKSARGEN":
            reg_Arr = ["Cotabato","Sarangani","South Cotabato","Sultan Kudarat"]
        elif regname == "Caraga":
            reg_Arr = ["Agusan del Norte","Agusan del Sur","Surigao del Norte","Surigao del Sur","Dinagat Islands"]
        elif regname == "BARMM":
            reg_Arr = ["Basilan","Lanao del Sur","Maguindanao","Sulu","Tawi-Tawi","Eight Area Cluster"]

        return reg_Arr