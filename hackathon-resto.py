import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_restaurant_data = pd.read_csv("restaurant_data.csv")

if df_restaurant_data.isnull().values.any():
    print("Hay valores faltantes en las siguientes columnas:")
    print(df_restaurant_data.isnull().sum())
else:
    print("No hay fallos")

columns = list(df_restaurant_data.columns)
df_restaurant_data = df_restaurant_data.drop_duplicates()
df_restaurant_data = df_restaurant_data.drop_duplicates(subset=columns)


df_restaurant_data['Marketing Percentage'] = (df_restaurant_data['Marketing Budget'] /
                                                              df_restaurant_data['Revenue']) * 100

df_restaurant_data['Revenue per Follower'] = round(df_restaurant_data['Revenue'] / df_restaurant_data['Social Media Followers'],3)
# print(df_restaurant_data[['Name','Social Media Followers', 'Revenue','Marketing Percentage of Revenue', 'Revenue per Follower']].head())


df_restaurant_data['Consumption per Pax'] = df_restaurant_data['Revenue'] / df_restaurant_data['Average Meal Price']


restaurants_by_cuisine = df_restaurant_data['Cuisine'].value_counts()
print("Cantidad de Restaurantes por Tipo de Cocina:")
print(restaurants_by_cuisine)

# grafico con la ganancia total y el tipo de        

revenue_by_cuisine = df_restaurant_data.groupby('Cuisine')['Revenue'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
revenue_by_cuisine.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Ganancia Total por Tipo de Cocina")
plt.xlabel("Tipo de Cocina")
plt.ylabel("Ganancia Total ($)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()




#grafico inversion mrkt y consumo por pax por tipode cocina
unique_cuisines = df_restaurant_data['Cuisine'].unique()
color_palette = sns.color_palette("tab10", len(unique_cuisines))
cuisine_color_map = dict(zip(unique_cuisines, color_palette))
df_restaurant_data['Color'] = df_restaurant_data['Cuisine'].map(cuisine_color_map)
plt.figure(figsize=(12, 8))
for cuisine, color in cuisine_color_map.items():
    subset = df_restaurant_data[df_restaurant_data['Cuisine'] == cuisine]
    plt.scatter(subset['Marketing Percentage'], subset['Consumption per Pax'], 
                color=color, label=cuisine, alpha=0.7)

plt.title("Relación entre Porcentaje de Marketing y Consumo por Pax por Tipo de Cocina")
plt.xlabel("Porcentaje de Inversión en Marketing (%)")
plt.ylabel("Consumo por Pax")
plt.legend(title="Cuisine", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

df_best_relations = df_restaurant_data.sort_values(
    by=['Marketing Percentage of Revenue', 'Revenue per Follower'], 
    ascending=[True, False])

print("Mejor relacion en inversion en marketing y ganancia por seguidor:")
print(df_best_relations[['Name', 'Marketing Percentage of Revenue', 'Revenue per Follower']].head(10))


print("Mejor relacion de la experiencia del chef y cantidad de pax por mes: ")
def costumers_month(df_restaurant_data):
    df_restaurant_data["nr of costumers"] = df_restaurant_data["Revenue"]/df_restaurant_data["Average Meal Price"]
    return df_restaurant_data
#grafico de barras para los 10 mejores
df_top_chefs = df_best_relations.head(10)

