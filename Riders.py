import pandas as pd
import os


file_path = os.path.join(os.getcwd(), "Rosslyn_Evenings.csv") #https://www.w3schools.com/python/ref_os_getcwd.asp
df = pd.read_csv(file_path)

df['date'] = pd.to_datetime(df['Day'], errors='coerce')

df['Entries'] = df['Entries'].astype(str).str.strip()  #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html
df['Entries'] = df['Entries'].str.replace(r'[^0-9]', '', regex=True) 
df['Entries'] = pd.to_numeric(df['Entries'], errors='coerce')  

df['Exits'] = df['Exits'].astype(str).str.strip()
df['Exits'] = df['Exits'].str.replace(r'[^0-9]', '', regex=True)
df['Exits'] = pd.to_numeric(df['Exits'], errors='coerce')

print("Unique Entries after cleaning:", df['Entries'].unique()) #https://numpy.org/doc/stable/reference/generated/numpy.unique.html
print("Unique Exits after cleaning:", df['Exits'].unique())

df = df.dropna(subset=['date']) #https://www.w3schools.com/python/pandas/ref_df_dropna.asp

weekends = df[df['date'].dt.weekday >= 5] #https://www.geeksforgeeks.org/weekday-function-of-datetime-date-class-in-python/

weekends = weekends.dropna(subset=['Entries', 'Exits']) 

average_entries = weekends['Entries'].mean()
average_exits = weekends['Exits'].mean()

print(f"Average Entries (Weekends): {average_entries}")
print(f"Average Exits (Weekends): {average_exits}")